from pathlib import Path
import pypdfium2 as pdfium


pdf_path = Path(r"E:\Panda\MITO\.tmp_blueprint\final_render_p01_split\blueprint-qa.pdf")
out_dir = pdf_path.parent
pdf = pdfium.PdfDocument(pdf_path)
for index in range(len(pdf)):
    page = pdf[index]
    image = page.render(scale=2.0).to_pil()
    image.save(out_dir / f"page-{index + 1:02d}.png")
print(f"pages={len(pdf)}")
