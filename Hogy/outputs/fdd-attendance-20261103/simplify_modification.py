from pathlib import Path
import zipfile,xml.etree.ElementTree as E
from xml.sax.saxutils import escape
folder=Path(__file__).parent
src=folder/'03-ATT_FDD_Absensi_Karyawan_HOGY_v1.1.docx'
out=folder/'03-ATT_FDD_Absensi_Karyawan_HOGY_v1.2.docx'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';q=lambda s:'{'+W+'}'+s
E.register_namespace('w',W)
with zipfile.ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
doc=E.fromstring(data['word/document.xml']);body=doc.find(q('body'))
tables=body.findall(q('tbl'))
def rows(i):return [[''.join(t.text or '' for t in c.iter(q('t'))) for c in r.findall(q('tc'))] for r in tables[i].findall(q('tr'))][1:]
# Reuse the existing document's table helper and paragraph styling.
scope={};code=(folder/'build.py').read_text(encoding='utf-8');exec(code[:code.index("b=title('Functional")],scope)
p=scope['p'];table=scope['table'];title=scope['title'];sub=scope['sub'];br=scope['br']
def label(t):return '<w:p><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="100"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t>'+escape(t)+'</w:t></w:r></w:p>'
b=title('3. Modification')+sub('3.1 Path menu')
b+=table(['Fitur','Path menu / lingkup'],[
('Jadwal / Roster (Profile Calendar)','Menu Profile Calendar yang digunakan pada environment HOGY. Compose, Upload Roster, tambah/edit manual dan tampilan roster berada pada fitur yang sama. Path lengkap dan ekstensi form dikonfirmasi teknis.'),
('Attendance Staging','Usulan: Human resources > Attendance > Attendance Staging. Form custom penampungan raw fingerprint.'),
('Employee Attendances','Usulan: Human resources > Attendance > Employee Attendances. Form custom hasil pengolahan staging.')],[2600,6760])
b+=sub('3.2 Flow')
b+='''<w:p><w:r><w:drawing><wp:inline xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><wp:extent cx="5943600" cy="4358640"/><wp:docPr id="900" name="Alur absensi HOGY"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="900" name="flow.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="rIdAttendanceFlow"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5943600" cy="4358640"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
b+=p('HR menyiapkan roster, lalu import fingerprint. Import hanya menyimpan Raw Text dan hasil parsing sebagai Pending. Process Attendance memvalidasi Pending, membaca jadwal, memeriksa duplikat, dan memilih punch-in paling awal serta punch-out paling akhir yang memenuhi rentang shift. Scan lain yang berbeda tetap menjadi sumber Processed; salinan scan yang sama menjadi Duplicate.')
b+=br()+sub('3.3 Field')+p('Kolom EDT menggunakan tipe data fungsional usulan. Nama EDT teknis, table, form, dan data entity dikonfirmasi teknis; bukan nama objek standar yang sudah dipastikan.')
def fieldtable(indices,extras=[]):
 rr=[]
 for i in indices:
  for row in rows(i):rr.append(row[1:])
 rr+=extras
 return table(['Field','EDT','Description / relasi / validasi'],rr,[2400,1800,5160])
b+=label('Jadwal / Roster (Profile Calendar)')
b+=fieldtable([3])
b+=p('Worker merujuk master worker dan legal entity. Profile merujuk master Profiles. Assignment tersimpan pada Profile Calendar worker/tanggal. Operational memerlukan roster eksplisit; Office dapat menggunakan Compose dan fallback yang diizinkan. Detail kosong tidak otomatis OFF. Profile operational harus memiliki detail weekday yang digunakan; S1 tidak otomatis menjadi S1F pada Jumat.')
b+=br()+label('Attendance Staging - header import')+fieldtable([6])
b+=label('Attendance Staging - detail transaksi')+fieldtable([8])
b+=p('Raw Text/Raw Data menyimpan baris asli. Parsing: Kode Mesin (2), Tahun (4), Bulan (2), Tanggal (2), Waktu HHmm (4), Kode Mesin Sumber (10), NPK (panjang dikonfirmasi), No Mesin (4 terakhir). Semua identitas disimpan sebagai teks untuk mempertahankan nol di depan. Contoh: 31 | 2026 | 07 | 01 | 0618 | 0000000000 | 0199 | 0024.')
b+=p('Saat import, kegagalan parsing dicatat pada pesan tanpa menghilangkan Raw Text; status tetap Pending. Saat Process Attendance, format/tanggal/jam invalid atau mapping NPK ambigu menghasilkan Error. NPK dipetakan ke Worker dan Legal Entity; referensi Employee Attendance diisi setelah proses berhasil. Usulan kunci duplikat: worker/NPK dalam konteks mapping + datetime scan + identitas mesin.')
b+=br()+label('Employee Attendances - identitas dan jadwal')+fieldtable([10])
b+=p('Worker merujuk master karyawan; Schedule Reference merujuk assignment Profile Calendar dan referensi revisi roster. Planned Shift, planned datetime, break, planned hours dan day type disimpan sebagai snapshot jadwal yang dipakai. Cegah duplikasi per legal entity, worker, work date dan kejadian shift.')
b+=br()+label('Employee Attendances - fingerprint dan aktual')+fieldtable([11])
b+=label('Employee Attendances - transaksi sumber')+table(['Field','EDT','Description / relasi / validasi'],[
('Staging Reference','Referensi staging','Relasi ke seluruh scan sumber; dapat berasal dari beberapa batch. Reprocess dapat membaca kembali scan Processed.'),('Finger Date Time / Machine','Datetime + teks','Mengikuti scan sumber. Tidak diubah melalui koreksi Actual.'),('Usage','Enum','Selected In, Selected Out, Other Scan.')],[2400,1800,5160])
b+=br()+label('Employee Attendances - status dan kontrol')+fieldtable([13])
b+=p('Finger In/Out read-only dari scan terpilih. Actual In/Out dapat dikoreksi HR dengan alasan dan audit nilai lama/baru. Actual Out tidak boleh sebelum Actual In; istirahat tidak negatif atau melebihi durasi pasangan. Pasangan belum lengkap tetap kosong pada sisi yang hilang dan menjadi exception. Shift lintas hari memakai datetime penuh; work date mengikuti assignment, dengan aturan shift mulai setelah tengah malam masih perlu konfirmasi.')
b+=br()+sub('3.4 Button')+label('Jadwal / Roster (Profile Calendar)')
b+=table(['Button','Proses / validasi'],[
('Compose','Membentuk jadwal periode Office dari pola mingguan. Hasil mengelola assignment Profile Calendar yang sama.'),
('Upload Roster','Membaca Worker, Work Date dan Shift Code, atau konversi matriks. Validasi worker, tanggal, profile, detail weekday/OFF dan bentrok. Tampilkan hasil dan perubahan sebelum Apply; penampungan internal tidak menjadi menu terpisah.'),
('Apply Roster','Tambah assignment baru; profile sama = Unchanged; berbeda = tampilkan old/new sebelum diterapkan; tanggal di luar file revisi tetap. Simpan user, waktu, alasan, jadwal lama/baru dan referensi upload.'),
('New / Edit','Tambah atau ubah assignment tanggal terkait, bukan master profile bersama. Tukar hari mengubah kedua tanggal. Perubahan attendance belum final menandai Need Reprocess. Data final/payroll terkunci tidak ditimpa otomatis.'),
('View Schedule Details / Export Excel','Tampilkan matriks worker x tanggal pada fitur yang sama, dengan filter bulan/tahun, department, worker dan profile group. Klik sel melihat jam, break, net hours dan sumber assignment. Bedakan shift, OFF, Schedule missing/setup error.')],[2400,6960])
b+=p('Pembacaan jadwal proses custom: individual > group > All > standard profile worker hanya bagi kelompok yang diizinkan. Operational tanpa roster = Schedule missing. Bekerja lembur ketika OFF tidak otomatis mengubah jadwal OFF; gunakan persetujuan lembur terkait. Perilaku cakupan dan resolver diverifikasi teknis.')
b+=br()+label('Attendance Staging')
b+=table(['Button','Proses / validasi'],[
('Import File','Simpan file/batch, nomor baris, Raw Text dan hasil parsing sebagai Pending. Bersihkan spasi untuk parsing tetapi pertahankan Raw Text asli. Lewati baris kosong. Belum melakukan validasi bisnis atau pairing.'),
('Process Attendance','Ambil Pending; validasi parsing, tanggal/jam, mapping karyawan dan jadwal efektif. Periksa scan yang sama dalam batch dan sumber sebelumnya: salinan = Duplicate. Tentukan punch masuk paling awal dan keluar paling akhir dalam rentang shift yang memenuhi aturan. Simpan/perbarui Employee Attendances dan relasi sumber sebelum menandai Processed. Kegagalan = Error beserta pesan; Pending lain tetap dapat diproses.'),
('Retry (usulan)','Setelah penyebab Error diperbaiki, HR mengembalikan baris ke Pending untuk Process Attendance. Tidak mengulang Processed/Duplicate secara otomatis.'),
('View Employee Attendance / View Errors','Buka attendance terkait atau filter baris gagal. Processed berarti scan telah ditautkan, bukan attendance sudah lengkap/final.')],[2400,6960])
b+=p('Range pairing sebelum/sesudah shift masih perlu disepakati. Satu scan tidak boleh menjadi In sekaligus Out atau digunakan pada dua shift tanpa aturan eksplisit. Scan tambahan untuk attendance Finalized ditahan untuk pemeriksaan; tidak mengubah hasil final.')
b+=br()+label('Employee Attendances')
b+=table(['Button','Proses / validasi'],[
('Process / Reprocess','Proses berbasis worker/periode dan jadwal untuk mencakup karyawan tanpa scan. Periksa OFF/cuti/izin/sakit sebelum menetapkan Absent. Reprocess membaca kembali scan terkait Processed dan Pending tambahan; tidak membuat duplikat, tidak menimpa koreksi manual, dan hanya berlaku sebelum Finalized. Perbarui snapshot serta hapus Need Reprocess setelah berhasil.'),
('Correct Attendance','HR mengubah Actual dengan alasan wajib. Catat nilai sebelum/sesudah, user dan waktu. Fingerprint serta Raw Text tetap. Setelah perubahan pada Reviewed, kembalikan Draft untuk review ulang.'),
('View Fingerprint Transactions','Tampilkan seluruh staging terkait beserta Usage dan mesin sumber.'),
('Mark as Reviewed','Catat reviewer dan waktu pemeriksaan; pastikan exception sudah ditindaklanjuti atau diputuskan beralasan.'),
('Finalize','Hanya HR berwenang. Tolak bila Need Reprocess aktif atau exception belum diselesaikan/diputuskan. Kunci hasil sebagai dasar payroll; perubahan berikutnya melalui mekanisme koreksi yang disetujui.')],[2400,6960])
b+=p('Jam lembur terdeteksi dan disetujui dipisahkan pada desain lembur. OT Before/After/Holiday, Fixed OT dan Total Index mengikuti FDD lembur setelah aturannya ditetapkan.')
children=list(body)
def txt(x):return ''.join(t.text or '' for t in x.iter(q('t')))
start=next(i for i,x in enumerate(children) if txt(x)=='3. Modification')
end=next(i for i,x in enumerate(children) if txt(x)=='4. Validasi dan hak akses')
old_prefix=[E.tostring(x) for x in children[:start]];old_suffix=[E.tostring(x) for x in children[end:]]
for x in children[start:end]:body.remove(x)
fragment=E.fromstring('<w:body xmlns:w="'+W+'">'+b+br()+'</w:body>')
for i,x in enumerate(list(fragment)):body.insert(start+i,x)
# Verify every unaffected body element is identical, then update cover revision only.
assert [E.tostring(x) for x in list(body)[:start]]==old_prefix
assert [E.tostring(x) for x in list(body)[-len(old_suffix):]]==old_suffix
for t in body.iter(q('t')):
 if t.text=='Draf 1.1':t.text='Draf 1.2'
data['word/document.xml']=E.tostring(doc,encoding='utf-8',xml_declaration=True)
R='http://schemas.openxmlformats.org/package/2006/relationships'
rels=E.fromstring(data['word/_rels/document.xml.rels'])
E.SubElement(rels,'{'+R+'}Relationship',Id='rIdAttendanceFlow',Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/image',Target='media/attendance-flow.png')
data['word/_rels/document.xml.rels']=E.tostring(rels,encoding='utf-8',xml_declaration=True)
data['word/media/attendance-flow.png']=(folder/'flow.png').read_bytes()
ct=E.fromstring(data['[Content_Types].xml']);C='http://schemas.openxmlformats.org/package/2006/content-types'
if not any(x.get('Extension')=='png' for x in ct):E.SubElement(ct,'{'+C+'}Default',Extension='png',ContentType='image/png')
data['[Content_Types].xml']=E.tostring(ct,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,d in data.items():
  if n.endswith('.xml'):E.fromstring(d)
  z.writestr(n,d)
headings=[txt(x) for x in fragment if x.find(q('pPr')+'/'+q('pStyle')) is not None]
assert headings==['3. Modification','3.1 Path menu','3.2 Flow','3.3 Field','3.4 Button'],headings
print('PASS: section 3 has four subsections; outside content preserved; flow image embedded; XML valid.')
print(out)
