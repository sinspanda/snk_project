from pathlib import Path
from pypdf import PdfReader, PdfWriter

folder = Path(r"E:\Panda\MITO\.tmp_blueprint\final_render_4")
files = sorted(folder.glob("page-*.pdf"))
writer = PdfWriter()
for path in files:
    reader = PdfReader(path)
    for page in reader.pages:
        writer.add_page(page)
out = folder / "blueprint-merged.pdf"
with out.open("wb") as stream:
    writer.write(stream)
print(out, len(writer.pages))
