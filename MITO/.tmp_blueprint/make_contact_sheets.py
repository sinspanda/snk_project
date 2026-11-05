from pathlib import Path
from PIL import Image, ImageDraw

folder = Path(r"E:\Panda\MITO\.tmp_blueprint\final_render_4")
pages = sorted(folder.glob("qa-*.png"))
outdir = folder / "contact_qa"
outdir.mkdir(exist_ok=True)
for offset in range(0, len(pages), 4):
    batch = pages[offset:offset + 4]
    ims = [Image.open(p).convert("RGB") for p in batch]
    w = max(im.width for im in ims)
    h = max(im.height for im in ims)
    sheet = Image.new("RGB", (w * 2 + 30, h * 2 + 30), "#d0d0d0")
    draw = ImageDraw.Draw(sheet)
    for idx, (path, im) in enumerate(zip(batch, ims)):
        x = (idx % 2) * (w + 10) + 5
        y = (idx // 2) * (h + 10) + 5
        sheet.paste(im, (x, y))
        draw.rectangle((x, y, x + 70, y + 24), fill="white", outline="black")
        draw.text((x + 5, y + 4), path.stem, fill="black")
    sheet.save(outdir / f"contact-{offset + 1:02d}-{offset + len(batch):02d}.png")
print(len(list(outdir.glob('contact-*.png'))))
