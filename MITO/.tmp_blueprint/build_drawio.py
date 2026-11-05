from __future__ import annotations

import ast
import html
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path


BASE = Path(r"E:\Panda\MITO\.tmp_blueprint")
SOURCE = BASE / "build_blueprint.py"
OUTPUT = Path(r"E:\Panda\MITO\MITO SFA Mobile - Business Process Flow.drawio")

TYPE_COLORS = {
    "Standard": "#C6E0B4",
    "Manual": "#BDD7EE",
    "Customization": "#F4B6C2",
    "Integration": "#F8CBAD",
}


def extract_processes():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    row_sets = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name.startswith("P") and len(name) >= 3 and name[1:3].isdigit():
                row_sets[name] = ast.literal_eval(node.value)

    processes = []
    for node in tree.body:
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            continue
        call = node.value
        if not isinstance(call.func, ast.Name) or call.func.id != "add_process":
            continue
        code = ast.literal_eval(call.args[0])
        title = ast.literal_eval(call.args[1])
        purpose = ast.literal_eval(call.args[2])
        rows_name = call.args[3].id
        notes = []
        if len(call.args) >= 5:
            notes = ast.literal_eval(call.args[4])
        processes.append({
            "code": code,
            "title": title,
            "purpose": purpose,
            "rows": row_sets[rows_name],
            "notes": notes,
        })
    return processes


def style_text(size=12, bold=False, color="#1F2937", align="left", vertical="middle"):
    weight = "fontStyle=1;" if bold else ""
    return (
        f"html=1;whiteSpace=wrap;align={align};verticalAlign={vertical};"
        f"fontFamily=Arial;fontSize={size};fontColor={color};{weight}"
    )


def add_vertex(root, cell_id, value, x, y, w, h, style, parent="1"):
    cell = ET.SubElement(root, "mxCell", {
        "id": cell_id,
        "value": value,
        "style": style,
        "vertex": "1",
        "parent": parent,
    })
    ET.SubElement(cell, "mxGeometry", {
        "x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"
    })
    return cell


def add_edge(root, cell_id, source, target, label="", style_extra=""):
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;"
        "html=1;endArrow=block;endFill=1;strokeColor=#64748B;strokeWidth=1.5;"
        "fontFamily=Arial;fontSize=10;fontColor=#334155;labelBackgroundColor=#FFFFFF;"
        + style_extra
    )
    cell = ET.SubElement(root, "mxCell", {
        "id": cell_id,
        "value": html.escape(label),
        "style": style,
        "edge": "1",
        "parent": "1",
        "source": source,
        "target": target,
    })
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    return cell


def new_graph(page_width, page_height):
    model = ET.Element("mxGraphModel", {
        "dx": "1422", "dy": "794", "grid": "1", "gridSize": "10", "guides": "1",
        "tooltips": "1", "connect": "1", "arrows": "1", "fold": "1", "page": "1",
        "pageScale": "1", "pageWidth": str(page_width), "pageHeight": str(page_height),
        "math": "0", "shadow": "0", "background": "#FFFFFF",
    })
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    return model, root


def diagram_id(name):
    return uuid.uuid5(uuid.NAMESPACE_URL, f"mito-sfa:{name}").hex[:20]


def build_overview(processes):
    process_rows = (len(processes) + 2) // 3
    note_y = 395 + process_rows * 100
    width, height = 1800, max(1150, note_y + 125)
    model, root = new_graph(width, height)
    add_vertex(root, "ov-title", "MITO SFA MOBILE — ARSITEKTUR & DAFTAR PROSES", 0, 0, width, 55,
               "shape=rect;rounded=0;fillColor=#111827;strokeColor=#111827;" + style_text(22, True, "#FFFFFF", "left"))
    add_vertex(root, "ov-title-clean", "MITO SFA MOBILE - ARSITEKTUR & DAFTAR PROSES", 0, 0, width, 55,
               "shape=rect;rounded=0;fillColor=#111827;strokeColor=#111827;" + style_text(22, True, "#FFFFFF", "left"))

    add_vertex(root, "ov-sfa", "<b>SFA MOBILE</b><br><font size='10'>Internal & External User</font>", 210, 110, 330, 120,
               "rounded=1;arcSize=12;fillColor=#DCE6F1;strokeColor=#4472C4;strokeWidth=2;" + style_text(18, True, "#111827", "center"))
    add_vertex(root, "ov-cms", "<b>CMS</b><br><font size='10'>Bridge & Source of Truth</font>", 735, 110, 330, 120,
               "rounded=1;arcSize=12;fillColor=#E2F0D9;strokeColor=#70AD47;strokeWidth=2;" + style_text(18, True, "#111827", "center"))
    add_vertex(root, "ov-odoo", "<b>ODOO</b><br><font size='10'>ERP Backend</font>", 1260, 110, 330, 120,
               "rounded=1;arcSize=12;fillColor=#FCE4D6;strokeColor=#ED7D31;strokeWidth=2;" + style_text(18, True, "#111827", "center"))
    add_edge(root, "ov-e1", "ov-sfa", "ov-cms", "Data & transaksi dua arah", "startArrow=block;startFill=1;")
    add_edge(root, "ov-e2", "ov-cms", "ov-odoo", "Integrasi dua arah melalui CMS", "startArrow=block;startFill=1;")
    add_vertex(root, "ov-boundary", "<b>Batas arsitektur:</b> tidak terdapat koneksi langsung antara SFA Mobile dan Odoo.", 500, 255, 800, 45,
               "shape=note;size=15;fillColor=#FFF2CC;strokeColor=#D6B656;" + style_text(12, False, "#5B4700", "center"))

    add_vertex(root, "ov-legend-title", "LEGENDA TYPE", 60, 340, 260, 35,
               "shape=rect;fillColor=#374151;strokeColor=#374151;" + style_text(13, True, "#FFFFFF", "center"))
    for i, (type_name, color) in enumerate(TYPE_COLORS.items()):
        add_vertex(root, f"ov-leg-{i}", f"<b>{type_name}</b>", 60, 385 + i * 60, 260, 45,
                   f"rounded=1;fillColor={color};strokeColor=#94A3B8;" + style_text(12, True, "#111827", "center"))

    add_vertex(root, "ov-list-title", "HALAMAN FLOW PROSES", 370, 340, 1370, 35,
               "shape=rect;fillColor=#374151;strokeColor=#374151;" + style_text(13, True, "#FFFFFF", "center"))
    for i, process in enumerate(processes):
        col, row = i % 3, i // 3
        x, y = 370 + col * 455, 385 + row * 100
        label = f"<b>{html.escape(process['code'])}</b><br>{html.escape(process['title'])}"
        add_vertex(root, f"ov-p-{i}", label, x, y, 425, 75,
                   "rounded=1;arcSize=8;fillColor=#F8FAFC;strokeColor=#94A3B8;" + style_text(12, False, "#111827", "left"))

    add_vertex(root, "ov-note", "Flow mengikuti header, deskripsi proses, dan urutan aktivitas pada blueprint. Cabang exception, retry, dan approval ditandai pada proses terkait dan dapat diperdalam pada blueprint teknis.", 370, note_y, 1370, 55,
               "shape=note;size=15;fillColor=#EAF2F8;strokeColor=#5B9BD5;" + style_text(11, False, "#1F4E79", "left"))
    broken_title = root.find("./mxCell[@id='ov-title']")
    if broken_title is not None:
        root.remove(broken_title)
    return model


def edge_label(process_code, from_id, to_id):
    labels = {
        ("P01B", "P01-EXT-06", "P01-EXT-07"): "Perlu revisi",
        ("P05", "P05-RSC-03", "P05-RSC-04"): "Disetujui",
        ("P13", "P13-WAR-05", "P13-WAR-06"): "Disetujui",
        ("P17", "P17-OFF-03", "P17-SYN-01"): "Koneksi tersedia",
        ("P17", "P17-SYN-01", "P17-SYN-02"): "Failed",
        ("P18", "P18-APR-03", "P18-APR-04"): "Hasil keputusan",
    }
    return labels.get((process_code, from_id, to_id), "")


def activity_label(act_id, act_name, description, type_name):
    return (
        f"<div style='text-align:center'><b>{html.escape(act_name)}</b></div>"
        f"<div style='text-align:center;font-size:10px;color:#475569'>{html.escape(act_id)} | {html.escape(type_name)}</div>"
        f"<hr><div style='text-align:left;font-size:10px'>{html.escape(description)}</div>"
    )


def build_process(process):
    rows = process["rows"]
    lanes = []
    for row in rows:
        pic = row[2]
        if pic not in lanes:
            lanes.append(pic)

    lane_h = 165
    node_w, node_h, step_x = 210, 112, 245
    content_x = 300
    page_width = max(1800, content_x + len(rows) * step_x + 220)
    notes_h = 95 if process["notes"] else 25
    page_height = max(900, 165 + len(lanes) * lane_h + notes_h + 70)
    model, root = new_graph(page_width, page_height)

    title = f"{process['code']} — {process['title']}"
    title = f"{process['code']} - {process['title']}"
    add_vertex(root, "title", html.escape(title), 0, 0, page_width, 55,
               "shape=rect;rounded=0;fillColor=#111827;strokeColor=#111827;" + style_text(22, True, "#FFFFFF", "left"))
    purpose = f"<b>Deskripsi Proses:</b> {html.escape(process['purpose'])}"
    add_vertex(root, "purpose", purpose, 25, 62, page_width - 50, 65,
               "shape=rect;rounded=0;fillColor=none;strokeColor=none;" + style_text(12, False, "#334155", "left", "top"))

    lane_y = {}
    for i, lane in enumerate(lanes):
        y = 145 + i * lane_h
        lane_y[lane] = y
        fill = "#F8FAFC" if i % 2 == 0 else "#EEF2F7"
        add_vertex(root, f"lane-bg-{i}", "", 20, y, page_width - 40, lane_h - 8,
                   f"shape=rect;rounded=0;fillColor={fill};strokeColor=#CBD5E1;strokeWidth=1;")
        add_vertex(root, f"lane-label-{i}", html.escape(lane), 20, y, 155, lane_h - 8,
                   "shape=rect;rounded=0;fillColor=#475569;strokeColor=#334155;" + style_text(12, True, "#FFFFFF", "center"))

    node_ids = []
    for i, row in enumerate(rows):
        act_id, act_name, pic, description, type_name = row
        x = content_x + i * step_x
        y = lane_y[pic] + 23
        color = TYPE_COLORS.get(type_name, "#FFFFFF")
        label = (
            f"<div style='text-align:center'><b>{html.escape(act_name)}</b></div>"
            f"<div style='text-align:center;font-size:10px;color:#475569'>{html.escape(act_id)} · {html.escape(type_name)}</div>"
            f"<hr><div style='text-align:left;font-size:10px'>{html.escape(description)}</div>"
        )
        label = activity_label(act_id, act_name, description, type_name)
        node_id = f"act-{i}"
        node_ids.append(node_id)
        cell = add_vertex(root, node_id, label, x, y, node_w, node_h,
                          f"rounded=1;arcSize=8;fillColor={color};strokeColor=#64748B;strokeWidth=1.5;spacing=7;" + style_text(11, False, "#111827", "center", "middle"))
        cell.set("tooltip", description)

    first_pic = rows[0][2]
    last_pic = rows[-1][2]
    add_vertex(root, "start", "Mulai", 195, lane_y[first_pic] + 50, 70, 60,
               "ellipse;aspect=fixed;fillColor=#A9D18E;strokeColor=#548235;strokeWidth=2;" + style_text(11, True, "#1F3B13", "center"))
    end_x = content_x + len(rows) * step_x
    add_vertex(root, "end", "Selesai", end_x, lane_y[last_pic] + 50, 70, 60,
               "ellipse;aspect=fixed;fillColor=#F4B6C2;strokeColor=#C00000;strokeWidth=2;" + style_text(11, True, "#7F0000", "center"))
    add_edge(root, "edge-start", "start", node_ids[0])

    for i in range(len(rows) - 1):
        from_id, to_id = rows[i][0], rows[i + 1][0]
        # Revision returns to the registration submission; approval continues directly to activation.
        if process["code"] == "P01B" and from_id == "P01-EXT-07" and to_id == "P01-EXT-08":
            idx_send = next(j for j, item in enumerate(rows) if item[0] == "P01-EXT-03")
            add_edge(root, f"edge-{i}", node_ids[i], node_ids[idx_send], "Kirim ulang", "dashed=1;strokeColor=#C65911;")
            continue
        add_edge(root, f"edge-{i}", node_ids[i], node_ids[i + 1], edge_label(process["code"], from_id, to_id))

    if process["code"] == "P01B":
        idx_review = next(i for i, row in enumerate(rows) if row[0] == "P01-EXT-06")
        idx_activate = next(i for i, row in enumerate(rows) if row[0] == "P01-EXT-08")
        add_edge(root, "edge-p01-approved", node_ids[idx_review], node_ids[idx_activate], "Disetujui", "strokeColor=#548235;")
    if process["code"] == "P17":
        idx_sync = next(i for i, row in enumerate(rows) if row[0] == "P17-SYN-01")
        idx_monitor = next(i for i, row in enumerate(rows) if row[0] == "P17-SYN-03")
        add_edge(root, "edge-p17-ok", node_ids[idx_sync], node_ids[idx_monitor], "Pending / Synced", "strokeColor=#548235;")

    add_edge(root, "edge-end", node_ids[-1], "end")

    if process["notes"]:
        note_y = 155 + len(lanes) * lane_h
        note_text = "<b>Catatan proses</b><br>" + "<br>".join(f"• {html.escape(item)}" for item in process["notes"])
        note_text = "<b>Catatan proses</b><br>" + "<br>".join(f"- {html.escape(item)}" for item in process["notes"])
        add_vertex(root, "notes", note_text, 180, note_y, page_width - 220, 75,
                   "shape=note;size=14;fillColor=#FFF2CC;strokeColor=#D6B656;spacing=8;" + style_text(11, False, "#5B4700", "left", "top"))

    return model


def build_p01b(process):
    groups = [
        ("Registrasi Owner", [row for row in process["rows"] if row[0].startswith("P01-EXT-")]),
        ("Registrasi Staff", [row for row in process["rows"] if row[0].startswith("P01-STF-")]),
    ]
    lane_h = 165
    node_w, node_h, step_x = 210, 112, 245
    content_x = 300
    max_steps = max(len(rows) for _, rows in groups)
    page_width = max(1800, content_x + max_steps * step_x + 220)

    group_meta = []
    page_height = 145
    for group_name, rows in groups:
        lanes = []
        for row in rows:
            if row[2] not in lanes:
                lanes.append(row[2])
        group_height = 45 + len(lanes) * lane_h + 35
        group_meta.append((group_name, rows, lanes, group_height))
        page_height += group_height
    page_height += 50

    model, root = new_graph(page_width, page_height)
    title = f"{process['code']} - {process['title']}"
    add_vertex(root, "title", html.escape(title), 0, 0, page_width, 55,
               "shape=rect;rounded=0;fillColor=#111827;strokeColor=#111827;" + style_text(22, True, "#FFFFFF", "left"))
    purpose = f"<b>Deskripsi Proses:</b> {html.escape(process['purpose'])}"
    add_vertex(root, "purpose", purpose, 25, 62, page_width - 50, 65,
               "shape=rect;rounded=0;fillColor=none;strokeColor=none;" + style_text(12, False, "#334155", "left", "top"))

    group_y = 145
    for group_index, (group_name, rows, lanes, group_height) in enumerate(group_meta):
        prefix = f"g{group_index}"
        add_vertex(root, f"{prefix}-header", group_name, 20, group_y, page_width - 40, 34,
                   "shape=rect;rounded=0;fillColor=#1F4E78;strokeColor=#17365D;" + style_text(13, True, "#FFFFFF", "left"))
        lane_y = {}
        for lane_index, lane in enumerate(lanes):
            y = group_y + 44 + lane_index * lane_h
            lane_y[lane] = y
            fill = "#F8FAFC" if lane_index % 2 == 0 else "#EEF2F7"
            add_vertex(root, f"{prefix}-lane-bg-{lane_index}", "", 20, y, page_width - 40, lane_h - 8,
                       f"shape=rect;rounded=0;fillColor={fill};strokeColor=#CBD5E1;strokeWidth=1;")
            add_vertex(root, f"{prefix}-lane-label-{lane_index}", html.escape(lane), 20, y, 155, lane_h - 8,
                       "shape=rect;rounded=0;fillColor=#475569;strokeColor=#334155;" + style_text(12, True, "#FFFFFF", "center"))

        node_ids = []
        for row_index, row in enumerate(rows):
            act_id, act_name, pic, description, type_name = row
            node_id = f"{prefix}-act-{row_index}"
            node_ids.append(node_id)
            x = content_x + row_index * step_x
            y = lane_y[pic] + 23
            color = TYPE_COLORS.get(type_name, "#FFFFFF")
            cell = add_vertex(root, node_id, activity_label(act_id, act_name, description, type_name), x, y, node_w, node_h,
                              f"rounded=1;arcSize=8;fillColor={color};strokeColor=#64748B;strokeWidth=1.5;spacing=7;" + style_text(11, False, "#111827", "center", "middle"))
            cell.set("tooltip", description)

        start_id, end_id = f"{prefix}-start", f"{prefix}-end"
        add_vertex(root, start_id, "Mulai", 195, lane_y[rows[0][2]] + 50, 70, 60,
                   "ellipse;aspect=fixed;fillColor=#A9D18E;strokeColor=#548235;strokeWidth=2;" + style_text(11, True, "#1F3B13", "center"))
        end_x = content_x + len(rows) * step_x
        add_vertex(root, end_id, "Selesai", end_x, lane_y[rows[-1][2]] + 50, 70, 60,
                   "ellipse;aspect=fixed;fillColor=#F4B6C2;strokeColor=#C00000;strokeWidth=2;" + style_text(11, True, "#7F0000", "center"))
        add_edge(root, f"{prefix}-edge-start", start_id, node_ids[0])

        for row_index in range(len(rows) - 1):
            from_id, to_id = rows[row_index][0], rows[row_index + 1][0]
            if from_id == "P01-EXT-07" and to_id == "P01-EXT-08":
                submit_index = next(i for i, item in enumerate(rows) if item[0] == "P01-EXT-03")
                add_edge(root, f"{prefix}-edge-{row_index}", node_ids[row_index], node_ids[submit_index], "Kirim ulang", "dashed=1;strokeColor=#C65911;")
                continue
            add_edge(root, f"{prefix}-edge-{row_index}", node_ids[row_index], node_ids[row_index + 1], edge_label(process["code"], from_id, to_id))

        if group_name == "Registrasi Owner":
            review_index = next(i for i, row in enumerate(rows) if row[0] == "P01-EXT-06")
            activate_index = next(i for i, row in enumerate(rows) if row[0] == "P01-EXT-08")
            add_edge(root, f"{prefix}-edge-approved", node_ids[review_index], node_ids[activate_index], "Disetujui", "strokeColor=#548235;")

        add_edge(root, f"{prefix}-edge-end", node_ids[-1], end_id)
        group_y += group_height

    return model


def main():
    processes = extract_processes()
    mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "agent": "Codex",
        "version": "24.7.17",
        "type": "device",
    })

    overview = ET.SubElement(mxfile, "diagram", {"id": diagram_id("overview"), "name": "00 - Overview"})
    overview.append(build_overview(processes))

    for process in processes:
        diagram = ET.SubElement(mxfile, "diagram", {
            "id": diagram_id(process["code"]),
            "name": f"{process['code']} - {process['title']}",
        })
        diagram.append(build_p01b(process) if process["code"] == "P01B" else build_process(process))

    ET.indent(mxfile, space="  ")
    tree = ET.ElementTree(mxfile)
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)
    print(f"{OUTPUT}\npages={1 + len(processes)}")


if __name__ == "__main__":
    main()
