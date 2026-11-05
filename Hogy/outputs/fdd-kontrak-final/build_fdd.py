from pathlib import Path
import re
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
root=Path(r'E:/Panda/Hogy/outputs/konsep-kontrak')
out=Path(r'E:/Panda/Hogy/outputs/fdd-kontrak-final')
md=(root/'Konsep-Kontrak-Karyawan-HOGY.md').read_text(encoding='utf8')
d=Document()
def setup(s,land=False):
 s.orientation=WD_ORIENT.LANDSCAPE if land else WD_ORIENT.PORTRAIT
 s.page_width=Inches(11 if land else 8.5);s.page_height=Inches(8.5 if land else 11)
 s.left_margin=s.right_margin=Inches(.65);s.top_margin=s.bottom_margin=Inches(.6)
 s.header_distance=s.footer_distance=Inches(.25)
setup(d.sections[0])
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
 st=d.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
 st.font.size=Pt(11 if name=='Normal' else 21 if name=='Title' else 15 if name=='Heading 1' else 12)
 st.paragraph_format.space_after=Pt(7)
 st.paragraph_format.line_spacing=1.06
 if name.startswith('Heading'):st.paragraph_format.keep_with_next=True
footer=d.sections[0].footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=footer.add_run('HOGY  |  02-EMP  |  ');r.font.size=Pt(8)
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');footer._p.append(f)
def rich(p,t):
 for i,x in enumerate(re.split(r'\*\*(.*?)\*\*',t)):
  r=p.add_run(x.replace('<br>','\n'));r.bold=bool(i%2)
def para(t):
 p=d.add_paragraph();rich(p,t);return p
def table(data):
 n=len(data[0]);width=9.7 if d.sections[-1].orientation==WD_ORIENT.LANDSCAPE else 7.2
 widths=([.4,1.9,2.55,width-4.85] if n==4 else [1.25,2.9,width-4.15] if n==3 else [1.8,width-1.8])
 t=d.add_table(rows=0,cols=n);t.autofit=False
 for c,w in zip(t.columns,widths):c.width=Inches(w)
 for ri,row in enumerate(data):
  cells=t.add_row().cells
  for ci,(c,txt) in enumerate(zip(cells,row)):
   c.width=Inches(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   cp=c._tc.get_or_add_tcPr(); borders=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
   cp.append(borders)
   shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'203864' if ri==0 else 'F2F5F9' if ri%2 else 'FFFFFF');cp.append(shade)
   mar=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    e=OxmlElement('w:'+edge);e.set(qn('w:w'),'85');e.set(qn('w:type'),'dxa');mar.append(e)
   cp.append(mar)
   p=c.paragraphs[0];rich(p,txt)
   p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(2)
   for r in p.runs:r.font.size=Pt(9.5);r.font.color.rgb=RGBColor.from_string('FFFFFF' if ri==0 else '000000');r.bold=ri==0 or r.bold
   if ri==0:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  tr=t.rows[-1]._tr.get_or_add_trPr();tr.append(OxmlElement('w:cantSplit'))
  if ri==0:tr.append(OxmlElement('w:tblHeader'))
 d.add_paragraph().paragraph_format.space_after=Pt(1)
 return t
def block(text):
 lines=text.strip().splitlines();i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('|'):
   data=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    row=[x.strip() for x in lines[i].strip().split('|')[1:-1]]
    if not all(re.fullmatch(r'[-:]+',x) for x in row):data.append(row)
    i+=1
   table(data);continue
  if line.startswith('### '):d.add_heading(line[4:],2)
  elif line.startswith('## '):d.add_heading(line[3:],1)
  elif line.startswith('!['):
   alt,path=re.match(r'!\[(.*?)\]\((.*?)\)',line).groups()
   p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
   pic=p.add_run().add_picture(str(root/path),width=Inches(9.7))
   pic._inline.docPr.set('descr',alt)
  elif line.startswith('- '):rich(d.add_paragraph(style='List Bullet'),line[2:])
  else:para(line)
  i+=1

d.add_heading('Functional Design Document',0)
d.add_heading('Kontrak Karyawan HOGY',1)
table([['Informasi','Keterangan'],['Document ID','02-EMP'],['Project','HR dan Payroll PT. HOGY INDONESIA'],['Platform','Microsoft Dynamics 365 Finance and Operations'],['Tanggal','26 Oktober 2026'],['Versi','1.0'],['Basis konsep','MD Kontrak Karyawan HOGY versi 1.4'],['Prepared by','Krisna Prasetya'],['Status','Untuk review teknis']])
goal=md[md.index('## 1. Tujuan'):md.index('## 2. Alur penggunaan')]
block(goal)
d.add_page_break();d.add_heading('2. Alur penggunaan',1)
p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
pic=p.add_run().add_picture(str(root/'images/alur-kontrak-v1.png'),height=Inches(8.65));pic._inline.docPr.set('descr','Alur kontrak dengan dua decision berbentuk belah ketupat')
para('Decision menggunakan belah ketupat dan proses menggunakan kotak. Validasi mengikuti ketentuan pada bagian 5.')
setup(d.add_section(WD_SECTION_START.NEW_PAGE),True)
d.add_heading('3. Modification',1)
emp=md[md.index('### 3.1 Employees'):md.index('### 3.2 Employment history')]
cut=emp.index('Field yang ditampilkan')
block(emp[:cut]);d.add_page_break();para('Employees — Field pada subtab Payroll');block(emp[cut:])
hist=md[md.index('### 3.2 Employment history'):md.index('## 4. Perubahan kontrak')]
d.add_page_break()
cut=hist.index('Tampilkan field **Worker**')
block(hist[:cut]);d.add_page_break();para('Employment history — Header dan field Payroll')
hist=hist[cut:].replace('Table: ditetapkan pada FDD','Table: verifikasi metadata D365').replace('Nama table fisik, field teknis, dan EDT nominal final ditetapkan pada FDD setelah memeriksa metadata lingkungan D365.','Pemetaan table fisik, field teknis, dan EDT nominal final harus dikonfirmasi terhadap metadata lingkungan D365 sebelum implementasi.')
block(hist)
setup(d.add_section(WD_SECTION_START.NEW_PAGE),False)
changes=md[md.index('## 4. Perubahan kontrak'):md.index('## 5. Validasi dan hak akses')]
block(changes)
d.add_page_break();block(md[md.index('## 5. Validasi dan hak akses'):md.index('## 6. Referensi')])
block(md[md.index('## 6. Referensi'):].replace('Dokumen ini menjadi dasar pembahasan teknis dan penyusunan FDD kontrak karyawan.',''))
d.core_properties.title='FDD Kontrak Karyawan HOGY';d.core_properties.author='Krisna Prasetya'
for tree in [d.styles._element,d._element]:
 for border in tree.xpath('.//w:pBdr'):border.getparent().remove(border)
dest=out/'02-EMP_FDD_Kontrak_Karyawan_HOGY.docx';d.save(dest)
print(dest)
print('Embedded images:',len(d.inline_shapes),'Tables:',len(d.tables))
