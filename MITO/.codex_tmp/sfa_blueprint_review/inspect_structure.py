from __future__ import annotations

import json
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph


def clean(text: str) -> str:
    return " ".join((text or "").replace("\u00a0", " ").split())


def iter_block_items(document):
    body = document.element.body
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def paragraph_level(paragraph: Paragraph):
    ppr = paragraph._p.pPr
    if ppr is not None:
        outline = ppr.find(qn("w:outlineLvl"))
        if outline is not None:
            try:
                return int(outline.get(qn("w:val"))) + 1
            except (TypeError, ValueError):
                pass
    style_el = paragraph.style.element if paragraph.style is not None else None
    if style_el is not None and style_el.pPr is not None:
        outline = style_el.pPr.find(qn("w:outlineLvl"))
        if outline is not None:
            try:
                return int(outline.get(qn("w:val"))) + 1
            except (TypeError, ValueError):
                pass
    name = paragraph.style.name if paragraph.style is not None else ""
    lower = name.lower()
    for prefix in ("heading ", "bp head ", "toc "):
        if lower.startswith(prefix):
            tail = lower[len(prefix):].strip()
            if tail.isdigit():
                return int(tail)
    return None


def app_props(path: Path):
    result = {}
    with zipfile.ZipFile(path) as zf:
        if "docProps/app.xml" in zf.namelist():
            root = ET.fromstring(zf.read("docProps/app.xml"))
            for child in root:
                result[child.tag.split("}")[-1]] = child.text
    return result


def main():
    path = Path(sys.argv[1])
    range_start = None
    range_end = None
    if "--from" in sys.argv[2:]:
        range_start = int(sys.argv[sys.argv.index("--from") + 1])
    if "--to" in sys.argv[2:]:
        range_end = int(sys.argv[sys.argv.index("--to") + 1])
    doc = Document(path)
    styles = Counter()
    nonempty = 0
    outlines = []
    body_flow = []
    table_summaries = []

    for idx, block in enumerate(iter_block_items(doc), start=1):
        if isinstance(block, Paragraph):
            text = clean(block.text)
            style = block.style.name if block.style is not None else "(none)"
            styles[style] += 1
            if not text:
                continue
            nonempty += 1
            level = paragraph_level(block)
            lower_style = style.lower()
            item = {"order": idx, "kind": "paragraph", "style": style, "level": level, "text": text}
            body_flow.append(item)
            if level is not None or lower_style.startswith(("bp head", "toc", "title")):
                outlines.append(item)
        else:
            rows = []
            for row in block.rows:
                rows.append([clean(cell.text) for cell in row.cells])
            summary = {
                "order": idx,
                "kind": "table",
                "rows": len(rows),
                "cols": max((len(r) for r in rows), default=0),
                "preview": rows[:5],
            }
            table_summaries.append(summary)
            body_flow.append(summary)

    headers = []
    footers = []
    for s_idx, section in enumerate(doc.sections, start=1):
        for label, part, target in (
            ("header", section.header, headers),
            ("first_header", section.first_page_header, headers),
            ("even_header", section.even_page_header, headers),
            ("footer", section.footer, footers),
            ("first_footer", section.first_page_footer, footers),
            ("even_footer", section.even_page_footer, footers),
        ):
            values = [clean(p.text) for p in part.paragraphs if clean(p.text)]
            if values:
                target.append({"section": s_idx, "type": label, "text": values})

    output = {
        "path": str(path),
        "app_properties": app_props(path),
        "paragraph_count": len(doc.paragraphs),
        "nonempty_body_paragraphs": nonempty,
        "table_count": len(doc.tables),
        "inline_shape_count": len(doc.inline_shapes),
        "section_count": len(doc.sections),
        "style_counts": styles.most_common(),
        "outline_candidates": outlines,
        "tables": table_summaries,
        "headers": headers,
        "footers": footers,
        "body_flow": body_flow,
    }
    if "--compact" in sys.argv[2:]:
        filtered_flow = [
            item
            for item in body_flow
            if (range_start is None or item["order"] >= range_start)
            and (range_end is None or item["order"] <= range_end)
        ]
        print(
            json.dumps(
                {
                    "app_properties": output["app_properties"],
                    "counts": {
                        "paragraphs": output["paragraph_count"],
                        "nonempty_body_paragraphs": output["nonempty_body_paragraphs"],
                        "tables": output["table_count"],
                        "inline_shapes": output["inline_shape_count"],
                        "sections": output["section_count"],
                    },
                    "style_counts": output["style_counts"],
                    "outline_candidates": output["outline_candidates"],
                    "headers": output["headers"],
                    "footers": output["footers"],
                    "compact_flow": [
                        item
                        if item["kind"] == "paragraph"
                        else {
                            "order": item["order"],
                            "kind": "table",
                            "rows": item["rows"],
                            "cols": item["cols"],
                            "header": item["preview"][0] if item["preview"] else [],
                        }
                        for item in filtered_flow
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
