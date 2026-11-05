from pathlib import Path
from docx import Document
from docx.shared import Pt,RGBColor
import re
root=Path(r'E:/Panda/Hogy/outputs')
mdpath=root/'konsep-kontrak/Konsep-Kontrak-Karyawan-HOGY.md'
fddroot=root/'fdd-kontrak-final'
d=Document(fddroot/'02-EMP_FDD_Kontrak_Karyawan_HOGY_v1.2.docx')
notes={
'Basic Salary':'Nominal gaji pokok individu. Sumber No. 1 (Sub Leader UP) dan No. 2 (Operator–Koordinator) menggunakan satu field. Nilai ditetapkan sesuai jabatan atau tabel gaji.',
'Fixed Transport Allowance':'Nominal transport tetap bulanan individu untuk Supervisor UP. Sumber No. 10. Jika seluruh nominal ditentukan tarif seragam per jabatan, sumber nilai menggunakan setting komponen gaji.',
'Position Allowance':'Nominal tunjangan jabatan individu untuk Adm Up. Sumber No. 20. Nominal ditetapkan sesuai jabatan.',
'Fixed Incentive':'Nominal incentive tetap bulanan individu untuk Operator–Koordinator berdasarkan tabel gaji. Sumber No. 21.',
'USD Allowance':'Nominal tunjangan USD tetap bulanan individu untuk Ekspatriat. Sumber No. 33.',
'Sales Incentive':'Nominal sales incentive tetap bulanan individu untuk Sales. Sumber No. 34. Jika pembayaran berdasarkan pencapaian, perhitungannya menggunakan komponen gaji.',
'Skill Allowance':'Nominal tunjangan skill individu untuk Translator/PJT. Sumber No. 35. Jika tarif seragam per skill, sumber nilai menggunakan setting komponen gaji.',
'Utility Operator Allowance':'Nominal tunjangan UO individu untuk Operator. Sumber No. 53. Jika tarif seragam bagi seluruh UO, sumber nilai menggunakan setting komponen gaji.'}
def setcell(c,txt):
 c.text=txt
 for p in c.paragraphs:
  p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(2)
  for r in p.runs:r.font.name='Arial';r.font.size=Pt(9.5);r.font.color.rgb=RGBColor(0,0,0)
for r in d.tables[2].rows[2:]:setcell(r.cells[3],notes[r.cells[1].text])
for r in d.tables[0].rows:
 if r.cells[0].text=='Versi':setcell(r.cells[1],'1.3')
 if r.cells[0].text=='Basis konsep':setcell(r.cells[1],'MD Kontrak Karyawan HOGY versi 1.5 dan Matriks Setup Komponen Gaji HOGY')
for p in d.paragraphs:
 if p.text.startswith('HOGY_Klasifikasi_Komponen_Kontrak_Payroll.xlsx'):
  p.text='Matriks-Setup-Komponen-Gaji-HOGY.md: penempatan 53 nomor sumber; 9 baris kontrak menjadi 8 jenis field nominal.'
dest=fddroot/'02-EMP_FDD_Kontrak_Karyawan_HOGY_v1.3.docx'
d.save(dest)

# Synchronize the concept with the latest reviewed FDD, including prior removals.
t=mdpath.read_text(encoding='utf8').replace('| Versi | 1.4 |','| Versi | 1.5 |')
removals=['Decision menggunakan belah ketupat','Tampilkan field **Worker** setelah **Company**','Field yang ditambahkan pada section Payroll dijabarkan','Semua field berikut berupa nominal bulanan','Kolom EDT mencantumkan sumber table']
t='\n'.join(line for line in t.splitlines() if not any(line.startswith(x) for x in removals))+'\n'
start=t.index('| No. | Field label | EDT | Catatan |',t.index('### 3.1 Employees'))
end=t.index('\n\n',start)
def mdtable(tab):
 rows=['| No. | Field label | EDT | Catatan |','|---:|---|---|---|']
 for r in tab.rows[1:]:rows.append('| '+' | '.join(c.text.replace('\n','<br>').replace('|','\\|') for c in r.cells)+' |')
 return '\n'.join(rows)
t=t[:start]+mdtable(d.tables[1])+t[end:]
start=t.index('| No. | Field label | EDT | Catatan |',t.index('### 3.2 Employment history'))
end=t.index('\n\n',start)
t=t[:start]+mdtable(d.tables[2])+t[end:]
t=t.replace('- HOGY_Klasifikasi_Komponen_Kontrak_Payroll.xlsx, hasil klasifikasi komponen tanggal 25 Oktober 2026.','- Matriks-Setup-Komponen-Gaji-HOGY.md: penempatan 53 nomor sumber; 9 baris kontrak menjadi 8 jenis field nominal.')
t=re.sub(r'\n{4,}','\n\n',t)
mdpath.write_text(t,encoding='utf8')
labels=[r.cells[1].text for r in d.tables[1].rows[1:]]
assert labels==list(notes)
assert [r.cells[1].text for r in d.tables[2].rows[2:]]==labels
assert d.tables[2].rows[1].cells[1].text=='Worker'
assert 'Decision menggunakan' not in t and 'verifikasi metadata D365' not in t
assert all((mdpath.parent/f).is_file() for f in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',t))
assert len(d.inline_shapes)==3
print('Synchronized MD 1.5 and FDD 1.3: eight nominal fields, Worker header, form names and matrix-based field notes.')
