from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.shared import Pt,RGBColor
root=Path(r'E:/Panda/Hogy/outputs/fdd-kontrak-final')
src=root/'02-EMP_FDD_Kontrak_Karyawan_HOGY.docx'
d=Document(src)
remove_starts=(
 'Tampilkan field Worker setelah Company',
 'Field yang ditambahkan pada section Payroll dijabarkan',
 'Semua field berikut berupa nominal bulanan',
 'Kolom EDT mencantumkan sumber table',
)
removed=[]
for p in list(d.paragraphs):
 if p.text.startswith(remove_starts):
  removed.append(p.text);p._element.getparent().remove(p._element)
def cell_text(c,text):
 c.text=text
 for p in c.paragraphs:
  p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(2)
  for r in p.runs:r.font.name='Arial';r.font.size=Pt(9.5);r.font.color.rgb=RGBColor(0,0,0)
employees=d.tables[1];history=d.tables[2]
for r in employees.rows[1:]:cell_text(r.cells[2],'Form: HcmWorkerEmployementFormPart\nField type: real (nominal)')
for r in history.rows[1:]:cell_text(r.cells[2],'Form: HcmEmploymentHistory\nField type: real (nominal)')
# Worker is a header display field, included in the same field specification.
new=deepcopy(history.rows[1]._tr)
history.rows[0]._tr.addnext(new)
worker=history.rows[1]
values=['1','Worker','Form: HcmEmploymentHistory\nField type: worker reference (display)','Ditampilkan pada header setelah Company dan sebelum Worker type. Nilai mengikuti karyawan pada kontrak terkait. Read-only.']
for c,v in zip(worker.cells,values):cell_text(c,v)
for n,r in enumerate(history.rows[2:],2):cell_text(r.cells[0],str(n))
for r in d.tables[0].rows:
 if r.cells[0].text=='Versi':cell_text(r.cells[1],'1.1')
dest=root/'02-EMP_FDD_Kontrak_Karyawan_HOGY_v1.1.docx'
d.save(dest)
assert len(removed)==4,len(removed)
assert len(history.rows)==10
assert len(d.inline_shapes)==3
text=' '.join(p.text for p in d.paragraphs)+' '.join(c.text for t in d.tables for r in t.rows for c in r.cells)
assert 'verifikasi metadata D365' not in text
assert 'mengikuti sumber Employment history' not in text
print(dest)
print('Removed 4 explanatory paragraphs; Worker added; 16 amount field mappings updated; all 3 images preserved.')
