from pathlib import Path
import json,re
base=Path(r'E:/Panda/Hogy')
rows=json.loads((base/'outputs/contract-payroll-20261025/source.json').read_text(encoding='utf8'))[4:]
contract={1,2,10,20,21,33,34,35,53};groups={3,7,38}
reasons={
1:'Nominal gaji pokok ditetapkan untuk individu.',
2:'Nominal hasil penetapan tabel gaji individu. Menggunakan satu field dengan No. 1.',
4:'Pembayaran mengikuti formula kehadiran.',
5:'Mengikuti rate dan kondisi pembayaran.',
6:'Nilai mengikuti kehadiran dan rate makan.',
8:'Rate umum dikalikan unit eligible.',
9:'Rate umum berdasarkan kondisi penerima.',
10:'Usulan nominal bulanan individu. Jika seragam per jabatan, gunakan komponen gaji.',
11:'Nilai mengikuti realisasi lembur.',
12:'Rate umum mengikuti shift aktual.',
13:'Nilai mengikuti penugasan aktual.',
14:'Nominal umum, dibayar berdasarkan pengajuan/upload.',
15:'Nominal umum, dibayar berdasarkan pengajuan/upload.',
16:'Pembayaran berdasarkan upload/kejadian, bukan nominal kontrak individu.',
17:'Nilai mengikuti kehadiran pada periode terkait.',
18:'Pembayaran berdasarkan pengajuan. Konfirmasi nominal tetap atau plafon.',
19:'Sumber menyebut formula. Jika nominal khusus individu, dapat dipindahkan ke kontrak.',
20:'Usulan nominal tunjangan jabatan individu.',
21:'Nominal tetap hasil penetapan tabel gaji individu.',
22:'Nominal umum untuk penerima yang eligible.',
23:'Nominal umum dengan kondisi keluarga terkait.',
24:'Rate umum; perlu konfirmasi per anak atau total.',
25:'Nominal umum untuk penerima sesuai kriteria.',
26:'Nilai merupakan hasil kalkulasi pajak.',
27:'Nilai mengikuti basis upah dan policy asuransi.',
28:'Nilai dihitung berdasarkan basis dan rule iuran.',
29:'Nilai dihitung per program dan porsi iuran.',
30:'Input nominal koreksi aktual melalui transaksi/upload.',
31:'Kalkulasi atau upload pada saat pembayaran bonus.',
32:'Pembayaran periode THR; sumber menyebut upload.',
33:'Usulan nominal tunjangan USD bulanan individu.',
34:'Mengikuti keterangan Fix/bln. Jika berdasarkan pencapaian, pindahkan ke komponen gaji.',
35:'Usulan nominal individu. Jika tarif seragam per skill, gunakan komponen gaji.',
36:'Hasil perhitungan berdasarkan saldo cuti yang diuangkan.',
37:'Input potongan aktual setiap bulan dari koperasi.',
39:'Perhitungan settlement berdasarkan kejadian keluar.',
40:'Perhitungan settlement berdasarkan alasan PHK.',
41:'Perhitungan settlement saat pensiun.',
42:'Perhitungan settlement saat pensiun dini.',
43:'Input/upload hasil kompensasi sesuai kejadian terkait.',
44:'Nilai mengikuti realisasi absen dan formula potongan.',
45:'Mekanisme perhitungan nilai proporsional.',
46:'Nilai mengikuti realisasi lembur dan formula.',
47:'Input potongan aktual berdasarkan data serikat.',
48:'Nilai mengikuti rule dan eligibility program terkait.',
49:'Koreksi perhitungan terkait periode asal.',
50:'Input/upload nilai aktual; bukan nominal bulanan kontrak.',
51:'Nominal umum dengan pemicu pembayaran/potongan yang perlu dikonfirmasi.',
52:'Input nominal approved. Jika substansinya dividen, arahkan ke proses finance.',
53:'Usulan nominal individu. Jika tarif seragam untuk seluruh UO, gunakan komponen gaji.'}
def label(r,n):
 text=next((r[i] for i in [3,2,1] if r[i]),'')
 text=re.sub(r'^\d+(?:\.\d+)*[. ]*','',text) if r[1] else re.sub(r'^[a-z]\.\s*','',text)
 if n in [8,9,10,11]:text='Transport '+text
 if n in [39,40,41,42]:text='Pesangon - '+text
 return text
def value(v):
 if v is None:return '—'
 if isinstance(v,(int,float)):return f'{v:,.0f}'.replace(',','.')
 return str(v).replace('|','\\|').replace('\n','<br>')
parts=['# Matriks Setup Komponen Gaji HOGY','',
'Matriks ini menentukan penempatan sumber nilai komponen pada kontrak individu atau komponen gaji payroll. Kolom Setup dan Alasan Setup merupakan usulan penempatan. Kolom Upah, Kriteria Posisi / Jabatan, Nilai, dan Fix Value / Formula mengikuti isi sumber.',
'', '## Matriks komponen','',
'| No. | Komponen | Upah | Kriteria Posisi / Jabatan | Nilai | Fix Value / Formula | Setup | Alasan Setup |',
'|---:|---|---|---|---|---|---|---|']
for i,r in enumerate(rows,1):
 assert r[0]==i
 setup='—' if i in groups else 'Kontrak' if i in contract else 'Komponen gaji'
 reason='Judul kelompok.' if i in groups else reasons[i]
 cells=[i,label(r,i),r[4],r[8],r[6],r[7],setup,reason]
 parts.append('| '+' | '.join(value(v) for v in cells)+' |')
parts+=['','## Ringkasan setup','',
'| Setup | Jumlah baris | Keterangan |','|---|---:|---|',
'| Kontrak | 9 | Menjadi 8 jenis field karena No. 1 dan 2 menggunakan satu field Basic Salary. |',
'| Komponen gaji | 41 | Termasuk rate umum, formula, serta input transaksi/upload payroll. |',
'| Judul kelompok | 3 | No. 3 Tunjangan, No. 7 Transport, dan No. 38 Pesangon. |',
'| Total | 53 | Terdiri dari 50 komponen detail dan 3 judul kelompok. |','',
'## Ketentuan pembacaan','',
'- Setup menunjukkan tempat sumber nilai. Komponen yang nominalnya disimpan di kontrak tetap direferensikan oleh komponen payroll saat perhitungan gaji.',
'- Kriteria posisi/jabatan menentukan kelompok penerima; tidak otomatis menentukan bahwa nominal harus disimpan di kontrak.',
'- Nominal khusus individu ditempatkan di kontrak. Nominal/rate umum, tabel, formula, dan transaksi aktual ditempatkan pada komponen gaji.',
'- Status tetap atau tidak tetap menurut kebijakan HOGY berbeda dari penempatan sumber nilai pada matriks ini.',
'- Kolom Upah disalin dari sumber. Maknanya tidak diasumsikan sebagai penanda dasar pajak.',
'- Kriteria pada matriks perlu dibaca bersama kolom Keterangan di sumber; tulisan All empoloyee tidak selalu berarti seluruh karyawan menerima komponen.',
'- Tanda — menunjukkan kolom sumber kosong atau baris judul kelompok.',
'','## Referensi','',
'Salary Componen (Penjelasan).xlsx, sheet Sheet1, range A5:J57. Nomor mengikuti kolom NO sumber; nama komponen pada baris turunan diberi konteks Transport/Pesangon agar dapat dibaca mandiri.','']
dest=base/'outputs/Matriks-Setup-Komponen-Gaji-HOGY.md'
dest.write_text('\n'.join(parts),encoding='utf8')
text=dest.read_text(encoding='utf8')
ids=[int(x) for x in re.findall(r'^\| (\d+) \|',text,re.M)]
assert ids==list(range(1,54))
assert sum(i in contract for i in ids)==9
assert len(ids)-len(groups)-len(contract)==41
assert len(reasons)==50
print(dest)
print('Verified 53 numbered rows, 9 contract candidates, 41 payroll components and 3 group headings.')
