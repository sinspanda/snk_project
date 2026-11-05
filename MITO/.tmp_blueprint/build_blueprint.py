from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE = Path(r"E:\Panda\MITO\.tmp_blueprint")
REF = BASE / "reference.docx"
OUT = Path(r"E:\Panda\MITO\MITO SFA Mobile - Blueprint Draft V0.1.docx")
MITO_LOGO = BASE / "media" / "mito_logo.png"
SINERKA_LOGO = BASE / "media" / "image2.png"

doc = Document()

def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:fill"), fill)

def set_cell_margins(cell, top=90, start=90, bottom=90, end=90):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in("w:tcMar")
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, v in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(v))
        node.set(qn("w:type"), "dxa")

def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement("w:tblHeader")
    tblHeader.set(qn("w:val"), "true")
    trPr.append(tblHeader)

def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    cant = OxmlElement("w:cantSplit")
    cant.set(qn("w:val"), "true")
    trPr.append(cant)

def set_table_geometry(table, widths_in):
    total = int(sum(widths_in) * 1440)
    tblPr = table._tbl.tblPr
    layout = tblPr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(qn("w:type"), "fixed")
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:w"), str(total))
    tblW.set(qn("w:type"), "dxa")
    tblInd = tblPr.find(qn("w:tblInd"))
    if tblInd is None:
        tblInd = OxmlElement("w:tblInd")
        tblPr.append(tblInd)
    tblInd.set(qn("w:w"), "90")
    tblInd.set(qn("w:type"), "dxa")
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths_in:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(int(width * 1440)))
        grid.append(col)
    for row in table.rows:
        for idx, (cell, width) in enumerate(zip(row.cells, widths_in)):
            cell.width = Inches(width)
            tcPr = cell._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:w"), str(int(width * 1440)))
            tcW.set(qn("w:type"), "dxa")
            set_cell_margins(cell)

def set_run_font(run, name="Arial", size=10, bold=None, italic=None, color=None):
    run.font.name = name
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:ascii"), name)
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)

def clear_container(container):
    element = getattr(container, "_element", container)
    for child in list(element):
        if child.tag != qn("w:sectPr"):
            element.remove(child)

def clear_header_footer(part):
    el = part._element
    for child in list(el):
        el.remove(child)
    p = OxmlElement("w:p")
    el.append(p)

def add_page_field(paragraph):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instr, separate, text, end):
        run._r.append(node)
    set_run_font(run, size=8)

def add_h1(text, page_break=True):
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = page_break
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "000000")
    pPr.append(shd)
    r = p.add_run(text)
    set_run_font(r, size=23, bold=True, color="FFFFFF")
    return p

def add_h2(text, page_break=False):
    p = doc.add_paragraph()
    p.paragraph_format.page_break_before = page_break
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size=17, bold=True)
    return p

def add_h3(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size=14, bold=True)
    return p

def add_body(text, bold_lead=None, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=5):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.08
    if bold_lead and text.startswith(bold_lead):
        r1 = p.add_run(bold_lead)
        set_run_font(r1, bold=True)
        r2 = p.add_run(text[len(bold_lead):])
        set_run_font(r2, italic=italic)
    else:
        r = p.add_run(text)
        set_run_font(r, italic=italic)
    return p

def add_bullets(items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            set_run_font(r)
        if not p.runs:
            r = p.add_run(item)
            set_run_font(r)
        else:
            p.runs[0].text = item

def add_table(headers, rows, widths, font_size=9, type_col=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    table.style = "Table Grid"
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    for i, text in enumerate(headers):
        cell = hdr.cells[i]
        set_cell_shading(cell, "606060")
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(str(text))
        set_run_font(r, size=font_size, bold=True, color="FFFFFF")
    colors = {"Standard": "C6E0B4", "Manual": "BDD7EE", "Customization": "F4B6C2", "Integration": "F8CBAD"}
    for data in rows:
        body_row = table.add_row()
        prevent_row_split(body_row)
        cells = body_row.cells
        for i, text in enumerate(data):
            cell = cells[i]
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in (0, 2, type_col) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.02
            r = p.add_run(str(text))
            set_run_font(r, size=font_size)
            if type_col is not None and i == type_col:
                set_cell_shading(cell, colors.get(str(text), "FFFFFF"))
                r.bold = True
    set_table_geometry(table, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table

def process_table(rows):
    return add_table(
        ["Activity ID", "Activity Name", "PIC", "Description", "Type"],
        rows,
        [0.85, 1.20, 0.88, 1.95, 1.00],
        font_size=8.2,
        type_col=4,
    )

def add_process(code, title, purpose, rows, notes=None, page_break=True):
    add_h2(f"{code} - {title}", page_break=page_break)
    add_body(f"Deskripsi Proses: {purpose}", bold_lead="Deskripsi Proses: ")
    process_table(rows)
    if notes:
        add_h3("Catatan Proses")
        add_bullets(notes)

# Start from a clean package while retaining the reference document's visual grammar.
clear_container(doc._element.body)

# Normalize source-derived styles.
normal = doc.styles["Normal"]
normal.font.name = "Arial"
normal.font.size = Pt(10)
for style_name, size, bold in (("BP Head 1", 23, True), ("BP Head 2", 17, True), ("BP Head 3", 14, True)):
    if style_name in [s.name for s in doc.styles]:
        st = doc.styles[style_name]
        st.font.name = "Arial"
        st.font.size = Pt(size)
        st.font.bold = bold

sec1 = doc.sections[0]
sec1.page_width = Inches(8.27)
sec1.page_height = Inches(11.69)
sec1.left_margin = Inches(1.50)
sec1.right_margin = Inches(0.89)
sec1.top_margin = Inches(1.00)
sec1.bottom_margin = Inches(1.38)
sec1.header_distance = Inches(0.60)
sec1.footer_distance = Inches(0.51)
sec1.different_first_page_header_footer = True
clear_header_footer(sec1.first_page_header)
clear_header_footer(sec1.first_page_footer)
clear_header_footer(sec1.header)
clear_header_footer(sec1.footer)

# Cover page, using the retained blue-band pattern.
cover = doc.add_table(rows=1, cols=2)
cover.alignment = WD_TABLE_ALIGNMENT.LEFT
cover.autofit = False
set_table_geometry(cover, [1.35, 4.53])
left, right = cover.rows[0].cells
set_cell_shading(left, "C6D9F1")
cover.rows[0].height = Inches(7.8)
cover.rows[0].height_rule = WD_ROW_HEIGHT_RULE.EXACTLY
right.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
rp = right.paragraphs[0]
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
rp.paragraph_format.space_after = Pt(6)
r = rp.add_run("SFA MOBILE")
set_run_font(r, size=25, bold=True)
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = rp.add_run("BLUEPRINT SISTEM")
set_run_font(r, size=25, bold=True)
rp.paragraph_format.space_after = Pt(42)
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = rp.add_run("Disiapkan untuk:")
set_run_font(r, size=9, bold=True, italic=True, color="4472C4")
rp.paragraph_format.space_after = Pt(5)
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
shape = rp.add_run().add_picture(str(MITO_LOGO), width=Inches(2.2))
shape._inline.docPr.set("descr", "Logo klien MITO Electronics")
shape._inline.docPr.set("title", "MITO Electronics")
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = rp.add_run("MITO Electronics")
set_run_font(r, size=14, bold=True)
rp.paragraph_format.space_after = Pt(38)
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = rp.add_run("Dipersiapkan oleh:")
set_run_font(r, size=9, bold=True, italic=True, color="4472C4")
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
shape = rp.add_run().add_picture(str(SINERKA_LOGO), height=Inches(1.0))
shape._inline.docPr.set("descr", "Logo penyusun PT. Sinergi Karya Solusindo")
shape._inline.docPr.set("title", "Sinerka")
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = rp.add_run("PT. Sinergi Karya Solusindo")
set_run_font(r, size=14, bold=True)
rp = right.add_paragraph()
rp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = rp.add_run("Draft V0.1 | 10 Agustus 2026")
set_run_font(r, size=9, italic=True, color="666666")

# Body section.
sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
sec2.page_width = Inches(8.27)
sec2.page_height = Inches(11.69)
sec2.left_margin = Inches(1.50)
sec2.right_margin = Inches(0.89)
sec2.top_margin = Inches(1.00)
sec2.bottom_margin = Inches(1.00)
sec2.header_distance = Inches(0.60)
sec2.footer_distance = Inches(0.51)
sec2.different_first_page_header_footer = False
sec2.header.is_linked_to_previous = False
sec2.footer.is_linked_to_previous = False
clear_header_footer(sec2.header)
clear_header_footer(sec2.footer)

# Recurring source-derived header.
header = sec2.header
hp = header.paragraphs[0]
hp._element.getparent().remove(hp._element)
ht = header.add_table(rows=1, cols=4, width=Inches(5.88))
ht.style = "Table Grid"
set_table_geometry(ht, [0.85, 1.20, 2.83, 1.00])
for c in ht.rows[0].cells:
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
ht.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
shape = ht.rows[0].cells[0].paragraphs[0].add_run().add_picture(str(SINERKA_LOGO), height=Inches(0.48))
shape._inline.docPr.set("descr", "Logo penyusun PT. Sinergi Karya Solusindo")
shape._inline.docPr.set("title", "Sinerka")
ht.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
shape = ht.rows[0].cells[1].paragraphs[0].add_run().add_picture(str(MITO_LOGO), width=Inches(0.92))
shape._inline.docPr.set("descr", "Logo klien MITO Electronics")
shape._inline.docPr.set("title", "MITO Electronics")
for idx, text in ((2, "SFA MOBILE BLUEPRINT"), (3, "CMS BRIDGE")):
    p = ht.rows[0].cells[idx].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_run_font(r, size=11 if idx == 2 else 8.5, bold=True)

# Footer with document identity and page field.
footer = sec2.footer
fp = footer.paragraphs[0]
fp._element.getparent().remove(fp._element)
ft = footer.add_table(rows=1, cols=2, width=Inches(5.88))
ft.style = "Table Grid"
set_table_geometry(ft, [4.85, 1.03])
p = ft.rows[0].cells[0].paragraphs[0]
r = p.add_run("Document Name: MITO SFA Mobile - Blueprint Draft V0.1")
set_run_font(r, size=8)
p = ft.rows[0].cells[1].paragraphs[0]
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p.add_run("Page: ")
set_run_font(r, size=8)
add_page_field(p)
p = footer.add_paragraph()
p.paragraph_format.space_before = Pt(2)
p.paragraph_format.space_after = Pt(0)
r = p.add_run("© 2026 ")
set_run_font(r, size=7, bold=True, color="FF0000")
r = p.add_run("PT. Sinergi Karya Solusindo. Dokumen ini bersifat RAHASIA dan hanya digunakan untuk kepentingan proyek MITO SFA.")
set_run_font(r, size=7)

# Document control.
add_h1("Pengendalian Dokumen", page_break=False)
add_h2("Riwayat Dokumen")
add_table(
    ["Versi", "Tanggal", "Penyusun", "Deskripsi"],
    [["0.1", "10 Agustus 2026", "Krisna Prasetya", "Draft awal blueprint SFA Mobile untuk review internal dan klien."]],
    [0.70, 1.25, 1.35, 2.58], 9,
)
add_h2("Distribusi Dokumen")
add_table(
    ["Penerima", "Tujuan"],
    [["MITO Electronics", "Review kebutuhan dan proses bisnis SFA Mobile."], ["PT. Sinergi Karya Solusindo", "Desain solusi dan estimasi implementasi."]],
    [2.00, 3.88], 9,
)

add_h1("Persetujuan")
add_body("Bagian ini disediakan untuk persetujuan setelah draft proses bisnis, ruang lingkup, dan batas integrasi disepakati.")
add_h2("MITO Electronics")
add_table(["Nama", "Peran Proyek", "Tanggal", "Tanda Tangan"], [["", "Project Sponsor", "", ""], ["", "Business Owner / Sales", "", ""], ["", "IT / CMS Owner", "", ""]], [1.55, 1.75, 1.10, 1.48], 9)
add_h2("PT. Sinergi Karya Solusindo")
add_table(["Nama", "Peran Proyek", "Tanggal", "Tanda Tangan"], [["Krisna Prasetya", "Project Manager / Functional", "", ""], ["", "Technical Lead", "", ""]], [1.55, 1.75, 1.10, 1.48], 9)

add_h1("Legenda")
add_body("Kolom Type digunakan sebagai pemetaan awal fit-gap dan effort implementasi, khususnya untuk pekerjaan pengembangan SFA Mobile dan integrasinya.")
legend_rows = [
    ["Standard", "Fitur telah tersedia pada aplikasi saat ini dan dapat digunakan tanpa perubahan pengembangan."],
    ["Manual", "Aktivitas bisnis dilakukan oleh pengguna di luar SFA atau merupakan interaksi lapangan tanpa otomasi sistem."],
    ["Customization", "Fitur baru atau perubahan perilaku aplikasi SFA Mobile yang membutuhkan pengembangan."],
    ["Integration", "Pertukaran atau pemrosesan data otomatis antara SFA Mobile dan CMS, serta kelanjutan dari CMS ke Odoo bila disebutkan."],
]
add_table(["Type", "Definisi"], legend_rows, [1.35, 4.53], 9, type_col=0)
add_body("Batas arsitektur: SFA Mobile tidak berkomunikasi langsung dengan Odoo. Seluruh komunikasi berlangsung melalui CMS sebagai bridge dan source of truth sesuai domain datanya.", bold_lead="Batas arsitektur:")

add_h1("Daftar Isi")
toc_items = [
    "1 Gambaran Umum Proyek", "2 Gambaran Umum Solusi", "3 Gambaran Fitur", "4 Alur Proses Bisnis",
    "P01A Registrasi & Aktivasi Pengguna Internal", "P01B Registrasi & Aktivasi Pengguna Eksternal",
    "P01C Login & Pengelolaan Akun", "P02 Dashboard & Ringkasan Kerja", "P03 Registrasi Customer",
    "P04 Profil Partner & Staff", "P05 Perencanaan Visit & Penjadwalan Ulang", "P06 Pelaksanaan Visit",
    "P07 Katalog Produk & Stok MITO", "P08 Sales Order Internal", "P09 Quotation Eksternal (Sell-In)",
    "P10 Pelacakan Penjualan", "P11 Pergerakan Stok Outlet & Opname", "P12 Penagihan Order & Collection",
    "P13 Aktivasi Garansi & Registrasi Sell-Out", "P14 Riwayat IMEI, Garansi & Reward", "P15 Katalog Reward & Klaim",
    "P16 Notifikasi", "P17 Mode Offline & Sinkronisasi", "P18 Approval Mobile",
    "5 Keputusan & Item Terbuka",
]
for item in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.15 if item.startswith("P") else 0)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(item)
    set_run_font(r, size=9.5, bold=not item.startswith("P"))

# Project overview.
add_h1("1 Gambaran Umum Proyek")
add_h2("1.1 Overview")
add_body("Blueprint ini mendefinisikan rancangan proses bisnis dan fitur utama aplikasi Sales Force Automation (SFA) Mobile MITO. Dokumen digunakan sebagai dasar review klien, fit-gap aplikasi yang tersedia, penyusunan estimasi effort, serta penyusunan desain fungsional dan teknis pada tahap berikutnya.")
add_h2("1.2 Tujuan")
add_bullets([
    "Menyediakan satu aplikasi mobile berbasis role untuk pengguna internal dan eksternal.",
    "Mendukung aktivitas lapangan Sales, Promotor/SPG, GTM, dan partner secara lebih terstruktur.",
    "Menjaga CMS sebagai bridge komunikasi antara SFA Mobile dan Odoo.",
    "Mendukung transaksi terpilih secara offline dengan antrean sinkronisasi yang aman.",
    "Menjadi dasar pemetaan Standard, Manual, Customization, dan Integration.",
])
add_h2("1.3 Ruang Lingkup")
add_table(["Area", "Ruang Lingkup"], [
    ["SFA Mobile", "Login, dashboard, customer/prospect, visit, produk, order, stock outlet, collection, IMEI/warranty, reward, notification, approval, dan offline synchronization."],
    ["CMS", "Autentikasi, role/access, master dan transaksi authoritative, approval matrix, validasi bisnis, integration staging, dan bridge ke Odoo."],
    ["Odoo", "Menerima Customer dan transaksi yang telah diproses CMS. Detail konfigurasi dan mapping Odoo dibahas dalam blueprint terpisah."],
    ["Di luar scope rinci", "Accounting journal, konfigurasi approval matrix di mobile, customer-level revenue target, dan desain teknis API/database."],
], [1.25, 4.63], 9)

add_h1("2 Gambaran Umum Solusi")
add_h2("2.1 Arsitektur Solusi")
arch = doc.add_table(rows=1, cols=5)
arch.style = "Table Grid"
arch.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_geometry(arch, [1.45, 0.42, 1.45, 0.42, 1.45])
for i, text in enumerate(["SFA MOBILE", "↔", "CMS", "↔", "ODOO"]):
    c = arch.rows[0].cells[i]
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    if i in (0, 2, 4):
        set_cell_shading(c, "D9EAF7" if i == 0 else "F2F2F2")
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_run_font(r, size=12 if i in (0, 2, 4) else 16, bold=True)
add_body("SFA Mobile berkomunikasi dua arah dengan CMS. CMS menangani validasi, hak akses, penyimpanan data authoritative, approval matrix, dan integrasi dua arah dengan Odoo. Tidak terdapat koneksi langsung antara SFA Mobile dan Odoo.")
add_h2("2.2 Peran Pengguna")
add_table(["Kelompok", "Peran", "Tanggung Jawab Utama"], [
    ["Internal", "Salesman", "Registrasi Customer, visit, Sales Order, collection, dan follow-up partner."],
    ["Internal", "GTM", "Registrasi Customer, pengembangan pasar, dan follow-up partner."],
    ["Internal", "Kacab", "Monitoring aktivitas cabang dan approval yang ditugaskan CMS."],
    ["Internal", "SPG", "Aktivitas outlet, IMEI/warranty, stock opname, dan collection bila diizinkan."],
    ["Eksternal", "Owner", "Profil partner, pengelolaan Staff, quotation, warranty, reward, dan stock outlet."],
    ["Eksternal", "Staff", "Quotation, warranty/IMEI, reward, penerimaan stok, dan stock opname sesuai role."],
], [0.85, 1.30, 3.73], 8.7)
add_body("Super Admin diposisikan sebagai aktor administrasi CMS/SFA, bukan sebagai role pengguna lapangan pada kelompok internal di atas.", italic=True)
add_h2("2.3 Prinsip Desain")
add_bullets([
    "Satu aplikasi digunakan pengguna internal dan eksternal dengan menu berbasis role.",
    "CMS menjadi source of truth untuk akses, approval matrix, dan data bisnis.",
    "Database mobile hanya menjadi cache dan pending-transaction queue.",
    "Blueprint berfokus pada business process; detail teknis dibahas terpisah.",
    "Proses lapangan menjadi prioritas utama; dashboard ditempatkan pada prioritas rendah.",
])

add_h1("3 Gambaran Fitur")
features = [
    ["SFA-01", "Login & Akses", "Semua pengguna", "Peningkatan", "Tinggi"],
    ["SFA-02", "Dashboard", "Salesman, Kacab, Super Admin", "Baru", "Rendah"],
    ["SFA-03", "Registrasi Customer", "Salesman, GTM, SPG", "Peningkatan", "Tinggi"],
    ["SFA-04", "Profil Partner & Staff", "Owner, Salesman", "Baru", "Sedang"],
    ["SFA-05", "Perencanaan Visit", "Salesman, Kacab", "Peningkatan", "Tinggi"],
    ["SFA-06", "Pelaksanaan Visit", "Salesman, SPG", "Peningkatan", "Tinggi"],
    ["SFA-07", "Katalog Produk & Stok MITO", "Internal dan Eksternal", "Peningkatan", "Tinggi"],
    ["SFA-08", "Sales Order Internal", "Salesman, Kacab", "Peningkatan", "Tinggi"],
    ["SFA-09", "Quotation Eksternal", "Owner, Staff", "Baru", "Tinggi"],
    ["SFA-10", "Pelacakan Penjualan", "Salesman, Kacab", "Peningkatan", "Sedang"],
    ["SFA-11", "Pergerakan Stok Outlet & Opname", "Owner, Staff, Salesman, SPG", "Baru", "Tinggi"],
    ["SFA-12", "Penagihan & Collection", "Salesman, SPG", "Peningkatan", "Tinggi"],
    ["SFA-13", "Aktivasi Garansi / Sell-Out", "Owner, Staff, SPG", "Baru", "Tinggi"],
    ["SFA-14", "Riwayat IMEI, Garansi & Reward", "Owner, Staff, Salesman", "Baru", "Sedang"],
    ["SFA-15", "Katalog Reward & Klaim", "Owner, Staff", "Baru", "Sedang"],
    ["SFA-16", "Notifikasi", "Semua pengguna", "Baru", "Sedang"],
    ["SFA-17", "Offline & Sinkronisasi", "Semua pengguna, Super Admin", "Baru", "Tinggi"],
    ["SFA-18", "Approval Mobile", "Salesman, Kacab", "Baru", "Tinggi"],
]
add_table(["ID", "Fitur", "Pengguna", "Posisi", "Prioritas"], features, [0.65, 1.75, 1.55, 0.85, 1.08], 8.2)

add_h1("4 Alur Proses Bisnis")
add_body("Bagian ini memuat activity flow pada level proses bisnis. P01A-P03 mengikuti hasil pembahasan yang telah direview; proses lainnya merupakan draft awal dan dapat disesuaikan pada sesi review berikutnya.")

P01A = [
    ["P01-INT-01", "Daftarkan Pengguna Internal", "Super Admin", "Super Admin membuat akun dan memilih salah satu role internal: Salesman, GTM, Kacab, atau SPG, termasuk assignment customer, outlet, atau territory bila diperlukan.", "Manual"],
    ["P01-INT-02", "Validasi Data Pengguna", "CMS", "Pada saat input, CMS memeriksa apakah username atau alamat email telah terdaftar.", "Integration"],
    ["P01-INT-03", "Aktifkan Akun Internal", "Super Admin", "Super Admin mengaktifkan akun internal yang telah valid dan memastikan role pengguna telah sesuai.", "Manual"],
    ["P01-INT-04", "Sediakan Informasi Aktivasi", "CMS", "CMS menyediakan informasi aktivasi serta instruksi pembuatan password kepada pengguna internal.", "Integration"],
    ["P01-INT-05", "Aktivasi Akses Internal", "Salesman / GTM / Kacab / SPG", "Pengguna internal membuat password dan mengaktifkan akses sesuai role yang telah ditentukan.", "Standard"],
]
add_process("P01A", "Registrasi & Aktivasi Pengguna Internal", "Registrasi internal digunakan untuk membuat akun Salesman, GTM, Kacab, dan SPG. Akun didaftarkan oleh Super Admin dan tidak menggunakan self-registration.", P01A, page_break=False)

P01B = [
    ["P01-EXT-01", "Mulai Self-Registration", "Owner", "Owner memulai registrasi mandiri sebagai calon Customer sekaligus pengguna utama pada SFA.", "Customization"],
    ["P01-EXT-02", "Lengkapi Data Customer dan User", "Owner", "Owner mengisi informasi usaha, alamat, segmentasi, dokumen pendukung, serta data akun Owner yang akan dihubungkan dengan Customer. OTP belum termasuk scope.", "Customization"],
    ["P01-EXT-03", "Kirim Self-Registration", "Owner", "Owner memeriksa kelengkapan data kemudian mengirim registrasi Customer dan User untuk diproses.", "Customization"],
    ["P01-EXT-04", "Validasi Data Registrasi", "CMS", "CMS memvalidasi data wajib serta memeriksa duplikasi Customer, username, dan alamat email.", "Integration"],
    ["P01-EXT-05", "Buat Customer dan User Terkait", "CMS", "CMS membuat satu record Customer dan satu User Owner yang saling terhubung dengan status menunggu review internal.", "Integration"],
    ["P01-EXT-06", "Review Registrasi Customer", "Salesman / GTM / Kacab", "Pengguna internal mereview informasi usaha, dokumen, dan User Owner kemudian menyetujui registrasi atau meminta revisi.", "Manual"],
    ["P01-EXT-07", "Revisi Data Registrasi", "Owner", "Owner memperbaiki data Customer atau User sesuai catatan review lalu mengirim ulang registrasi yang sama.", "Customization"],
    ["P01-EXT-08", "Aktifkan Customer dan User", "CMS", "Setelah disetujui, CMS mengaktifkan Customer beserta User Owner terkait dan meneruskan master Customer ke Odoo melalui integration staging.", "Integration"],
    ["P01-EXT-09", "Aktivasi Akses Owner", "Owner", "Owner membuat password dan mengaktifkan akses ke SFA sebagai User utama dari Customer yang telah disetujui.", "Standard"],
    ["P01-STF-01", "Daftarkan Staff", "Owner", "Owner mendaftarkan data Staff dan menentukan role. Hak akses mengikuti konfigurasi role yang telah ditetapkan pada SFA dan CMS.", "Customization"],
    ["P01-STF-02", "Validasi dan Hubungkan Staff", "CMS", "CMS memvalidasi kewenangan Owner, memeriksa duplikasi username atau email, lalu membuat User Staff yang terhubung dengan Customer milik Owner.", "Integration"],
    ["P01-STF-03", "Aktifkan Staff", "Owner", "Owner mengaktifkan atau menonaktifkan Staff tanpa approval pengguna internal.", "Customization"],
    ["P01-STF-04", "Aktivasi Akses Staff", "Staff", "Staff membuat password dan mengaktifkan akses pada organisasi serta role yang telah ditentukan Owner.", "Standard"],
]
add_process("P01B", "Registrasi & Aktivasi Pengguna Eksternal", "Owner melakukan self-registration yang menghasilkan Customer dan User Owner terkait. Setelah review internal, Customer dan User diaktifkan. Staff didaftarkan oleh Owner sebagai User tambahan pada Customer yang sudah ada tanpa approval internal.", P01B)

P01C = [
    ["P01-LOG-01", "Login ke SFA", "Pengguna Internal / Eksternal", "Pengguna memasukkan username atau email terdaftar dan password untuk mengakses SFA.", "Standard"],
    ["P01-LOG-02", "Autentikasi Pengguna", "CMS", "CMS memvalidasi credential, status akun, role, dan organisasi pengguna.", "Integration"],
    ["P01-LOG-03", "Sediakan Hak Akses", "CMS", "CMS menyediakan role, menu, dan assignment customer, dealer, outlet, atau territory kepada SFA.", "Integration"],
    ["P01-LOG-04", "Siapkan Akses Mobile", "SFA Mobile", "SFA menampilkan dashboard berbasis role dan menyiapkan data yang diizinkan untuk kebutuhan offline.", "Customization"],
    ["P01-LOG-05", "Akses SFA Offline", "Pengguna Internal / Eksternal", "Pengguna dapat menggunakan sesi lokal yang masih valid; login pertama dan autentikasi sesi kedaluwarsa wajib dilakukan online.", "Customization"],
    ["P01-LOG-06", "Ubah Password", "Pengguna Internal / Eksternal", "Pengguna mengajukan perubahan password dengan mengonfirmasi password saat ini dan memasukkan password baru sesuai kebijakan.", "Standard"],
    ["P01-LOG-07", "Perbarui Password", "CMS", "CMS memvalidasi permintaan dan memperbarui credential untuk akses berikutnya.", "Integration"],
    ["P01-LOG-08", "Logout dari SFA", "Pengguna Internal / Eksternal", "Pengguna mengakhiri sesi aktif sehingga akun harus login kembali untuk mengakses aplikasi.", "Standard"],
]
add_process("P01C", "Login & Pengelolaan Akun", "Flow ini digunakan bersama oleh seluruh role internal dan eksternal setelah akun aktif, mencakup login, akses offline, perubahan password, dan logout.", P01C)

P02 = [
    ["P02-DSH-01", "Sediakan Informasi Dashboard", "CMS", "CMS menyediakan ringkasan visit, order, revenue, stock outlet, dan aktivitas sesuai role dan scope data pengguna.", "Integration"],
    ["P02-DSH-02", "Review Aktivitas Penjualan", "Sales / Sales Manager", "Pengguna mereview aktual visit, order, dan revenue yang tersedia untuk memahami aktivitas penjualan.", "Customization"],
    ["P02-DSH-03", "Review Visit Conversion", "Sales / Sales Manager", "Pengguna mereview completed visit dengan order, tanpa order, dan Visit-to-Order Conversion.", "Customization"],
    ["P02-WRK-01", "Review Prioritas Harian", "Sales", "Sales mereview aktivitas hari ini dan pekerjaan tertunda untuk menentukan follow-up.", "Customization"],
    ["P02-WRK-02", "Review Prioritas Stock Outlet", "Sales / Sales Manager", "Pengguna mereview outlet dengan status Out of Stock, Low Stock, On Stock, atau Stock Opname Due.", "Customization"],
    ["P02-WRK-03", "Jadwalkan Visit dari Alert", "Sales", "Sales membuat jadwal visit dari kebutuhan follow-up stock; sistem tidak membuat visit otomatis.", "Customization"],
    ["P02-INT-01", "Review Integration Staging", "Super Admin", "Super Admin mereview transaksi Pending, Synced, dan Failed antara SFA dan CMS.", "Integration"],
]
add_process("P02", "Dashboard & Ringkasan Kerja", "Dashboard menyediakan ringkasan aktivitas dan prioritas kerja. Implementasinya ditempatkan sebagai prioritas rendah pada draft awal.", P02, ["Target revenue tahunan/bulanan per customer tidak termasuk minimum scope.", "Integration Staging hanya tersedia untuk Super Admin."])

P03 = [
    ["P03-CUS-01", "Daftarkan Customer dan User", "Salesman / GTM / SPG", "Pengguna internal mendaftarkan informasi Customer, segmentasi bisnis seperti Retail atau Pareto, Salesperson yang bertanggung jawab, dan data User Owner utama.", "Customization"],
    ["P03-CUS-02", "Validasi Data Customer dan User", "CMS", "CMS memvalidasi data wajib serta memeriksa duplikasi Customer, username, dan alamat email pada saat registrasi.", "Integration"],
    ["P03-CUS-03", "Buat Customer dan User Terkait", "CMS", "CMS membuat satu record Customer dan satu User Owner yang saling terhubung, termasuk hubungan dengan Salesperson dan segmentasi yang dipilih.", "Integration"],
    ["P03-CUS-04", "Integrasikan Master Customer", "CMS", "CMS meneruskan master Customer ke Odoo melalui integration staging. Master User tetap dikelola pada CMS dan SFA.", "Integration"],
    ["P03-CUS-05", "Sediakan Informasi Aktivasi", "CMS", "CMS menyediakan informasi aktivasi kepada User Owner yang didaftarkan oleh pengguna internal.", "Integration"],
    ["P03-CUS-06", "Aktivasi Akses Customer", "Owner", "Owner membuat password dan mengaktifkan akses ke SFA sebagai User utama dari Customer terkait.", "Standard"],
]
add_process("P03", "Registrasi Customer", "Salesman, GTM, atau SPG dapat mendaftarkan Customer beserta User Owner terkait. CMS membuat dan menghubungkan kedua record, kemudian hanya master Customer yang diteruskan ke Odoo.", P03, ["Master segmentasi, termasuk Retail, Pareto, dan kategori lain, dikelola di CMS.", "User Customer tetap dikelola pada CMS/SFA dan tidak dibuat sebagai user Odoo."])

P04 = [
    ["P04-PRF-01", "Review Profil Partner", "Dealer Owner", "Dealer Owner mereview profil usaha, data legal, alamat, outlet, dan dokumen partner yang aktif.", "Customization"],
    ["P04-PRF-02", "Ajukan Perubahan Profil", "Dealer Owner", "Dealer Owner mengajukan perubahan data atau dokumen; data aktif tetap digunakan selama proses review.", "Customization"],
    ["P04-PRF-03", "Distribusikan Permintaan Review", "CMS", "CMS memvalidasi kelengkapan dan mengarahkan permintaan kepada Internal Sales yang ditugaskan.", "Integration"],
    ["P04-PRF-04", "Review Perubahan Profil", "Internal Sales", "Internal Sales menyetujui, menolak dengan alasan, atau meminta revisi perubahan profil partner.", "Customization"],
    ["P04-PRF-05", "Terapkan Perubahan Profil", "CMS", "CMS menerapkan data yang disetujui sebagai profil aktif dan menyediakan hasil review kepada SFA.", "Integration"],
    ["P04-STF-01", "Kelola Staff Partner", "Dealer Owner", "Dealer Owner mendaftarkan, mengatur role, mengaktifkan, atau menonaktifkan staff tanpa approval Internal Sales.", "Customization"],
]
add_process("P04", "Profil Partner & Staff", "Proses ini mendukung pemeliharaan profil partner dengan review Internal Sales serta pengelolaan staff oleh Dealer Owner.", P04)

P05 = [
    ["P05-VPL-01", "Sediakan Jadwal Visit", "CMS", "CMS menyediakan jadwal visit berdasarkan assignment Sales dan customer/outlet.", "Integration"],
    ["P05-VPL-02", "Review Agenda Visit", "Sales", "Sales mereview agenda harian melalui date navigator dan memilih visit yang perlu dilakukan.", "Standard"],
    ["P05-VPL-03", "Buat Jadwal Visit", "Sales", "Sales membuat jadwal visit untuk customer atau outlet yang menjadi tanggung jawabnya.", "Standard"],
    ["P05-RSC-01", "Ajukan Reschedule", "Sales", "Sales mengajukan tanggal/waktu baru dan alasan perubahan jadwal.", "Customization"],
    ["P05-RSC-02", "Distribusikan Approval Reschedule", "CMS", "CMS menentukan approver berdasarkan approval matrix dan menyediakan permintaan pada approval inbox.", "Integration"],
    ["P05-RSC-03", "Putuskan Reschedule", "Sales Manager", "Sales Manager menyetujui atau menolak reschedule. Riwayat pengajuan tetap tercatat pada detail jadwal.", "Customization"],
    ["P05-RSC-04", "Perbarui Jadwal", "CMS", "Jika disetujui, CMS mengganti planned date/time dengan jadwal baru; jika ditolak jadwal lama tetap berlaku.", "Integration"],
]
add_process("P05", "Perencanaan Visit & Penjadwalan Ulang", "Proses mencakup penyusunan agenda visit dan perubahan jadwal dengan approval. Actual visit tetap mengikuti timestamp aktual.", P05, ["Selama reschedule masih pending, Sales tetap dapat visit pada tanggal usulan dan clock-in sesuai actual timestamp serta radius outlet."])

P06 = [
    ["P06-VEX-01", "Review Detail Visit", "Sales / Promotor", "Pengguna mereview customer, lokasi, tujuan, dan task visit yang ditugaskan.", "Standard"],
    ["P06-VEX-02", "Clock In Visit", "Sales / Promotor", "Pengguna melakukan clock in dengan actual timestamp dan validasi radius lokasi customer/outlet.", "Customization"],
    ["P06-VEX-03", "Laksanakan Visit", "Sales / Promotor", "Pengguna melakukan aktivitas penjualan, follow-up, pengecekan outlet, atau komunikasi dengan customer.", "Manual"],
    ["P06-VEX-04", "Catat Hasil Visit", "Sales / Promotor", "Pengguna mencatat outcome, catatan, foto bukti, komplain/follow-up, dan alasan tidak order bila tidak terjadi order.", "Customization"],
    ["P06-VEX-05", "Buat Order dari Visit", "Sales", "Jika terjadi order, Sales membuat Sales Order yang otomatis terhubung dengan Visit.", "Customization"],
    ["P06-VEX-06", "Clock Out & Selesaikan Visit", "Sales / Promotor", "Pengguna melakukan clock out; actual timestamp tetap mengikuti waktu transaksi sebenarnya.", "Customization"],
    ["P06-VEX-07", "Catat Penyelesaian Visit", "CMS", "CMS menerima hasil visit dan mempertahankan relasi Visit, Order, evidence, dan outcome.", "Integration"],
]
add_process("P06", "Pelaksanaan Visit", "Pelaksanaan visit menggunakan actual timestamp, validasi radius, evidence, outcome, dan hubungan Visit-to-Order.", P06)

P07 = [
    ["P07-PRD-01", "Sediakan Katalog dan Konteks Komersial", "CMS", "CMS menyediakan produk, gambar, kategori, harga, assortment, warehouse, dan stock MITO sesuai customer dan hak akses.", "Integration"],
    ["P07-PRD-02", "Review Katalog Produk", "Internal / External User", "Pengguna mencari dan mereview produk yang dapat dijual sesuai customer atau partner terpilih.", "Standard"],
    ["P07-PRD-03", "Pilih Warehouse", "Sales", "Sales menggunakan default warehouse customer/territory atau memilih warehouse lain jika memiliki kewenangan.", "Customization"],
    ["P07-PRD-04", "Review Stock MITO", "Internal / External User", "Pengguna melihat stock per warehouse terpilih tanpa agregasi antar-warehouse.", "Customization"],
    ["P07-PRD-05", "Scan Produk", "Internal / External User", "Pengguna dapat mencari produk melalui barcode scanner dengan pencarian manual sebagai fallback.", "Customization"],
]
add_process("P07", "Katalog Produk & Stok MITO", "Katalog menampilkan produk dan stok MITO berdasarkan konteks customer, warehouse, serta ketentuan komersial dari CMS.", P07)

P08 = [
    ["P08-SO-01", "Mulai Sales Order", "Sales", "Sales memilih satu Customer dan memulai order, termasuk dari detail Visit bila relevan.", "Customization"],
    ["P08-SO-02", "Susun Produk Order", "Sales", "Sales memilih beberapa produk, menentukan quantity, dan mereview cart sebagai satu Sales Order.", "Customization"],
    ["P08-SO-03", "Sediakan Harga, Discount & Tax", "CMS", "CMS menyediakan harga dan tax; Sales dapat mengisi line discount dalam batas role yang diizinkan.", "Integration"],
    ["P08-SO-04", "Simpan Draft Order", "Sales", "Sales menyimpan order yang belum final dan dapat mengubah atau membatalkannya sesuai akses.", "Standard"],
    ["P08-SO-05", "Konfirmasi Sales Order", "Sales", "Sales mengonfirmasi cart sebagai satu Sales Order untuk diproses lebih lanjut.", "Customization"],
    ["P08-SO-06", "Validasi & Proses Sales Order", "CMS", "CMS memvalidasi customer, produk, stock, harga, discount, tax, dan approval sebelum meneruskan transaksi ke Odoo.", "Integration"],
    ["P08-SO-07", "Review Status Order", "Sales / Sales Manager", "Pengguna mereview status, timeline, approval, atau alasan rejection pada Sales Order yang sama.", "Standard"],
]
add_process("P08", "Sales Order Internal", "Sales menyusun beberapa produk dalam cart dan mengonfirmasinya sebagai satu Sales Order. Perhitungan komersial final dilakukan CMS.", P08, ["Unit price dan tax tidak dapat diubah manual di SFA.", "Discount di atas batas role membutuhkan approval Sales Manager; desain detail masih menunggu review tim."])

P09 = [
    ["P09-QT-01", "Mulai Quotation", "External Partner", "Partner memilih produk dan quantity melalui konsep catalog-cart yang sama dengan Sales Order internal.", "Customization"],
    ["P09-QT-02", "Sediakan Ketentuan Komersial", "CMS", "CMS menyediakan harga, tax, product assortment, dan warehouse yang berlaku untuk partner.", "Integration"],
    ["P09-QT-03", "Konfirmasi Quotation", "External Partner", "Partner mengonfirmasi satu cart sebagai satu Quotation dan dapat menambahkan catatan atau attachment.", "Customization"],
    ["P09-QT-04", "Proses Sell-In Order", "CMS", "CMS memvalidasi Quotation, mencatatnya sebagai transaksi Sell-In, dan meneruskannya sebagai Sales Order internal ke Odoo.", "Integration"],
    ["P09-QT-05", "Review Status Quotation", "External Partner", "Partner memantau status dan hasil proses pada record Quotation yang sama tanpa modul tracking terpisah.", "Customization"],
]
add_process("P09", "Quotation Eksternal (Sell-In)", "Nama transaksi untuk partner eksternal adalah Quotation; transaksi tersebut merepresentasikan order dealer/outlet kepada MITO atau Sell-In.", P09)

P10 = [
    ["P10-TRK-01", "Sediakan Data Sales Tracking", "CMS", "CMS menyediakan agregat dan detail Sell-In, Sell-Out, order, customer, produk, dan Visit-to-Order.", "Integration"],
    ["P10-TRK-02", "Review Sell-In & Sell-Out", "Sales / Sales Manager", "Pengguna mereview ringkasan dan daftar transaksi per customer, produk, serta periode.", "Customization"],
    ["P10-TRK-03", "Review Visit Conversion", "Sales / Sales Manager", "Pengguna membandingkan completed visit dengan order dan tanpa order untuk melihat Visit-to-Order Conversion.", "Customization"],
    ["P10-TRK-04", "Review Detail Aktivitas", "Sales / Sales Manager", "Pengguna membuka detail Customer, Visit, atau Order dari ringkasan sesuai data-access scope.", "Standard"],
]
add_process("P10", "Pelacakan Penjualan", "Pelacakan penjualan menggunakan dashboard aggregate dengan drill-down daftar Sell-In, Sell-Out, dan Visit-to-Order.", P10, ["Satu Visit dengan beberapa order tetap dihitung sebagai satu Converted Visit.", "Cancelled, Missed, dan Rescheduled Visit tidak masuk denominator conversion."])

P11 = [
    ["P11-STK-01", "Review Stock Outlet", "Dealer / Sales / SPG", "Pengguna melihat On Hand per produk, status Out of Stock/Low Stock/On Stock, dan tanggal opname terakhir pada outlet yang diizinkan.", "Customization"],
    ["P11-STK-02", "Catat Penerimaan Stock", "Dealer Staff / Sales / SPG", "Pengguna mengonfirmasi penerimaan berdasarkan delivery/order reference atau mencatat penerimaan manual bila referensi tidak tersedia.", "Customization"],
    ["P11-STK-03", "Catat Movement IN", "CMS", "CMS membuat movement IN dan mencegah konfirmasi ganda untuk reference penerimaan yang sama.", "Integration"],
    ["P11-STK-04", "Catat Sell-Out", "CMS", "CMS membuat movement OUT ketika Warranty Activation/Sell-Out disetujui. Reward Claim tidak membuat OUT kedua.", "Integration"],
    ["P11-STK-05", "Laksanakan Stock Opname", "Dealer / Sales / SPG", "Pengguna membandingkan System On Hand dengan Counted Quantity pada outlet.", "Customization"],
    ["P11-STK-06", "Catat Adjustment Stock", "CMS", "CMS membuat Adjustment IN atau OUT sebesar selisih sehingga On Hand sama dengan Counted Quantity tanpa menghapus riwayat movement.", "Integration"],
    ["P11-STK-07", "Tindak Lanjut Stock Priority", "Sales", "Sales menjadwalkan visit dari alert Low Stock, Out of Stock, atau Stock Opname Due bila diperlukan.", "Customization"],
]
add_process("P11", "Pergerakan Stok Outlet & Opname", "CMS menyimpan On Hand authoritative berdasarkan movement penerimaan, Sell-Out, dan adjustment hasil stock opname.", P11, ["Buffer stock dan frekuensi opname dikonfigurasi per produk di CMS.", "Partial receipt menggunakan manual receipt dengan derived reference yang unik."])

P12 = [
    ["P12-COL-01", "Sediakan Invoice", "CMS", "CMS menyediakan order yang siap invoice, nomor invoice, status pembayaran, due date, dan PDF invoice kepada SFA.", "Integration"],
    ["P12-COL-02", "Review & Sampaikan Invoice", "Sales / SPG", "Pengguna mereview, mengunduh, mencetak, atau membagikan PDF invoice kepada customer.", "Standard"],
    ["P12-COL-03", "Lakukan Collection", "Sales / SPG", "Sales atau SPG melakukan penagihan dan menerima informasi atau bukti pembayaran dari customer.", "Manual"],
    ["P12-COL-04", "Catat Collection", "Sales / SPG", "Pengguna mencatat invoice, tanggal, jumlah, metode, reference, dan attachment wajib; transaksi dapat dikonfirmasi offline.", "Customization"],
    ["P12-COL-05", "Catat Pembayaran", "CMS", "CMS mencatat payment, menandai invoice Paid untuk SFA, dan mengelola sinkronisasi pembayaran ke Odoo.", "Integration"],
]
add_process("P12", "Penagihan Order & Collection", "SFA mendukung penyampaian invoice dan pencatatan collection tanpa scope accounting journal. Setelah collection dikonfirmasi, status SFA menjadi Paid.", P12, ["Status Pending Odoo Sync, Synced, atau Sync Failed hanya terlihat di CMS."])

P13 = [
    ["P13-WAR-01", "Pilih IMEI", "Dealer / SPG", "Pengguna memindai IMEI atau memasukkannya secara manual sebagai fallback.", "Customization"],
    ["P13-WAR-02", "Lengkapi Aktivasi Warranty", "Dealer / SPG", "Pengguna memilih produk, tanggal Sell-Out, data minimum pemilik warranty, attachment, dan reward yang eligible.", "Customization"],
    ["P13-WAR-03", "Konfirmasi Warranty Activation", "Dealer / SPG", "Pengguna mengonfirmasi aktivasi; konfirmasi offline menghasilkan status Pending Sync.", "Customization"],
    ["P13-WAR-04", "Validasi IMEI & Warranty", "CMS", "CMS memvalidasi format, produk, duplicate IMEI/Sell-Out, warranty eligibility, reward eligibility, dan ketersediaan reward.", "Integration"],
    ["P13-WAR-05", "Review Warranty Activation", "Internal Sales / Approver", "Approver menyetujui atau menolak aktivasi dan wajib memberikan alasan jika ditolak.", "Customization"],
    ["P13-WAR-06", "Aktifkan Warranty & Sell-Out", "CMS", "CMS mengaktifkan warranty, mencatat Sell-Out, dan membuat movement OUT stock outlet untuk IMEI yang disetujui.", "Integration"],
]
add_process("P13", "Aktivasi Garansi & Registrasi Sell-Out", "Aktivasi garansi merepresentasikan Sell-Out dealer/outlet kepada end customer sekaligus aktivasi warranty dan pemilihan reward.", P13)

P14 = [
    ["P14-HIS-01", "Sediakan Riwayat IMEI", "CMS", "CMS menyediakan riwayat IMEI sesuai dealer/customer dan access assignment.", "Integration"],
    ["P14-HIS-02", "Review Warranty & Reward", "Dealer / Internal Sales", "Pengguna mereview IMEI, produk, Sell-Out date, reward, submitter, status warranty, dan status Reward Claim secara terpisah.", "Customization"],
    ["P14-HIS-03", "Review Rejection", "Dealer / Internal Sales", "Pengguna melihat alasan rejection dan data yang perlu diperbaiki.", "Customization"],
    ["P14-HIS-04", "Kirim Ulang Aktivasi", "Dealer / SPG", "Pengguna memperbaiki data yang diizinkan dan mengirim ulang aktivasi yang ditolak.", "Customization"],
]
add_process("P14", "Riwayat IMEI, Garansi & Reward", "Riwayat IMEI dibatasi per dealer/customer dan menampilkan status warranty terpisah dari status Reward Claim.", P14)

P15 = [
    ["P15-RWD-01", "Sediakan Reward Eligible", "CMS", "CMS menyediakan reward yang eligible berdasarkan produk, IMEI, partner, dan ketentuan yang berlaku.", "Integration"],
    ["P15-RWD-02", "Pilih Reward", "Dealer / SPG", "Reward dipilih langsung saat Warranty Activation tanpa memilih program terpisah.", "Customization"],
    ["P15-CLM-01", "Ajukan Reward Claim", "Dealer / Partner", "Partner memilih IMEI dengan warranty Active dan status reward Eligible lalu mengonfirmasi claim tanpa attachment tambahan.", "Customization"],
    ["P15-CLM-02", "Validasi Reward Claim", "CMS", "CMS memastikan warranty Active dan IMEI belum pernah diklaim. Satu IMEI hanya dapat memiliki satu Reward Claim.", "Integration"],
    ["P15-CLM-03", "Catat & Kunci Claim", "CMS", "CMS mencatat claim yang valid, menguncinya dari klaim ganda, dan menyiapkan kebutuhan Vendor Bill bila reward bersifat payable.", "Integration"],
    ["P15-CLM-04", "Review Status Claim", "Dealer / Partner", "Partner memantau status Eligible, Pending Sync, Claimed, Processing, dan Completed pada claim yang sama.", "Customization"],
]
add_process("P15", "Katalog Reward & Klaim", "Reward dipilih saat Warranty Activation dan diklaim melalui proses terpisah setelah warranty Active. Tidak ada approval manual kedua.", P15, ["Detail mapping Vendor Bill dibahas pada blueprint CMS/Odoo."])

P16 = [
    ["P16-NTF-01", "Sediakan Notification", "CMS", "CMS menyediakan notification terkait visit, order, approval, invoice, account, IMEI/reward, dan pengumuman sistem.", "Integration"],
    ["P16-NTF-02", "Review Notification", "User", "Pengguna mereview notification yang belum dibaca dan membuka record terkait sesuai hak akses.", "Customization"],
    ["P16-NTF-03", "Tandai Notification Dibaca", "User", "Pengguna menandai notification sebagai telah dibaca.", "Customization"],
]
add_process("P16", "Notifikasi", "Notifikasi mengikuti pola in-app/push standar dan mengarahkan pengguna ke record bisnis terkait.", P16)

P17 = [
    ["P17-OFF-01", "Sediakan Data Offline", "CMS", "CMS menyediakan data yang diizinkan untuk disimpan sebagai cache lokal sesuai role dan assignment pengguna.", "Integration"],
    ["P17-OFF-02", "Laksanakan Aktivitas Offline", "User", "Pengguna melaksanakan visit atau aktivitas lapangan ketika koneksi tidak tersedia.", "Manual"],
    ["P17-OFF-03", "Konfirmasi Transaksi Offline", "User", "Pengguna dapat mengonfirmasi transaksi yang didukung sehingga tersimpan sebagai Pending Sync dengan local transaction ID unik.", "Customization"],
    ["P17-SYN-01", "Sinkronkan Transaksi", "CMS", "CMS menerima transaksi Pending, melakukan validasi akhir, dan mengembalikan status Synced atau Failed.", "Integration"],
    ["P17-SYN-02", "Tindak Lanjut Sync Failed", "User", "Pengguna melihat alasan kegagalan lalu melakukan Retry atau Edit & Resubmit sehingga transaksi kembali Pending.", "Customization"],
    ["P17-SYN-03", "Monitor Integration Staging", "Super Admin", "Super Admin memonitor transaksi Pending, Synced, dan Failed antara SFA dan CMS.", "Integration"],
]
add_process("P17", "Mode Offline & Sinkronisasi", "Database mobile berfungsi sebagai cache dan antrean transaksi, bukan source of truth. Final validation tetap dilakukan CMS.", P17, ["Error koneksi sementara tetap Pending dan dapat auto-retry.", "Failed digunakan untuk business validation atau permission error yang memerlukan tindak lanjut."])

P18 = [
    ["P18-APR-01", "Sediakan Approval Assignment", "CMS", "CMS menentukan approver dan level berdasarkan approval matrix yang tersimpan di CMS.", "Integration"],
    ["P18-APR-02", "Review Approval Inbox", "Sales / Sales Manager", "Approver mereview permintaan partner registration/profile, warranty/IMEI, Sales Order/discount, atau visit reschedule yang ditugaskan.", "Customization"],
    ["P18-APR-03", "Putuskan Approval", "Sales / Sales Manager", "Approver menyetujui, menolak dengan alasan, atau mengembalikan permintaan untuk revisi sesuai kewenangan.", "Customization"],
    ["P18-APR-04", "Proses Hasil Approval", "CMS", "CMS memperbarui status record bisnis dan menjalankan proses lanjutan sesuai hasil approval.", "Integration"],
]
add_process("P18", "Approval Mobile", "SFA hanya menampilkan dan mengeksekusi approval yang ditugaskan CMS. Approval matrix tidak dikonfigurasi atau disimpan secara authoritative di mobile.", P18, ["Reward Claim tidak memerlukan approval manual kedua."])

add_h1("5 Keputusan & Item Terbuka")
add_h2("5.1 Keputusan Utama")
add_bullets([
    "SFA Mobile berkomunikasi dengan CMS; CMS berkomunikasi dengan Odoo dua arah.",
    "Satu aplikasi digunakan pengguna internal dan eksternal dengan pengalaman berbasis role.",
    "Approval matrix disimpan dan dikonfigurasi di CMS.",
    "Offline Confirm menghasilkan Pending Sync; status sinkronisasi adalah Pending, Synced, dan Failed.",
    "Registrasi Customer dapat dilakukan melalui self-registration Owner atau pendaftaran oleh internal; kedua jalur menghasilkan Customer dan User Owner terkait di CMS.",
    "Outlet stock menggunakan movement IN/OUT dan adjustment hasil opname; On Hand disimpan authoritative di CMS.",
    "Warranty Activation menghasilkan Sell-Out dan movement OUT; Reward Claim tidak menghasilkan OUT kedua.",
    "Collection yang dikonfirmasi menampilkan Paid di SFA; status integrasi pembayaran ke Odoo hanya terlihat di CMS.",
])
add_h2("5.2 Item untuk Review Lanjutan")
open_items = [
    ["OI-01", "Discount & Tax", "Konfirmasi detail batas discount per role, global discount, dan rounding."],
    ["OI-02", "Segmentasi Prospect", "Finalisasi daftar master segmentasi selain contoh Retail dan Pareto."],
    ["OI-03", "Reward", "Finalisasi detail eligibility, fulfillment, exception, dan Vendor Bill mapping."],
    ["OI-04", "CMS/Odoo", "Detail endpoint, payload, retry, reconciliation, dan ownership data dibahas pada blueprint teknis/integrasi."],
    ["OI-05", "Prioritas", "Dashboard tetap low priority; urutan implementasi fitur lain dikonfirmasi setelah effort assessment."],
]
add_table(["ID", "Topik", "Catatan"], open_items, [0.75, 1.35, 3.78], 9)

# Keep automatic field refresh disabled during draft rendering; the PAGE field
# remains dynamic and is evaluated normally by Word without refreshing legacy
# template fields that no longer appear in the rewritten body.
settings = doc.settings._element
update = settings.find(qn("w:updateFields"))
if update is not None:
    settings.remove(update)

# Core properties.
doc.core_properties.title = "MITO SFA Mobile - Blueprint Draft V0.1"
doc.core_properties.subject = "Draft Blueprint Sales Force Automation Mobile"
doc.core_properties.author = "PT. Sinergi Karya Solusindo"
doc.core_properties.keywords = "MITO, SFA, Mobile, CMS, Odoo, Blueprint"

doc.save(OUT)
print(OUT)
