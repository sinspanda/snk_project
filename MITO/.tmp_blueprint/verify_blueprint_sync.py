from pathlib import Path
import re
import xml.etree.ElementTree as ET

from docx import Document


BASE = Path(r"E:\Panda\MITO")
DOCX = BASE / "MITO SFA Mobile - Blueprint Draft V0.1.docx"
DRAWIO = BASE / "MITO SFA Mobile - Business Process Flow.drawio"


doc = Document(DOCX)
paragraphs = [p.text.strip() for p in doc.paragraphs]
process_headings = [
    text for text in paragraphs
    if re.match(r"^P(?:01[A-C]|0[2-9]|1[0-8]) - ", text)
]

missing_descriptions = []
for heading in process_headings:
    index = paragraphs.index(heading)
    following = next((text for text in paragraphs[index + 1:] if text), "")
    if not following.startswith("Deskripsi Proses: "):
        missing_descriptions.append(heading)

root = ET.parse(DRAWIO).getroot()
page_names = [diagram.attrib["name"] for diagram in root.findall("diagram")]
drawio_process_pages = page_names[1:]

if process_headings != drawio_process_pages:
    raise SystemExit(
        "Header mismatch\nDOCX: " + repr(process_headings) +
        "\nDRAWIO: " + repr(drawio_process_pages)
    )
if missing_descriptions:
    raise SystemExit("Missing process descriptions: " + repr(missing_descriptions))
if "\ufffd" in DRAWIO.read_text(encoding="utf-8"):
    raise SystemExit("Draw.io contains replacement characters")

vertices = len(root.findall(".//mxCell[@vertex='1']"))
edges = len(root.findall(".//mxCell[@edge='1']"))
print(f"process_headers={len(process_headings)}")
print(f"drawio_pages={len(page_names)}")
print(f"descriptions={len(process_headings)}")
print(f"vertices={vertices}")
print(f"edges={edges}")
print("status=OK")
