from pathlib import Path
from copy import deepcopy
from hashlib import sha256
from zipfile import ZipFile
import json, math
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.section import WD_SECTION_START,WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image,ImageDraw,ImageFont
root=Path(r'E:/Panda/Hogy/outputs/fdd-data-reformat')
ref=Path(r'E:/Panda/Hogy/outputs/fdd-kontrak-final/02-EMP_FDD_Kontrak_Karyawan_HOGY_v1.3.docx')
src=Document(r'E:/Panda/Hogy/FDD/07-EMP- Data Karyawan MSD 365.docx')
d=Document(ref)
body=d._element.body
for node in list(body):
 if node.tag!=qn('w:sectPr'):body.remove(node)
# Preserve source styles, table formatting and all package parts by working from the reference.
meta_proto=deepcopy(Document(ref).tables[0]._tbl)
field_proto=deepcopy(Document(ref).tables[1]._tbl)
valid_proto=deepcopy(Document(ref).tables[4]._tbl)
from docx.table import Table

def setup(s,land=False):
 s.orientation=WD_ORIENT.LANDSCAPE if land else WD_ORIENT.PORTRAIT
 s.page_width=Inches(11 if land else 8.5);s.page_height=Inches(8.5 if land else 11)
 s.left_margin=s.right_margin=Inches(.65);s.top_margin=s.bottom_margin=Inches(.6)
 s.header_distance=s.footer_distance=Inches(.25)
setup(d.sections[0])
for s in d.sections:
 for p in s.footer.paragraphs:
  for r in p.runs:
   if '02-EMP' in r.text:r.text=r.text.replace('02-EMP','FDD-HR-SPICY')

def para(txt='',style=None):
 p=d.add_paragraph(txt,style)
 return p

def heading(txt,level=1):return d.add_heading(txt,level)

def setcell(c,text,head=False):
 p=c.paragraphs[0]
 for child in list(p._p):
  if child.tag!=qn('w:pPr'):p._p.remove(child)
 p.add_run(str(text))
 for extra in list(c._tc)[1:]:
  if extra.tag==qn('w:p') and extra is not p._p:c._tc.remove(extra)
 for r in p.runs:
  r.font.name='Arial';r.font.size=Pt(9.5);r.font.color.rgb=RGBColor.from_string('FFFFFF' if head else '000000');r.bold=head
 p.paragraph_format.space_before=Pt(2);p.paragraph_format.space_after=Pt(3)
 p.paragraph_format.keep_with_next=False
 if head:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 else:p.alignment=WD_ALIGN_PARAGRAPH.LEFT

def table(rows,proto,widths=None):
 node=deepcopy(proto);d._element.body.insert(len(d._element.body)-1,node)
 t=Table(node,d._body)
 head=deepcopy(t.rows[0]._tr);item=deepcopy(t.rows[1]._tr)
 for tr in list(node.findall(qn('w:tr'))):node.remove(tr)
 for ri,row in enumerate(rows):
  tr=deepcopy(head if ri==0 else item);node.append(tr)
  for ci,c in enumerate(t.rows[-1].cells):
   setcell(c,row[ci],ri==0)
   pr=c._tc.get_or_add_tcPr();shd=pr.find(qn('w:shd'))
   if shd is not None:shd.set(qn('w:fill'),'203864' if ri==0 else 'F2F5F9' if ri%2 else 'FFFFFF')
  if ri==0:
   trpr=tr.get_or_add_trPr()
   if trpr.find(qn('w:tblHeader')) is None:trpr.append(OxmlElement('w:tblHeader'))
 if widths:
  t.autofit=False
  for c,w in zip(t.columns,widths):c.width=Inches(w)
  for row in t.rows:
   for c,w in zip(row.cells,widths):c.width=Inches(w)
 para().paragraph_format.space_after=Pt(1)
 return t

# Exact reference evidence and allowed body replacements.
with ZipFile(ref) as z:
 inventory={n:{'size':len(z.read(n)),'sha256':sha256(z.read(n)).hexdigest()} for n in z.namelist()}
(root/'reference-package-inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf8')
(root/'artifact.md').write_text(f'''# Reference contract\nReference: {ref}\nSHA256: {sha256(ref.read_bytes()).hexdigest()}\nReference QA: reference-contact.png, retained qa-v1.3.pdf (8 pages).\nPage system: US Letter portrait 8.5 x 11 in; landscape 11 x 8.5 in. Left/right margins .65 in; top/bottom .6 in; header/footer .25 in. Portrait then landscape then portrait.\nTypography: reference Arial; Title 21 pt, Subtitle 12 pt, Heading 1 15 pt, Heading 2 12 pt. Normal 7 pt after, line spacing 1.06. Clone real styles without global substitutions.\nTables: dark blue 203864, white header type; alternating F2F5F9/FFFFFF, gray D9D9D9 borders; cell margins 85 twips; table type 9.5 pt. Repeat headers and keep rows intact.\nSlots: replace body title, metadata, paragraphs, tables, and diagrams with Data Karyawan content. Retain all source content/status/decisions, grouped field mapping and implementation/acceptance sections. Add suggested functional types, explicitly pending metadata verification. No invented EDT/form/entity names. Footer code is replaced with source Document ID FDD-HR-SPICY.\nPackage: preserve styles, numbering, theme, headers, footer PAGE field and original opaque parts. Existing body drawings may be removed as unrelated Kontrak content; add a flow drawing. Inventory reference-package-inventory.json.\nFlow: review source -> mapping -> approval -> validation -> import -> reconciliation -> process-owner approval; mapping/validation/import/reconciliation failures return to corrective work.\nFidelity: reference byte identity unchanged; compare page geometry, styles, table pattern and preserve-only package inventory. Validate content coverage and view every final page before delivery.\n''',encoding='utf8')

# Deterministic process diagram, in the same blue process / amber decision grammar as the reference.
W,H=1500,1800
im=Image.new('RGB',(W,H),'white');dr=ImageDraw.Draw(im)
font=ImageFont.truetype(r'C:/Windows/Fonts/arial.ttf',28)
small=ImageFont.truetype(r'C:/Windows/Fonts/arial.ttf',25)
bold=ImageFont.truetype(r'C:/Windows/Fonts/arialbd.ttf',29)
blue='#203864';line='#526985';fill='#EDF3FC';amber='#FFF2CC'
def center(txt,box,f=font,color=blue):
 x1,y1,x2,y2=box;lines=txt.split('\n');rh=38 if f!=small else 34;yy=(y1+y2-rh*len(lines))/2
 for text in lines:
  b=dr.textbbox((0,0),text,font=f);dr.text(((x1+x2-(b[2]-b[0]))/2,yy),text,font=f,fill=color);yy+=rh

def box(txt,b,kind='process'):
 if kind=='decision':
  x,y,x2,y2=b;dr.polygon([((x+x2)/2,y),(x2,(y+y2)/2),((x+x2)/2,y2),(x,(y+y2)/2)],fill=amber,outline='#BF9000',width=3)
 else:dr.rounded_rectangle(b,radius=25 if kind=='terminal' else 7,fill=fill,outline=line,width=3)
 center(txt,b,bold if kind=='terminal' else font)

def arrow(points,label=None,pos=None):
 dr.line(points,fill=line,width=3)
 (x0,y0),(x,y)=points[-2:];a=math.atan2(y-y0,x-x0);l=13
 dr.polygon([(x,y),(x-l*math.cos(a-.45),y-l*math.sin(a-.45)),(x-l*math.cos(a+.45),y-l*math.sin(a+.45))],fill=line)
 if label:
  xx,yy=pos;bb=dr.textbbox((xx,yy),label,font=small);dr.rectangle((bb[0]-5,bb[1]-3,bb[2]+5,bb[3]+3),fill='white');dr.text((xx,yy),label,font=small,fill=blue)
# Central trunk with three corrective loops; enough space around all labels.
box('Mulai',(440,20,960,90),'terminal')
box('Periksa data sumber Spicy\n61 kolom dan 64 data karyawan',(380,130,1020,240))
box('Petakan field dan data terkait\nPeriksa standar, konfigurasi, dan gap',(340,285,1060,395))
box('Pemetaan\ndisetujui?',(460,440,940,600),'decision')
box('Konfirmasi definisi,\nmaster, dan konfigurasi',(1110,445,1480,590))
box('Validasi data sebelum impor',(340,655,1060,745))
box('Data\nvalid?',(460,790,940,950),'decision')
box('Perbaiki data\natau referensi master',(1110,795,1480,940))
box('Impor melalui data entity\nyang telah dikonfirmasi',(340,1005,1060,1115))
box('Periksa hasil impor\ndan rekonsiliasi per field / record',(340,1170,1060,1280))
box('Hasil\nsesuai?',(460,1325,940,1485),'decision')
box('Telusuri dan perbaiki\nmapping, data, atau impor',(10,1325,390,1485))
box('Persetujuan pemilik proses',(340,1540,1060,1630))
box('Selesai',(440,1690,960,1760),'terminal')
for y1,y2 in [(90,130),(240,285),(395,440),(600,655),(745,790),(950,1005),(1115,1170),(1280,1325),(1485,1540),(1630,1690)]:arrow([(700,y1),(700,y2)])
arrow([(940,520),(1110,520)],'Tidak',(975,480));arrow([(1295,445),(1295,340),(1060,340)])
arrow([(940,870),(1110,870)],'Tidak',(975,830));arrow([(1295,795),(1295,700),(1060,700)])
arrow([(1060,1060),(1370,1060),(1370,940)],'Gagal impor',(1110,1013))
arrow([(460,1405),(390,1405)],'Tidak',(395,1360))
arrow([(200,1325),(200,340),(340,340)])
for y in [610,960,1490]:center('Ya',(710,y,790,y+35),small)
im.save(root/'Alur_Data_Karyawan_HOGY.png',dpi=(200,200))

para('Functional Design Document','Title')
para('Data Karyawan HOGY','Subtitle')
meta=[['Informasi','Keterangan'],['Document ID','FDD-HR-SPICY'],['Project','HR dan Payroll PT. HOGY INDONESIA'],['Platform','Microsoft Dynamics 365 Finance and Operations'],['Menu tujuan','Human Resource > Workers > Employee'],['Tanggal','28 Oktober 2026'],['Versi','Draf 1.1'],['Basis dokumen','07-EMP- Data Karyawan MSD 365.docx; format FDD Kontrak Karyawan HOGY v1.3'],['Prepared by','Krisna Prasetya'],['Status','Untuk review teknis']]
table(meta,meta_proto)
heading('1. Tujuan')
# Preserve source purpose paragraphs exactly.
start=False
for p in src.paragraphs:
 if p.text=='1. Tujuan':start=True;continue
 if p.text=='2. Alur penggunaan':break
 if start and p.text.strip():para(p.text)
d.add_page_break()
heading('2. Alur penggunaan')
para('Alur berikut mencakup persetujuan pemetaan, pemeriksaan sebelum impor, dan rekonsiliasi hasil. Data atau pemetaan yang belum sesuai dikembalikan untuk diperbaiki sebelum diterima oleh pemilik proses.')
p=para();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run().add_picture(str(root/'Alur_Data_Karyawan_HOGY.png'),width=Inches(6.45),height=Inches(7.74))
p.paragraph_format.space_after=Pt(0)

setup(d.add_section(WD_SECTION_START.NEW_PAGE),True)
heading('3. Modification')
heading('3.1 Data karyawan',2)
for i,p in enumerate(src.paragraphs):
 if p.text=='3.1 Data karyawan':
  para(src.paragraphs[i+1].text);break
heading('3.2 Pemetaan field sumber',2)
para('Status berikut merupakan penilaian awal dan perlu dikonfirmasi pada lingkungan MSD 365 F&O yang digunakan. Kolom EDT mencatat usulan tipe data fungsional; nama EDT, table, form, dan data entity belum ditetapkan. Field tambahan hanya dikembangkan untuk kesenjangan yang telah terkonfirmasi.')
rows=[['No.','Field label','EDT','Catatan']]
# Types are design proposals only, not unverified product metadata.
types=[
'Teks / string','Teks / string','Referensi / enum','Referensi posisi','Referensi organisasi','Dihitung; tidak disimpan','Tanggal / date','Referensi / enum','Referensi grade','Teks / string','Referensi / enum','Teks / string','Teks / string','Teks / string','Dihitung; tidak disimpan','Referensi organisasi','Referensi / enum','Tanggal / date','Numerik + satuan','Referensi cost center','Teks / pilihan terkontrol','Referensi pendidikan','Referensi / enum','Referensi bank + teks rekening','Referensi / teks','Dokumen identitas; tipe dikonfirmasi','Dokumen identitas; tipe dikonfirmasi','Tanggal per dokumen','Referensi / kunci integrasi','Boolean / enum Y-N','Referensi kode dan rute','Belum ditetapkan','Belum ditetapkan','Boolean / enum; dikonfirmasi','Belum ditetapkan','Boolean / data tanggungan','Teks + tanggal; data terkait','Teks + tanggal; data terkait','Teks + tanggal; data berulang']
for i,row in enumerate(src.tables[2].rows[1:]):
 vals=[c.text for c in row.cells]
 rows.append([str(i+1),vals[0],types[i],f'Status awal: {vals[1]}.\n{vals[2]}'])
table(rows,field_proto,[.4,2.15,2.15,5.0])
para('Field yang dikelompokkan dalam satu baris mengikuti pengelompokan pada dokumen sumber. Workbook pemetaan akhir tetap harus menjabarkan keputusan untuk seluruh 61 kolom sumber, termasuk kolom yang dihitung atau dikecualikan.')

setup(d.add_section(WD_SECTION_START.NEW_PAGE),False)
heading('4. Validasi dan hak akses')
table([[c.text for c in row.cells] for row in src.tables[3].rows],valid_proto)
heading('5. Tahapan implementasi')
table([[c.text for c in row.cells] for row in src.tables[4].rows],valid_proto,[.4,3.4,3.4])
# Retain every decision, acceptance item and source reference, in original order.
for section in ['6. Keputusan yang diperlukan','7. Kriteria penerimaan','8. Referensi']:
 heading(section)
 active=False
 for p in src.paragraphs:
  if p.text==section:active=True;continue
  if active and p.style.name.startswith('Heading'):break
  if active and p.text.strip():para(p.text)
# Keep source field/source text and all source decisions intact; avoid orphaned headings.
for p in d.paragraphs:
 if p.style.name.startswith('Heading'):p.paragraph_format.keep_with_next=True
# Let Word refresh PAGE fields without rewriting unrelated source parts.
settings=d.settings._element
uf=settings.find(qn('w:updateFields'))
if uf is None:uf=OxmlElement('w:updateFields');settings.append(uf)
uf.set(qn('w:val'),'true')
final=root/'07-EMP_FDD_Data_Karyawan_HOGY_v1.1.docx'
d.save(final)
assert sha256(ref.read_bytes()).hexdigest() in (root/'artifact.md').read_text(encoding='utf8')
alltext='\n'.join(p.text for p in d.paragraphs)+'\n'+'\n'.join(c.text for t in d.tables for row in t.rows for c in row.cells)
for row in src.tables[2].rows[1:]:
 for c in row.cells:assert c.text in alltext,c.text
for title in ['6. Keputusan yang diperlukan','7. Kriteria penerimaan','8. Referensi']:
 assert title in alltext
assert 'Kontrak karyawan mencatat' not in alltext
print(final)
print('Preserved 39 grouped mapping rows; 8 validation rules; 6 implementation steps; source decisions, acceptance criteria and references.')
