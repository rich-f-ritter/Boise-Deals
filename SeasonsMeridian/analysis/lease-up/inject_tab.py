#!/usr/bin/env python3
"""Inject 'Lease-Up Bridge' into the .xlsm by rewriting only the parts it owns.

Why not openpyxl: loading and re-saving the model destroys 8 of its 15 charts and
drops 60 package parts. Why not copy/paste in Excel: moving a sheet between
workbooks rewrites every cross-sheet reference as an external link back to the
source file, which is exactly what broke the first attempt.

So the sheet is written straight into the package. Every byte the sheet does not
own is passed through untouched.

Strings are emitted inline rather than through sharedStrings.xml, so the model's
string table is never renumbered.
"""
import re
import shutil
import sys
import zipfile
from xml.sax.saxutils import escape

MODEL_IN = sys.argv[1] if len(sys.argv) > 1 else 'model.xlsm'
MODEL_OUT = sys.argv[2] if len(sys.argv) > 2 else 'model_with_tab.xlsm'
STANDALONE = 'Lease-Up Bridge (drop into model).xlsx'
SHEETNAME = 'Lease-Up Bridge'


def sheet_target(z):
    """(worksheet path, r:id) of the sheet we are replacing."""
    wbx = z.read('xl/workbook.xml').decode('utf8')
    m = re.search(r'<sheet[^>]*name="%s"[^>]*r:id="(rId\d+)"' % re.escape(SHEETNAME), wbx)
    if not m:
        raise SystemExit(f'"{SHEETNAME}" not found in the workbook — add it once in Excel first')
    rid = m.group(1)
    rels = z.read('xl/_rels/workbook.xml.rels').decode('utf8')
    t = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels).group(1)
    return 'xl/' + t.lstrip('/'), rid


def inline_strings(xml, shared):
    """t="s" -> t="inlineStr" so the model's sharedStrings table is left alone."""
    def sub(m):
        idx = int(m.group(2))
        txt = escape(shared[idx]) if idx < len(shared) else ''
        return f'{m.group(1)} t="inlineStr"><is><t xml:space="preserve">{txt}</t></is></c>'
    return re.sub(r'(<c\b[^>]*?) t="s"[^>]*>\s*<v>(\d+)</v>\s*</c>', sub, xml)


def main():
    zin = zipfile.ZipFile(MODEL_IN)
    zsa = zipfile.ZipFile(STANDALONE)
    target, _rid = sheet_target(zin)
    names = zin.namelist()

    # next free indices in the model's package
    def nxt(pref):
        ns = [int(re.search(r'(\d+)\.xml$', n).group(1)) for n in names
              if n.startswith(pref) and re.search(r'\d+\.xml$', n) and '_rels' not in n]
        return (max(ns) + 1) if ns else 1

    c0, d0 = nxt('xl/charts/chart'), nxt('xl/drawings/drawing')
    chart_map = {f'chart{i+1}.xml': f'chart{c0+i}.xml' for i in range(3)}
    draw_new = f'drawing{d0}.xml'

    # --- worksheet: inline its strings, point its drawing rel at the new drawing
    shared = []
    if 'xl/sharedStrings.xml' in zsa.namelist():
        sx = zsa.read('xl/sharedStrings.xml').decode('utf8')
        shared = [re.sub(r'<[^>]+>', '', s) for s in re.findall(r'<si>(.*?)</si>', sx, re.S)]
        shared = [s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>') for s in shared]
    ws = zsa.read('xl/worksheets/sheet1.xml').decode('utf8')
    ws = inline_strings(ws, shared)

    # --- drawing + charts
    dr = zsa.read('xl/drawings/drawing1.xml').decode('utf8')
    drr = zsa.read('xl/drawings/_rels/drawing1.xml.rels').decode('utf8')
    # rel targets may be absolute (/xl/charts/chartN.xml) or relative (../charts/…);
    # match on the filename so the new drawing cannot end up pointing at the model's
    # own charts, which share the low index numbers.
    for old, new in chart_map.items():
        drr = re.sub(r'(?<=[/\\])' + re.escape(old) + r'(?=")', new, drr)
    for old in chart_map:
        assert f'/{old}"' not in drr, f'chart rel still points at {old}'

    out_parts = {
        target: ws.encode('utf8'),
        f'xl/worksheets/_rels/{target.split("/")[-1]}.rels':
            ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
             f'relationships/drawing" Target="../drawings/{draw_new}"/></Relationships>').encode('utf8'),
        f'xl/drawings/{draw_new}': dr.encode('utf8'),
        f'xl/drawings/_rels/{draw_new}.rels': drr.encode('utf8'),
    }
    for old, new in chart_map.items():
        out_parts[f'xl/charts/{new}'] = zsa.read(f'xl/charts/{old}')

    # --- content types
    ct = zin.read('[Content_Types].xml').decode('utf8')
    add = ''
    for new in chart_map.values():
        if f'/xl/charts/{new}' not in ct:
            add += (f'<Override PartName="/xl/charts/{new}" ContentType="application/vnd.'
                    f'openxmlformats-officedocument.drawingml.chart+xml"/>')
    if f'/xl/drawings/{draw_new}' not in ct:
        add += (f'<Override PartName="/xl/drawings/{draw_new}" ContentType="application/vnd.'
                f'openxmlformats-officedocument.drawing+xml"/>')
    if f'/{target}' not in ct:
        add += (f'<Override PartName="/{target}" ContentType="application/vnd.openxmlformats-'
                f'officedocument.spreadsheetml.worksheet+xml"/>')
    ct = ct.replace('</Types>', add + '</Types>')
    # calcChain is dropped, not patched: it indexes the sheet we just replaced, and a
    # stale chain makes Excel evaluate cells in an order the new formulas do not admit.
    # Excel rebuilds it silently on open.
    ct = re.sub(r'<Override PartName="/xl/calcChain\.xml"[^>]*/>', '', ct)
    out_parts['[Content_Types].xml'] = ct.encode('utf8')

    # force a full recalculation on open so the injected formulas evaluate immediately
    wbx = zin.read('xl/workbook.xml').decode('utf8')
    if '<calcPr' in wbx:
        wbx = re.sub(r'<calcPr([^>]*?)/>',
                     lambda m: '<calcPr' + re.sub(r'\s*fullCalcOnLoad="[^"]*"', '', m.group(1))
                     + ' fullCalcOnLoad="1"/>', wbx, count=1)
    else:
        wbx = wbx.replace('</workbook>', '<calcPr fullCalcOnLoad="1"/></workbook>')
    out_parts['xl/workbook.xml'] = wbx.encode('utf8')

    # --- write: pass every untouched part through byte-for-byte
    replaced = set(out_parts)
    with zipfile.ZipFile(MODEL_OUT, 'w', zipfile.ZIP_DEFLATED) as zo:
        for item in zin.infolist():
            if item.filename in replaced or item.filename == 'xl/calcChain.xml':
                continue
            zo.writestr(item, zin.read(item.filename))
        for name, data in out_parts.items():
            zo.writestr(name, data)
    zin.close()
    zsa.close()

    zc = zipfile.ZipFile(MODEL_OUT)
    bad = zc.testzip()
    print(f'wrote {MODEL_OUT}')
    print(f'  replaced worksheet : {target}')
    print(f'  charts injected    : {", ".join(chart_map.values())}')
    print(f'  drawing injected   : {draw_new}')
    print(f'  parts in package   : {len(zc.namelist())}  (zip integrity: {bad or "OK"})')


if __name__ == '__main__':
    main()
