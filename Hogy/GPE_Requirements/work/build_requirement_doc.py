from pathlib import Path
import re
import json
import zipfile
from lxml import etree
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Twips
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'work' / 'requirements.md'
OUTPUT = ROOT / 'GPE_Requirement_Document_HRIS_People_Payroll_v0.1.docx'
TOKENS = {
    'preset': 'standard_business_brief', 'header_pattern': 'memo_masthead',
    'page_dxa': [12240, 15840], 'margin_dxa': 1440,
    'header_footer_inches': 0.492, 'font': 'Calibri',
    'body': [11, 0, 6, 1.1],
    'h1': [16, 16, 8, '2E74B5'], 'h2': [13, 12, 6, '2E74B5'],
    'h3': [12, 8, 4, '1F4D78'],
    'list': {'left': 720, 'hanging': 360, 'after': 8, 'line_twips': 280},
    'table': {'width': 9360, 'indent': 120, 'margin': [80, 80, 120, 120], 'fill': 'F2F4F7'},
    'overrides': {
        'Title': '26 pt black; before 0 after 4; line 1.1; bold',
        'Subtitle': '14 pt muted; before 0 after 16; line 1.1',
        'Meta': '9.5 pt muted; before 0 after 4; line 1.1',
        'Table Text': '10 pt black; before 0 after 4; line 1.1',
        'Callout': '11 pt; fill F4F6F9; before 6 after 10; line 1.1',
        'Header/Footer': '9 pt muted; before 0 after 0; line 1.0; no rule',
    }
}

def el(tag, **attrs):
    n = OxmlElement('w:' + tag)
    for k, v in attrs.items():
        n.set(qn('w:' + k), str(v))
    return n

def configure_style(doc, name, size, before, after, color='222222', line=1.1, bold=False):
    s = doc.styles[name] if name in doc.styles else doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    s.font.name = 'Calibri'
    s.font.size = Pt(size)
    s.font.color.rgb = RGBColor.from_string(color)
    s.font.bold = bold
    s.font.italic = False
    rpr = s.element.get_or_add_rPr()
    fonts = rpr.find(qn('w:rFonts'))
    if fonts is None:
        fonts = el('rFonts'); rpr.append(fonts)
    for k in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
        fonts.set(qn('w:' + k), 'Calibri')
    lang = rpr.find(qn('w:lang'))
    if lang is None:
        lang = el('lang'); rpr.append(lang)
    lang.set(qn('w:val'), 'id-ID')
    pf = s.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    pf.line_spacing = line
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.widow_control = True
    return s

def configure_numbering(doc):
    root = doc.part.numbering_part.element
    abstract_ids = [int(n.get(qn('w:abstractNumId'))) for n in root.findall(qn('w:abstractNum'))]
    num_ids = [int(n.get(qn('w:numId'))) for n in root.findall(qn('w:num'))]
    for offset, (name, fmt, text) in enumerate([('List Bullet', 'bullet', '•'), ('List Number', 'decimal', '%1.')], 1):
        aid = max(abstract_ids, default=0) + offset
        nid = max(num_ids, default=0) + offset
        abstract = el('abstractNum', abstractNumId=aid)
        abstract.append(el('multiLevelType', val='singleLevel'))
        level = el('lvl', ilvl=0)
        level.append(el('start', val=1)); level.append(el('numFmt', val=fmt))
        level.append(el('lvlText', val=text)); level.append(el('lvlJc', val='left'))
        ppr = el('pPr')
        tabs = el('tabs'); tabs.append(el('tab', val='num', pos=720)); ppr.append(tabs)
        ppr.append(el('ind', left=720, hanging=360))
        ppr.append(el('spacing', before=0, after=160, line=280, lineRule='auto'))
        level.append(ppr)
        rpr = el('rPr'); rpr.append(el('rFonts', ascii='Calibri', hAnsi='Calibri')); level.append(rpr)
        abstract.append(level); root.append(abstract)
        num = el('num', numId=nid); num.append(el('abstractNumId', val=aid)); root.append(num)
        s = configure_style(doc, name, 11, 0, 8, line=280/240)
        s.paragraph_format.left_indent = Twips(720)
        s.paragraph_format.first_line_indent = Twips(-360)
        spr = s.element.get_or_add_pPr()
        existing = spr.find(qn('w:numPr'))
        if existing is not None: spr.remove(existing)
        numpr = el('numPr'); numpr.append(el('ilvl', val=0)); numpr.append(el('numId', val=nid)); spr.append(numpr)

def add_field(p, name):
    r = p.add_run()
    r._r.append(el('fldChar', fldCharType='begin'))
    ins = el('instrText'); ins.set(qn('xml:space'), 'preserve'); ins.text = ' ' + name + ' '
    r._r.append(ins); r._r.append(el('fldChar', fldCharType='end'))

def add_text(doc, text, style='Normal'):
    p = doc.add_paragraph(style=style)
    if ': ' in text and (text.startswith('Kriteria penerimaan:') or text.startswith('Keputusan:') or text.startswith('Owner usulan:')):
        label, body = text.split(': ', 1)
        p.add_run(label + ': ').bold = True; p.add_run(body)
    else:
        p.add_run(text)
    return p

def add_table(doc, rows):
    headers = rows[0]
    widths = [1800, 4400, 3160]
    if headers[0] == 'Peran': widths = [2050, 3300, 4010]
    elif headers[0] == 'Fungsi reviewer': widths = [3650, 2500, 3210]
    elif rows[1][0].startswith('UAT'): widths = [1100, 5100, 3160]
    elif rows[1][0].startswith('INT'): widths = [1100, 3500, 4760]
    elif rows[1][0].startswith('RPT'): widths = [1100, 4550, 3710]
    assert len(widths) == len(headers) and sum(widths) == 9360
    t = doc.add_table(rows=len(rows), cols=len(headers))
    t.autofit = False
    pr = t._tbl.tblPr
    for tag in ('tblW', 'tblInd', 'tblCellMar', 'tblBorders'):
        old = pr.find(qn('w:' + tag))
        if old is not None: pr.remove(old)
    pr.append(el('tblW', type='dxa', w=9360))
    pr.append(el('tblInd', type='dxa', w=120))
    mar = el('tblCellMar')
    for k, v in [('top', 80), ('bottom', 80), ('start', 120), ('end', 120)]: mar.append(el(k, w=v, type='dxa'))
    pr.append(mar)
    borders = el('tblBorders')
    for k in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV'):
        borders.append(el(k, val='single', sz=4, color='D7DBE2'))
    pr.append(borders)
    for col, w in zip(t._tbl.tblGrid.gridCol_lst, widths): col.set(qn('w:w'), str(w))
    for ri, (row, vals) in enumerate(zip(t.rows, rows)):
        row._tr.get_or_add_trPr().append(el('cantSplit'))
        if ri == 0: row._tr.get_or_add_trPr().append(el('tblHeader'))
        for ci, (c, val) in enumerate(zip(row.cells, vals)):
            c.width = Twips(widths[ci]); c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            c._tc.get_or_add_tcPr().find(qn('w:tcW')).set(qn('w:type'), 'dxa')
            if ri == 0: c._tc.get_or_add_tcPr().append(el('shd', fill='F2F4F7', val='clear'))
            p = c.paragraphs[0]; p.style = doc.styles['Table Text']
            p.paragraph_format.keep_with_next = ri == 0
            if ci == 0 and headers[0] == 'ID': p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.add_run(val).bold = ri == 0
    return t

def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Twips(12240); section.page_height = Twips(15840)
    section.top_margin = section.bottom_margin = section.left_margin = section.right_margin = Twips(1440)
    section.header_distance = section.footer_distance = Inches(0.492)
    configure_style(doc, 'Normal', 11, 0, 6)
    configure_style(doc, 'Title', 26, 0, 4, '000000', bold=True)
    configure_style(doc, 'Subtitle', 14, 0, 16, '555555')
    for idx, values in enumerate([TOKENS['h1'], TOKENS['h2'], TOKENS['h3']], 1):
        size, before, after, color = values
        st = configure_style(doc, f'Heading {idx}', size, before, after, color, bold=True)
        st.paragraph_format.keep_with_next = True
    configure_style(doc, 'Meta', 9.5, 0, 4, '555555')
    configure_style(doc, 'Table Text', 10, 0, 4)
    configure_style(doc, 'Table Citation', 9.5, 4, 4, '555555')
    configure_style(doc, 'Callout', 11, 6, 10)
    configure_style(doc, 'Header', 9, 0, 0, '666666', line=1)
    configure_style(doc, 'Footer', 9, 0, 0, '666666', line=1)
    configure_numbering(doc)
    hp = section.header.paragraphs[0]; hp.style = 'Header'
    hp.add_run('GPE  |  HRIS, People & Payroll')
    fp = section.footer.paragraphs[0]; fp.style = 'Footer'
    fp.paragraph_format.tab_stops.add_tab_stop(Twips(9360), WD_TAB_ALIGNMENT.RIGHT)
    fp.add_run('v0.1 - Draft for Review\t'); fp.add_run('Halaman '); add_field(fp, 'PAGE')
    doc.core_properties.title = 'GPE Requirement Document - HRIS, People & Payroll'
    doc.core_properties.subject = 'User and functional requirements based on MOM 18, 21, 22 July 2026'
    doc.core_properties.author = 'Draft untuk review GPE'
    doc.core_properties.keywords = 'GPE, HRIS, payroll, requirement, draft'
    lines = SOURCE.read_text(encoding='utf-8').splitlines()
    i = 0; first_h1 = True; first_h2 = True; pagebreak_next = False
    while i < len(lines):
        line = lines[i].strip()
        if not line: i += 1; continue
        if line == '---': pagebreak_next = True; i += 1; continue
        if line.startswith('|'):
            raw = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                vals = [s.strip() for s in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', s) for s in vals): raw.append(vals)
                i += 1
            add_table(doc, raw)
            continue
        if line.startswith('# '):
            p = add_text(doc, line[2:], 'Title' if first_h1 else 'Heading 1')
            first_h1 = False
        elif line.startswith('## '):
            p = add_text(doc, line[3:], 'Subtitle' if first_h2 else 'Heading 2')
            first_h2 = False
        elif line.startswith('### '):
            p = add_text(doc, line[4:], 'Heading 3')
        elif line.startswith('- '):
            p = add_text(doc, line[2:], 'List Bullet')
        elif line.startswith('> '):
            p = add_text(doc, line[2:], 'Callout')
            p._p.get_or_add_pPr().append(el('shd', val='clear', fill='F4F6F9'))
        else:
            meta = line.startswith(('Status:', 'Document ID:', 'Versi:', 'Tanggal penyusunan:', 'Referensi pembahasan:', 'Lingkup organisasi:', 'Klasifikasi:'))
            p = add_text(doc, line, 'Meta' if meta else 'Normal')
            if line.startswith('Status:'): p.paragraph_format.keep_with_next = True
        if pagebreak_next:
            p.paragraph_format.page_break_before = True; pagebreak_next = False
        i += 1
    doc.save(OUTPUT)
    (ROOT / 'work' / 'design_tokens.json').write_text(json.dumps(TOKENS, indent=2), encoding='utf-8')
    return audit()

def audit():
    doc = Document(OUTPUT)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for s in doc.sections:
        assert s.page_width.twips == 12240 and s.page_height.twips == 15840
        assert all(getattr(s, n).twips == 1440 for n in ['top_margin', 'bottom_margin', 'left_margin', 'right_margin'])
        assert abs(s.header_distance.inches - 0.492) < 0.001
        assert abs(s.footer_distance.inches - 0.492) < 0.001
    for name, size, before, after, line in [('Normal',11,0,6,1.1),('Heading 1',16,16,8,1.1),('Heading 2',13,12,6,1.1),('Heading 3',12,8,4,1.1)]:
        st = doc.styles[name]; pf = st.paragraph_format
        assert st.font.name == 'Calibri' and st.font.size.pt == size
        assert pf.space_before.pt == before and pf.space_after.pt == after
        assert abs(pf.line_spacing-line) < 0.01
    for t in doc.tables:
        pr = t._tbl.tblPr
        assert pr.find(qn('w:tblW')).get(qn('w:w')) == '9360'
        assert pr.find(qn('w:tblInd')).get(qn('w:w')) == '120'
        widths = [int(x.get(qn('w:w'))) for x in t._tbl.tblGrid]
        assert sum(widths) == 9360
        for row in t.rows:
            assert row.height is None
            assert [c.width.twips for c in row.cells] == widths
        assert t.rows[0]._tr.trPr.find(qn('w:tblHeader')) is not None
    text = SOURCE.read_text(encoding='utf-8')
    definitions = re.findall(r'^### ([A-Z]+-\d{2}) \|', text, re.M)
    decisions = re.findall(r'^### (D\d{2}) \|', text, re.M)
    assert len(definitions) == len(set(definitions))
    assert len(decisions) == 16 and len(set(decisions)) == 16
    decision_refs = set(re.findall(r'\bD\d{2}\b', text))
    assert decision_refs == set(decisions)
    table_ids = re.findall(r'^\| ((?:INT|RPT|UAT)-\d{2}) \|', text, re.M)
    known = set(definitions + table_ids)
    refs = set(re.findall(r'\b[A-Z]{2,4}-\d{2}\b', text))
    assert refs <= known, refs-known
    headings = [p.text for p in doc.paragraphs if p.style.name.startswith('Heading')]
    assert all(not p.text.startswith(('- ', '• ')) for p in doc.paragraphs)
    with zipfile.ZipFile(OUTPUT) as z:
        for n in z.namelist():
            if n.endswith('.xml'): etree.fromstring(z.read(n))
    report = {
        'output': str(OUTPUT), 'bytes': OUTPUT.stat().st_size,
        'requirement_definitions': len(definitions),
        'functional_requirements': len([x for x in definitions if not x.startswith('NFR')]),
        'nfr': len([x for x in definitions if x.startswith('NFR')]),
        'open_decisions': len(decisions), 'integration_points': len([x for x in table_ids if x.startswith('INT')]),
        'reports': len([x for x in table_ids if x.startswith('RPT')]),
        'uat_scenarios': len([x for x in table_ids if x.startswith('UAT')]),
        'tables': len(doc.tables), 'headings': len(headings),
        'words_approx': len(text.split()),
        'structural_checks': 'PASS', 'visual_qa': 'PENDING renderer availability'
    }
    (ROOT / 'work' / 'qa_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    build()
