from pathlib import Path
import zipfile,xml.etree.ElementTree as E,copy
f=Path(__file__).parent;W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';q=lambda x:'{'+W+'}'+x
E.register_namespace('w',W)
src=f/'03-ATT_FDD_Absensi_Karyawan_HOGY_v1.2.docx';out=f/'03-ATT_FDD_Absensi_Karyawan_HOGY_v1.2.docx'
with zipfile.ZipFile(src) as z:data={n:z.read(n) for n in z.namelist()}
doc=E.fromstring(data['word/document.xml']);body=doc.find(q('body'));ch=list(body)
def txt(x):return ''.join(t.text or '' for t in x.iter(q('t')))
def index(t):return next(i for i,x in enumerate(ch) if txt(x)==t)
start=index('3. Modification');end=index('4. Validasi dan hak akses')
fields_start=index('3.3 Field');buttons_start=index('3.4 Button')
def paragraph(t,heading=None):
 p=E.Element(q('p'));pr=E.SubElement(p,q('pPr'))
 if heading:E.SubElement(pr,q('pStyle'),{q('val'):heading});E.SubElement(pr,q('keepNext'))
 E.SubElement(pr,q('spacing'),{q('after'):'110'})
 r=E.SubElement(p,q('r'));E.SubElement(r,q('t')).text=t;return p
def pagebreak():
 p=E.Element(q('p'));r=E.SubElement(p,q('r'));E.SubElement(r,q('br'),{q('type'):'page'});return p
def clean(nodes):
 out=[]
 for x in nodes:
  y=copy.deepcopy(x)
  # Page breaks from the earlier layout are handled at feature/section boundaries.
  if y.tag==q('p') and not txt(y) and y.find('.//'+q('br')) is not None:continue
  out.append(y)
 return out
field_labels=[('Jadwal / Roster (Profile Calendar)','Attendance Staging - header import'),('Attendance Staging - header import','Employee Attendances - identitas dan jadwal'),('Employee Attendances - identitas dan jadwal','3.4 Button')]
fieldgroups=[clean(ch[index(a)+1:index(b)]) for a,b in field_labels]
# Remove group-caption paragraphs only; retain descriptions/tables.
for group in fieldgroups:
 group[:]=[x for x in group if not (x.tag==q('p') and txt(x).startswith(('Attendance Staging -','Employee Attendances -')))]
buttonlabels=['Jadwal / Roster (Profile Calendar)','Attendance Staging','Employee Attendances']
bi=[next(i for i in range(buttons_start+1,end) if txt(ch[i])==v) for v in buttonlabels]
buttongroups=[clean(ch[bi[j]+1:(bi[j+1] if j<2 else end)]) for j in range(3)]
imagebase=next(x for x in ch if x.find('.//'+q('drawing')) is not None)
new=[paragraph('3. Modification','Heading1')]
names=['Profile Calendar','Attendance Staging','Employee Attendances']
paths=['Path menu: Profile Calendar pada environment HOGY; path lengkap diverifikasi teknis.','Path menu usulan: Human resources > Attendance > Attendance Staging.','Path menu usulan: Human resources > Attendance > Employee Attendances.']
descs=['Mengelola Jadwal / Roster pada satu fitur. Compose, Upload Roster, tambah/edit manual dan tampilan matriks mengelola assignment Profile Calendar yang sama. Master dan assignment mengacu standar D365; upload serta tampilan roster merupakan pengembangan.','Menampung Raw Text setiap baris hasil import dan kolom parsing dengan status Pending. Validasi karyawan, jadwal dan duplikat baru dijalankan saat HR memilih Process Attendance.','Menyimpan hasil pengolahan staging per worker, work date dan kejadian shift, termasuk pasangan punch, snapshot jadwal serta referensi seluruh scan sumber.']
flows=['HR menyiapkan roster melalui Compose, upload atau tambah/edit. Validasi dan review dilakukan sebelum assignment disimpan. Perubahan tanggal terkait memperbarui roster dan menandai attendance belum final sebagai Need Reprocess.','Import menyimpan raw text dan parsing sebagai Pending. Process Attendance memvalidasi data Pending, mencocokkan jadwal, memeriksa duplikat, dan memilih punch masuk paling awal serta keluar paling akhir yang memenuhi rentang shift. Hasil valid yang tersimpan menjadi Processed; salinan identik Duplicate; kegagalan Error.','Hasil pairing membentuk/memperbarui Employee Attendances. HR memeriksa exception dan melakukan koreksi/reprocess bila diperlukan sebelum review dan Finalize. Hasil final menjadi dasar laporan dan proses payroll.']
R='http://schemas.openxmlformats.org/package/2006/relationships';rels=E.fromstring(data['word/_rels/document.xml.rels'])
for j,name in enumerate(names):
 num=f'3.{j+1}'
 if j:new.append(pagebreak())
 new += [paragraph(num+' '+name,'Heading2'),paragraph(paths[j]),paragraph(descs[j]),paragraph(num+'.1 Flow','Heading3')]
 im=copy.deepcopy(imagebase)
 for e in im.iter():
  if e.tag.endswith('}blip'):e.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed','rIdFeatureFlow'+str(j))
  if e.tag.endswith('}extent'):e.set('cx','5943600');e.set('cy','3608614')
  if e.tag.endswith('}ext') and 'cx' in e.attrib:e.set('cx','5943600');e.set('cy','3608614')
  if e.tag.endswith('}docPr'):e.set('id',str(910+j));e.set('name',name+' flow')
 new += [im,paragraph(flows[j]),pagebreak(),paragraph(num+'.2 Field','Heading3'),paragraph('EDT di bawah merupakan usulan tipe data fungsional; nama EDT teknis dikonfirmasi oleh tim teknis.')]+fieldgroups[j]
 new += [pagebreak(),paragraph(num+'.3 Button','Heading3')]+buttongroups[j]
 E.SubElement(rels,'{'+R+'}Relationship',Id='rIdFeatureFlow'+str(j),Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/image',Target='media/feature-flow-'+str(j)+'.png')
 data['word/media/feature-flow-'+str(j)+'.png']=(f/('flow-'+str(j)+'.png')).read_bytes()
new.append(pagebreak())
prefix=[E.tostring(x) for x in ch[:start]];suffix=[E.tostring(x) for x in ch[end:]]
for x in ch[start:end]:body.remove(x)
for i,x in enumerate(new):body.insert(start+i,x)
assert [E.tostring(x) for x in list(body)[:start]]==prefix
assert [E.tostring(x) for x in list(body)[-len(suffix):]]==suffix
data['word/document.xml']=E.tostring(doc,encoding='utf-8',xml_declaration=True)
data['word/_rels/document.xml.rels']=E.tostring(rels,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,d in data.items():
  if n.endswith('.xml'):E.fromstring(d)
  z.writestr(n,d)
print('PASS: grouped per feature; path/description + Flow/Field/Button; outside section 3 preserved.')
print(out)
