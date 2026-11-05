from pathlib import Path
from zipfile import ZipFile
from docx import Document
from docx.oxml.ns import qn

DOCX = Path(r"E:\Panda\MITO\.tmp_blueprint\reference.docx")
doc = Document(DOCX)

def val(x):
    return None if x is None else str(x)

print("SECTIONS", len(doc.sections))
for i, s in enumerate(doc.sections, 1):
    print("SECTION", i, {
        "page_width": val(s.page_width), "page_height": val(s.page_height),
        "top": val(s.top_margin), "bottom": val(s.bottom_margin),
        "left": val(s.left_margin), "right": val(s.right_margin),
        "header_distance": val(s.header_distance), "footer_distance": val(s.footer_distance),
        "different_first": s.different_first_page_header_footer,
    })

print("STYLES")
for name in ["Normal", "BP Head 1", "BP Head 2", "BP Head 3", "List Paragraph", "Caption"]:
    if name not in [s.name for s in doc.styles]:
        continue
    st = doc.styles[name]
    f = st.font
    p = st.paragraph_format
    print(name, {
        "font": f.name, "size": val(f.size), "bold": f.bold, "italic": f.italic,
        "color": val(f.color.rgb), "before": val(p.space_before), "after": val(p.space_after),
        "line": val(p.line_spacing), "left": val(p.left_indent), "first": val(p.first_line_indent),
        "keep_next": p.keep_with_next, "page_break": p.page_break_before,
    })

print("BODY COUNTS", len(doc.paragraphs), len(doc.tables), len(doc.inline_shapes))
for i, p in enumerate(doc.paragraphs[:90]):
    txt = p.text.strip().replace("\n", " ")
    if txt:
        size = next((r.font.size for r in p.runs if r.font.size), None)
        bold = any(bool(r.bold) for r in p.runs)
        print("P", i, p.style.name, val(size), bold, repr(txt[:150]))

for si, s in enumerate(doc.sections, 1):
    for kind, part in [("header", s.header), ("first_header", s.first_page_header), ("footer", s.footer), ("first_footer", s.first_page_footer)]:
        print("PART", si, kind, "paras", len(part.paragraphs), "tables", len(part.tables))
        for pi, p in enumerate(part.paragraphs):
            if p.text.strip():
                print(" ", pi, p.style.name, repr(p.text.strip()))
        for ti, t in enumerate(part.tables):
            print(" TABLE", ti, "rows", len(t.rows), "cols", len(t.columns), "style", t.style.name if t.style else None)
            for row in t.rows[:3]:
                print("  ", [c.text.strip().replace("\n", " | ")[:100] for c in row.cells])

with ZipFile(DOCX) as z:
    names = z.namelist()
    print("PACKAGE PARTS", len(names))
    for n in names:
        if n.startswith(("word/header", "word/footer", "word/media/", "word/theme", "word/styles", "word/numbering")):
            info = z.getinfo(n)
            print("PARTFILE", n, info.file_size)
