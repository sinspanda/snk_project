from pathlib import Path
from html import escape
import re
root=Path(r'E:/Panda/Hogy/outputs/konsep-kontrak')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="1390" viewBox="0 0 1100 1390"><rect width="1100" height="1390" fill="white"/><defs><marker id="a" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#526579"/></marker></defs>']
def text(x,y,lines,size=18):
    for i,line in enumerate(lines):svg.append(f'<text x="{x}" y="{y+i*24}" text-anchor="middle" font-family="Arial" font-size="{size}" fill="#172B4D">{escape(line)}</text>')
def box(x,y,w,h,lines):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#EAF1FA" stroke="#234E79" stroke-width="2"/>');text(x+w/2,y+h/2-(len(lines)-1)*12+6,lines)
def diamond(x,y,w,h,label):
    svg.append(f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" fill="#FFF3D6" stroke="#9A6400" stroke-width="2.5"/>');text(x,y+6,[label],19)
def arrow(points):svg.append(f'<polyline points="{points}" fill="none" stroke="#526579" stroke-width="2" marker-end="url(#a)"/>')
# Explicit polygon decisions preserve the agreed notation in every Markdown viewer.
box(300,25,300,74,['HR Manager membuka','Employment history'])
diamond(450,205,270,140,'Jenis kebutuhan?');arrow('450,99 450,135')
box(75,365,270,65,['Buat kontrak baru']);box(555,365,270,65,['Pilih kontrak berjalan'])
arrow('315,205 210,205 210,365');text(190,260,['Kontrak awal /', 'Mutasi / Promosi / Demosi'],16)
arrow('585,205 690,205 690,365');text(790,255,['Adjustment nominal'],16)
box(75,470,270,65,['Isi periode kontrak']);arrow('210,430 210,470')
box(75,575,270,75,['Isi nominal pada','section Payroll']);arrow('210,535 210,575')
box(555,575,270,75,['Ubah nominal pada','section Payroll']);arrow('690,430 690,575')
box(300,720,300,65,['Validasi data'])
arrow('210,650 210,690 450,690 450,720');arrow('690,650 690,690 450,690 450,720')
diamond(450,895,220,140,'Data valid?');arrow('450,785 450,825')
box(755,860,290,70,['Tampilkan pesan validasi']);arrow('560,895 755,895');text(650,880,['Tidak'],17)
box(755,1020,290,75,['HR Manager','memperbaiki data']);arrow('900,930 900,1020')
arrow('1045,1057 1075,1057 1075,752 600,752')
box(300,1035,300,65,['Simpan kontrak']);arrow('450,965 450,1035');text(475,1005,['Ya'],17)
box(280,1150,340,75,['Tampilkan nominal secara','read-only pada Employees']);arrow('450,1100 450,1150')
box(280,1280,340,75,['Employee melihat kontrak','miliknya sendiri']);arrow('450,1225 450,1280')
svg.append('</svg>')
(root/'images/alur-kontrak-v1.svg').write_text(''.join(svg),encoding='utf8')
p=root/'Konsep-Kontrak-Karyawan-HOGY.md';t=p.read_text(encoding='utf8')
m=re.search(r'```mermaid\n(.*?)```',t,re.S);assert m
(root/'images/alur-kontrak-v1.mmd').write_text(m.group(1),encoding='utf8')
t=t[:m.start()]+'![Alur penggunaan kontrak dengan decision belah ketupat](images/alur-kontrak-v1.png)'+t[m.end():]
t=t.replace('| Versi | 1.2 |','| Versi | 1.3 |');p.write_text(t,encoding='utf8')
print('Updated Markdown to use fixed diagram image with two polygon decisions.')
