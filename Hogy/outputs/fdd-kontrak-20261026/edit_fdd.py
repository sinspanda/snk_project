from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from pathlib import Path

out=Path(r'E:/Panda/Hogy/outputs/fdd-kontrak-20261026')
source=Path(r'C:/Users/SAYID/OneDrive/02. Project/HOGY/04. Development/HR Payroll/02-EMP-Kontrak Karyawan.docx')
d=Document(source)
# Reuse the source style definitions; remove unrelated POS content and screenshots.
body=d._element.body
for e in list(body):
    if e.tag!=qn('w:sectPr'): body.remove(e)
sec=d.sections[0]
sec.page_width=Inches(8.27); sec.page_height=Inches(11.69)
sec.top_margin=sec.bottom_margin=Inches(.65)
sec.left_margin=sec.right_margin=Inches(.7)
for part in (sec.header,sec.footer):
    for el in list(part._element):part._element.remove(el)
normal=d.styles['Normal']; normal.font.name='Arial';normal.font.size=Pt(10)
normal.paragraph_format.space_after=Pt(6)
normal.paragraph_format.line_spacing=1.05
for name in ['Title','Heading 1','Heading 2','Heading 3']:
    if name not in d.styles:d.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
    st=d.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
    st.font.size=Pt(20 if name=='Title' else 14 if name=='Heading 1' else 11)
    st.paragraph_format.space_before=Pt(10);st.paragraph_format.space_after=Pt(6)
    st.paragraph_format.keep_with_next=True
if 'Subtitle' not in d.styles:d.styles.add_style('Subtitle',WD_STYLE_TYPE.PARAGRAPH)
def p(t='',style=None):return d.add_paragraph(t,style)
def h(t):d.add_heading(t,1)
def sub(t):d.add_heading(t,2)
def page():d.add_page_break()
def table(headers,rows,widths):
    t=d.add_table(rows=1, cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for c,w in zip(t.columns,widths):c.width=Inches(w)
    for i,x in enumerate(headers):t.rows[0].cells[i].text=x
    repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
    for row in rows:
        for c,x in zip(t.add_row().cells,row):c.text=str(x)
    for ri,r in enumerate(t.rows):
        pr=r._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
        for ci,c in enumerate(r.cells):
            c.width=Inches(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cp=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
            cp.append(b)
            margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                e=OxmlElement('w:'+side);e.set(qn('w:w'),'75');e.set(qn('w:type'),'dxa');margins.append(e)
            cp.append(margins)
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'203864' if ri==0 else 'F1F4F8' if ri%2 else 'FFFFFF');cp.append(shade)
            for para in c.paragraphs:
                para.paragraph_format.space_after=Pt(3);para.paragraph_format.space_before=Pt(2)
                if ri==0:para.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for run in para.runs:
                    run.font.name='Arial';run.font.size=Pt(9)
                    run.bold=ri==0;run.font.color.rgb=RGBColor.from_string('FFFFFF' if ri==0 else '000000')
    p()
    return t

p('Functional Design Document','Title')
p('Kontrak Karyawan dan Komponen Gaji Tetap','Subtitle')
p('D365 Finance and Operations\nPT. HOGY INDONESIA')
p('Document ID: 02-EMP\nVersi: 1.1\nTanggal revisi: 26 Oktober 2026\nPrepared by: Krisna Prasetya')
h('Revision and Sign off Sheet')
table(['Tanggal','Versi','Perubahan'],[['26 Oktober 2026','1.1','Penambahan field nominal komponen gaji tetap individu pada Position Assignment di Work History Worker atau Employee. Isi template POS diganti sesuai ruang lingkup kontrak karyawan HOGY.']],[1.1,.6,5.1])
sub('Approvers')
table(['Peran','Nama','Persetujuan dan tanggal'],[['HOGY HR / Payroll','',''],['Project Manager','','']],[2,2,2.8])
sub('Document Properties')
p('Ruang lingkup: field nilai gaji tetap individu, histori berdasarkan tanggal berlaku, pembacaan oleh payroll, validasi, dan skenario pengujian. Nama field teknis di dokumen ini adalah usulan extension HOGY dan perlu mengikuti konvensi pengembangan proyek.')
page()
h('Introduction')
sub('Background')
p('HOGY memerlukan pencatatan nominal gaji tetap yang melekat pada masing-masing karyawan. Nominal tersebut menjadi sumber nilai bagi payroll dan harus dapat ditelusuri berdasarkan periode penugasan serta tanggal mulai berlakunya perubahan.')
sub('Purpose')
p('Menambahkan kelompok field Fixed Salary Components pada Position Assignment yang diakses dari Work History pada Worker atau Employee. Nilai dicatat pada penugasan individu, bukan pada master Position yang dapat dipakai oleh karyawan lain.')
sub('Audience')
p('HOGY HR dan Payroll, konsultan fungsional, developer D365, serta tim pengujian.')
h('Justification')
sub('Target Penempatan')
p('Worker / Employee > Work History > Position Assignment > Fixed Salary Components. Jalur ini merupakan target penempatan desain HOGY. Nama menu mengikuti tampilan dan konfigurasi lingkungan D365 yang digunakan.')
p('Kelompok field nominal merupakan extension HOGY pada konteks Position Assignment. Dokumen ini tidak menyatakan bahwa seluruh field nominal tersebut tersedia secara standard D365.')
sub('Batasan Ruang Lingkup')
p('Nilai umum dan formula seperti makan, transport harian, shift, perumahan, keluarga, anak, pajak, dan iuran tetap dikelola pada komponen payroll. Pengajuan, koreksi, bonus, dan settlement menggunakan transaksi payroll sesuai prosesnya.')
p('Basic Salary untuk Sub Leader UP dan Operator sampai Koordinator menggunakan satu field Basic Salary. Perbedaan kelompok digunakan saat penetapan nominal, bukan membuat dua pembayaran basic salary.')
sub('Considerations')
p('Payroll membaca satu sumber resmi per komponen. Apabila Basic Salary juga dikelola pada Fixed Compensation, proyek harus menetapkan arah sinkronisasi agar dua nominal tidak dapat dipelihara secara independen. Sales Incentive termasuk rancangan field sementara sampai sifat tetap bulanannya dikonfirmasi.')
page()
h('Modification Description')
sub('Position Assignment pada Work History')
p('Tambahkan kelompok Fixed Salary Components. Semua nominal berikut merupakan nilai bulanan sebelum prorate. Basic Salary wajib untuk assignment yang menjadi sumber payroll. Komponen lain diisi sesuai hak individu, dengan nilai 0 bila tidak diberikan.')
table(['No','Field Label','EDT / Type usulan','Note'],[
['1','Basic Salary','Amount / decimal\nHogyBasicSalary','Satu nominal gaji pokok individu. Penetapan mengikuti jabatan atau tabel gaji. Tidak boleh ada dua sumber basic salary aktif untuk cakupan payroll yang sama.'],
['2','Fixed Transport Allowance','Amount / decimal\nHogyFixedTransport','Nominal transport tetap bulanan individu. Berbeda dari transport yang mengikuti kehadiran atau lembur.'],
['3','Position Allowance','Amount / decimal\nHogyPositionAllowance','Nominal tunjangan jabatan individu. Jika seluruh nilai ditentukan dari tabel jabatan, sumber nilai dapat dialihkan ke tabel payroll setelah keputusan HOGY.'],
['4','Fixed Incentive','Amount / decimal\nHogyFixedIncentive','Nominal incentive tetap bulanan sesuai tabel gaji atau penetapan individu. Bukan perhitungan pencapaian target.'],
['5','USD Allowance','Amount / decimal\nHogyUsdAllowance','Nominal bulanan dalam USD untuk penerima yang eligible. Nilai tidak dijumlahkan langsung dengan nominal IDR.'],
['6','Sales Incentive','Amount / decimal\nHogySalesIncentive','Field sementara, perlu konfirmasi. Gunakan hanya jika hak individu berupa nominal tetap bulanan. Jika berbasis target, kelola melalui formula payroll.'],
['7','Skill Allowance','Amount / decimal\nHogySkillAllowance','Nominal tunjangan Translator / PJT individu selama assignment berlaku. Jika tarif seragam per skill, pertimbangkan tabel payroll.'],
['8','Utility Operator Allowance','Amount / decimal\nHogyUoAllowance','Nominal UO individu selama assignment berlaku. Jika tarif seragam bagi seluruh UO, pertimbangkan master rate payroll.']
],[.3,1.35,1.6,3.55])
p('Currency nominal selain USD Allowance mengikuti currency remunerasi yang ditetapkan untuk employment/legal entity. USD Allowance menggunakan USD. Currency tidak boleh diasumsikan hanya dari lokasi perusahaan.')
page()
h('Aturan Penggunaan Field')
table(['Area','Ketentuan'],[
['Konteks individu','Nilai terikat pada Worker, employment/legal entity, dan Position Assignment. Tidak menyimpan nilai pada master Position bersama.'],
['Tanggal berlaku','Gunakan tanggal berlaku assignment sebagai konteks. Bila nilai berubah tanpa perubahan posisi, buat versi nilai bertanggal berlaku dalam assignment yang sama. Histori sebelumnya tetap tersimpan.'],
['Validasi periode','Tolak overlap versi nilai untuk assignment dan cakupan komponen yang sama. Perubahan tanggal tidak boleh menghilangkan histori payroll.'],
['Banyak assignment','Jika worker memiliki beberapa assignment aktif, tentukan assignment sumber payroll atau alokasi yang disetujui. Jangan menjumlahkan seluruh Basic Salary secara otomatis.'],
['Akses dan perubahan','HR/Compensation yang berwenang memelihara nominal sesuai legal entity. Payroll membaca nominal. Catat pengguna, waktu, tanggal berlaku, dan alasan perubahan.'],
['Pembacaan payroll','Ambil versi nilai yang berlaku untuk periode terkait. Jika ada perubahan tengah periode, gunakan aturan segmentasi/prorate payroll yang disepakati.'],
['Payroll final','Perubahan nominal tidak mengubah hasil payroll yang telah final. Perubahan retroaktif masuk proses rapel/koreksi yang disetujui.'],
['Nilai dan currency','Nominal tidak negatif. Nilai 0 berarti tidak menerima komponen. Currency wajib diketahui sebelum payroll. Kurs, tanggal kurs, dan pembulatan USD mengikuti setup payroll.']
],[1.25,5.55])
sub('Error Handling')
p('Tampilkan pesan validasi bila Basic Salary wajib belum diisi, nominal negatif, periode bertumpang tindih, currency belum ditentukan, atau assignment sumber payroll belum jelas. Tolak perubahan tanpa hak akses. Jika nilai payroll belum tersedia, hentikan kalkulasi komponen terkait dan tampilkan penyebabnya; jangan otomatis mengganti nilai yang hilang menjadi 0.')
sub('Komponen di Luar Field Kontrak')
p('Perumahan 60.000, Keluarga 60.000, Anak 40.000, dan Keluarga Janda 40.000 menggunakan master nominal serta eligibility pada payroll sesuai sumber. Nominal khusus individu hanya ditambahkan ke rancangan kontrak bila HOGY mengonfirmasi adanya pengecualian.')
page()
h('Test Scripts')
table(['ID','Skenario','Expected Result'],[
['EMP-01','Input Basic Salary 5.000.000 dan Fixed Transport 500.000 pada assignment sumber payroll.','Payroll bulan penuh membaca nilai 5.000.000 dan 500.000 dari versi assignment yang berlaku. Angka merupakan data uji.'],
['EMP-02','Karyawan tidak menerima Skill Allowance dan UO.','Field bernilai 0; payroll tidak membentuk pembayaran kedua komponen tersebut.'],
['EMP-03','Ubah nominal dengan tanggal berlaku baru tanpa mengubah posisi.','Versi lama tetap tersedia; payroll membaca versi sesuai tanggal. Tidak perlu membuat perpindahan posisi fiktif.'],
['EMP-04','Buat periode nilai yang overlap pada assignment yang sama.','Sistem menolak penyimpanan dan menjelaskan periode yang bertabrakan.'],
['EMP-05','Worker mempunyai dua assignment aktif.','Payroll memakai sumber/alokasi yang ditetapkan. Jika belum jelas, kalkulasi dihentikan dan tidak menggandakan Basic Salary.'],
['EMP-06','Input USD Allowance 100 dengan currency USD.','Nilai tetap disimpan sebagai USD 100; konversi mengikuti setup payroll. Tidak dijumlah langsung dengan nominal currency lain.'],
['EMP-07','Ubah nilai setelah payroll periode lalu final.','Hasil final tetap; koreksi retroaktif mengikuti proses rapel yang disetujui.'],
['EMP-08','Akses melalui pengguna tanpa kewenangan atau legal entity lain.','Pengguna tidak dapat melihat/mengubah nominal di luar kewenangan.'],
],[.65,2.7,3.45])
sub('Keputusan yang Perlu Dikonfirmasi')
p('1. Sumber resmi Basic Salary dan hubungan dengan Fixed Compensation.\n2. Sales Incentive benar tetap bulanan atau berbasis pencapaian.\n3. Position Allowance, Skill Allowance, dan UO berupa nominal individu atau tarif seragam.\n4. Mekanisme versi nilai, approval perubahan, sumber payroll saat banyak assignment, dan aturan perubahan tengah periode.\n5. Currency remunerasi serta aturan konversi USD.')
p('Referensi komponen: Salary Componen (Penjelasan).xlsx, Sheet1, No. 1, 2, 10, 20, 21, 33, 34, 35, dan 53. Basic Salary pada No. 1 dan 2 digabung sebagai satu field.')
d.core_properties.title='Kontrak Karyawan dan Komponen Gaji Tetap'
d.core_properties.subject='HOGY Position Assignment Work History'
d.core_properties.author='Krisna Prasetya'
path=out/'02-EMP-Kontrak Karyawan_Revisi_Position_Assignment.docx'
d.save(path)
print(path)
print('Tables:',len(d.tables),'Field rows:',len(d.tables[3].rows))
