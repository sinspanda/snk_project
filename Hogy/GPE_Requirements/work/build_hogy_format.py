from pathlib import Path
from copy import deepcopy
import re, json, hashlib, zipfile, posixpath
from lxml import etree as E

HERE=Path(__file__).resolve().parent
REF=Path(r'E:\Panda\Hogy\Blueprint_NSI HOGY_Payroll System V1.0.docx')
OUT=HERE.parent/'GPE_Requirement_Document_Format_Blueprint_HOGY_v0.1.docx'
EXPECTED='23f9245e6620f7b8f75cb4866d93bfb9ecb3f19c4c89715cb73c1ac1c2f8eb4d'
assert hashlib.sha256(REF.read_bytes()).hexdigest()==EXPECTED
assert (HERE/'artifact.md').exists()
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships','wp':'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
W='{'+NS['w']+'}'
def node(tag, **attrs):
    n=E.Element(W+tag)
    for k,v in attrs.items(): n.set(W+k,str(v))
    return n
def txt(e): return ''.join(e.xpath('.//w:t/text()',namespaces=NS))
def getpr(e):
    p=e.find(W+'pPr')
    if p is None: p=node('pPr');e.insert(0,p)
    return p
def clean_markers(e):
    for n in list(e.iter()):
        if E.QName(n).localname in ['bookmarkStart','bookmarkEnd','proofErr','lastRenderedPageBreak']:
            if n.getparent() is not None:n.getparent().remove(n)
    for n in e.iter():
        for k in list(n.attrib):
            if E.QName(k).localname in ['paraId','textId']: del n.attrib[k]
    return e
def replace_p(p,value):
    rpr=p.find('w:r/w:rPr',NS)
    if rpr is None: rpr=p.find('w:pPr/w:rPr',NS)
    rpr=deepcopy(rpr) if rpr is not None else None
    for child in list(p):
        if child.tag!=W+'pPr':p.remove(child)
    r=node('r')
    if rpr is not None:r.append(rpr)
    t=node('t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=value
    r.append(t);p.append(r)
    return p
def clone_p(sample,value):return clean_markers(replace_p(deepcopy(sample),value))
def prop(pr,name,**attrs):
    e=pr.find(W+name)
    if e is None:e=node(name);pr.append(e)
    for k,v in attrs.items():e.set(W+k,str(v))
    return e

zin=zipfile.ZipFile(REF)
parts={n:zin.read(n) for n in zin.namelist()}
root=E.fromstring(parts['word/document.xml'])
body=root.find(W+'body'); original=list(body)
tables=[e for e in original if e.tag==W+'tbl']
samples={'body':original[77],'h1':original[75],'h2':original[76],'h3':original[133],'bullet':original[84]}
table_samples={2:tables[4],3:tables[5],6:tables[6]}
source= (HERE/'requirements.md').read_text(encoding='utf-8')
reqs=[]
for m in re.finditer(r'^### ([A-Z]+-\d{2}) \| ([^\n]+)\n(.*?)(?=^#{1,3} |\Z)',source,re.M|re.S):
    chunks=[p.strip() for p in m.group(3).split('\n\n') if p.strip() and p.strip()!='---']
    reqs.append({'id':m.group(1),'name':m.group(2),'meta':chunks[0],'desc':chunks[1],'ac':chunks[2]})
assert len(reqs)==47

def para(value,kind='body',bold=False):
    p=clone_p(samples[kind],value)
    pr=getpr(p)
    if kind.startswith('h'):prop(pr,'keepNext')
    if bold:
        rpr=p.find('w:r/w:rPr',NS)
        if rpr is None:rpr=node('rPr');p.find(W+'r').insert(0,rpr)
        prop(rpr,'b')
    body.append(p)
    return p
def head(value,level=1,page=False):
    p=para(value,'h'+str(level))
    if page:prop(getpr(p),'pageBreakBefore')
    return p
def fill_cell(cell,value):
    ps=cell.findall(W+'p'); sample=ps[0]
    for p in ps:cell.remove(p)
    for line in str(value).split('\n'):
        p=clone_p(sample,line)
        prop(getpr(p),'keepNext',val=0)
        cell.append(p)
def clone_table(sample,rows):
    t=deepcopy(sample); trlist=t.findall(W+'tr'); hs=deepcopy(trlist[0]); rs=deepcopy(trlist[1])
    for tr in trlist:t.remove(tr)
    for idx, vals in enumerate(rows):
        row=deepcopy(hs if idx==0 else rs)
        cells=row.findall(W+'tc');assert len(cells)==len(vals)
        trpr=row.find(W+'trPr')
        if trpr is None:trpr=node('trPr');row.insert(0,trpr)
        for n in list(trpr):
            if n.tag==W+'trHeight':trpr.remove(n)
        prop(trpr,'cantSplit')
        if idx==0:prop(trpr,'tblHeader')
        for c,v in zip(cells,vals):fill_cell(c,v)
        t.append(clean_markers(row))
    return t
def table(rows):
    t=clone_table(table_samples[len(rows[0])],rows);body.append(t);return t
def fragment(start,end=None):
    content=source.split(start+'\n',1)[1]
    if end: content=content.split(end+'\n',1)[0]
    return content.strip()
def emit_md(content,depth=0,ignore_top=False):
    lines=content.splitlines();i=0
    while i<len(lines):
        s=lines[i].strip();i+=1
        if not s or s=='---':continue
        if s.startswith('|'):
            data=[]
            while True:
                vals=[v.strip() for v in s.strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?',v) for v in vals):data.append(vals)
                if i>=len(lines) or not lines[i].strip().startswith('|'):break
                s=lines[i].strip();i+=1
            table(data);continue
        if s.startswith('#'):
            level=len(s)-len(s.lstrip('#'));value=s[level:].strip()
            if ignore_top and level==1:continue
            head(value,min(3,max(2,level+depth)));continue
        if s.startswith('- '):para(s[2:],'bullet')
        elif s.startswith('> '):para(s[2:])
        else:para(s)

# Retain the original cover and frontmatter components; replace client-specific slots.
for i in [0,4,16,34]:
    for p in original[i].xpath('.//w:txbxContent/w:p',namespaces=NS):
        value=txt(p)
        replacements={'MICROSOFT DYNAMICS 365FO':'ODOO','Payroll System':'HRIS, People & Payroll','PT. Hogy Indonesia':'GPE','PT. Nusantara Secom Infotech':'Draft untuk Review'}
        if value in replacements:replace_p(p,replacements[value])
for t in original[31].findall('.//'+W+'t'):
    if (t.text or '').strip()=='aaa':t.text=''
# Remove only pure logo drawings, leaving outer anchored textboxes/sidebar geometry.
for d in reversed(root.xpath('.//w:drawing',namespaces=NS)):
    if d.xpath('.//a:blip',namespaces=NS) and not txt(d):d.getparent().remove(d)
for obj in root.xpath('.//w:object',namespaces=NS):obj.getparent().remove(obj)
replace_p(original[55],'Persetujuan dokumen hanya berlaku untuk requirement dan solusi yang secara eksplisit diterima. Item OPEN, klasifikasi TBD, prioritas, biaya dan jadwal belum dianggap disetujui. Dokumen ini berstatus Draft for Review.')
replace_p(original[56],'GPE')
replace_p(original[61],'Tim Implementasi - reviewer dikonfirmasi')
front_tables={
49:[['Version','Date','Author','Description'],['0.1','2 September 2026','Draft untuk review GPE','Requirement HRIS, People & Payroll berdasarkan MOM 18, 21, 22 Juli 2026.'],['','','','']],
53:[['# of Copy','Description','Location'],['1','Master draft untuk review GPE','Digital / repository proyek'],['','','']],
57:[['Name','Project Role','Date','Signed'],['TBD','HR HO / HR Site','',''],['TBD','GA / Operations','',''],['TBD','Finance / Accounting','',''],['TBD','Project Owner / Management','','']],
62:[['Name','Project Role','Date','Signed'],['TBD','Functional Consultant','',''],['TBD','Technical / Integration','',''],['TBD','IT / Security','',''],['TBD','Project Lead','','']]}
for idx,rows in front_tables.items():
    replacement=clone_table(original[idx],rows);body.replace(original[idx],replacement);original[idx]=replacement
# Erase the source content tail, preserve the final section exactly.
final_sect=deepcopy(original[-1]);assert final_sect.tag==W+'sectPr'
for child in list(body)[75:]:body.remove(child)
table([['Status / Solution','Interpretation'],['Tercatat','Disebutkan di summary/MOM; belum merupakan sign-off.'],['Terbuka / OPEN','Sebagian aturan belum final; lihat D01-D16.'],['Usulan','Kontrol atau kriteria uji ditambahkan untuk review.'],['TBD - Fit-gap Odoo','Standard/configuration/manual/workaround/customization belum dinilai pada versi Odoo yang disepakati.']])
para('Seluruh kriteria penerimaan adalah usulan untuk review. Tidak ada klasifikasi standard/customization, fase delivery, biaya, jadwal atau rumus legal yang otomatis disetujui dari dokumen ini.')

head('Project Overview',page=True)
head('Overview',2)
para('Dokumen GPE-URD-HRIS-001 versi 0.1, 2 September 2026, mencakup AKP, GAM dan HO. Dokumen ini menerjemahkan summary MOM 18, 21 dan 22 Juli 2026 menjadi kebutuhan HRIS end-to-end untuk review, fit-gap Odoo dan UAT. Platform/versi serta solusi teknis final menunggu keputusan D12/D16.')
emit_md(fragment('### Tujuan dokumen','### Dasar penyusunan'))
emit_md(fragment('### Dasar penyusunan','### Cara membaca'))
emit_md(fragment('# Konteks dan batas scope','# Peran, akses, dan approval'))
head('Deliverables dan Modification',2)
para('Deliverable tahap ini adalah requirement baseline draft, katalog proses/aktivitas, kebutuhan data dan interface, kriteria penerimaan, serta daftar keputusan. Konfigurasi/modul custom, migrasi, training dan deployment hanya dapat dikomitmenkan setelah fit-gap dan scope delivery disetujui. Kolom Solution pada aktivitas sengaja diberi TBD.')

head('Master Data dan Konfigurasi',page=True)
masters=[
('Komponen Gaji dan Tabel Gaji','Struktur komponen per site/employee, all-in/OT, recurring/variable, rate, eligibility, tanggal efektif dan pembulatan. Rujukan PAY-01 sampai PAY-03; D04-D07.'),
('Employment Type dan Employee Master','NIK KTP terpisah dari NIK employee; status tetap/kontrak, tanggal masuk, kontrak, lokal/nonlokal, histori penempatan. Tahap pembentukan NIK menunggu D11. Rujukan EMP-01.'),
('Department, Section, Position dan Job Level','Company bila digunakan, operating unit, site, lokasi/pit, departemen, unit dan jabatan. Section/job level dipetakan bila digunakan GPE; jangan mengambil master dari proyek template. Rujukan D01/D14.'),
('Jadwal Shift dan Kalender','Roster 13:1/6:1, shift, kode absensi, libur nasional dan work schedule HO. Rujukan ATT-01 sampai ATT-03; D07.'),
('Tipe Cuti dan Master Data Cuti','Jenis, eligibility, saldo, carryover/expiry, kalender dan approval; annual 12 hari setelah setahun adalah catatan MOM yang masih membutuhkan finalisasi aturan. Rujukan LEV-01 sampai LEV-03; D08.'),
('Hitungan Lembur','Rate/matriks per site, status employee, D6/D7/libur, jam istirahat dan kasus operasional. Tidak mengadopsi formula lembur dari proyek template. Rujukan ATT-03/PAY-01; D07.'),
('Payroll Calendar and Parameters','Cut-off attendance/SPL/insentif, periode, koreksi slip bayangan, approval/lock, pembayaran terpisah, dan posting/reversal. Rujukan PAY-04/PAY-05/FIN-01; D05-D07/D15.'),
('Security Roles and Workflow','Mapping user-role-site/company, validator versus approver, reason reject, delegasi dan histori akses. Rujukan SEC-01/SEC-02; D01/D02/D14.'),
('GA, Asset dan Accounting Master','Mess, kapasitas, vendor, tarif layanan, kategori meals, item/APD, satuan, serial, gudang, minimum stock, kendaraan, COA dan analytic distribution. Rujukan D03/D04/D10/D15.')]
for title,content in masters:head(title,2);para(content)
head('Master Data Minimum dan Saldo Awal',2)
emit_md(fragment('## Master data minimum','---'))

head('Report dan Printout',page=True)
head('Report',2)
emit_md(fragment('## Keluaran laporan','## Kontrol non-fungsional yang diusulkan'))
head('Printout dan Form',2)
para('Format final menggunakan contoh GPE: slip bayangan/final, rekap payroll, PTK/MPP, kontrak, form cuti/SPL, SK/SP, travel, custody, exit clearance dan pengajuan loan/CA sesuai proses yang diterima. Template pajak, bank dan pembayaran otomatis tidak ditambahkan tanpa persetujuan scope. Lihat D05/D06/D12/D13.')

head('Alur Proses',page=True)
head('Role and Approval Matrix',2)
emit_md(fragment('## Peran yang terlibat','## Requirement akses dan approval'))
para('Activity ID memakai pola GPE.[kelompok].[nomor] dan dipetakan ke ID requirement pada Comments / Notes. PIC adalah fungsi usulan, bukan penugasan personal. Description merangkum aktivitas; aturan lanjutan dan acceptance disajikan setelah tabel agar tetap terbaca.')
groups=[
('Akses dan Approval',['SEC'],'HR HO / IT'),
('Karyawan, Recruitment dan Manpower Planning',['EMP','REC'],'HR'),
('Absensi, Working Schedule dan Lembur',['ATT'],'HR Site / HO'),
('Cuti dan Perubahan Roster',['LEV'],'HR / Admin'),
('Payroll Bulanan',['PAY'],'HR / Finance'),
('Employee Loan',['LON'],'HR / Finance'),
('Mutasi, Promosi, SP dan Dokumen',['CAR','DIS','DOC'],'HR / User'),
('Pemberhentian dan Exit Clearance',['OFF'],'HR / GA / Finance'),
('Layanan dan Monitoring GA',['GA'],'GA'),
('Custody, APD dan Pengadaan',['AST','PRO'],'GA / Logistics'),
('Accounting dan Cash Advance',['FIN'],'Finance')]
all_covered=[]
for title,prefixes,pic in groups:
    selected=[r for r in reqs if r['id'].split('-')[0] in prefixes]
    head(title,2)
    rows=[['Activity ID','Activity Name','PIC','Description','Solution','Comments / Notes']]
    for r in selected:
        first,sep,rest=r['desc'].partition('. ')
        r['rest']=rest if sep else ''
        summary=first+'.' if sep else first
        decision=' / '.join(sorted(set(re.findall(r'\bD\d{2}\b',r['meta']))))
        status=r['meta'].split('|')[0].replace('Status: ','').strip()
        rows.append(['GPE.'+r['id'].replace('-','.'),r['name'],pic,summary,'TBD\nFit-gap Odoo',r['id']+'\n'+status])
        all_covered.append(r['id'])
    table(rows)
    head('Business Rules dan Acceptance',3)
    for r in selected:
        para(r['id']+' | '+r['name'],bold=True)
        para(r['meta'])
        if r['rest']:para(r['rest'])
        para(r['ac'])

head('FitGap Traceability dan Open Decisions',page=True)
head('Requirement Baseline dan Interpretation',2)
table([['Item','Baseline draft'],['Functional / process requirements','43'],['Non-functional requirements','4 - usulan'],['Integration points','7'],['Reports','8'],['UAT scenarios','14 - usulan'],['Open decisions','16'],['Fit / Gap status','Belum dinilai; seluruh Solution masih TBD']])
para('Jumlah di atas merupakan hitungan requirement draft GPE, bukan angka FitGap proyek lain. Tercatat tidak berarti standard Odoo atau approved. Expected result payroll harus memakai aturan dan test fixture yang disetujui HR/Finance GPE.')
head('Integration dan Data',2)
emit_md(fragment('## Titik integrasi','## Master data minimum'),depth=1)
head('Non-Functional Requirements',2)
for r in reqs:
    if r['id'].startswith('NFR'):
        head(r['id']+' | '+r['name'],3)
        para(r['meta']);para(r['desc']);para(r['ac'])
head('UAT dan Acceptance Gate',2)
emit_md(fragment('# Rencana validasi dan UAT','# Daftar keputusan terbuka'),depth=1)
head('Open Decisions',2)
emit_md(fragment('# Daftar keputusan terbuka','# Paket data GPE dan persetujuan baseline'))
head('Data GPE dan Next Steps',2)
emit_md(fragment('## Checklist bahan workshop','## Lembar review dan persetujuan'),depth=1)
para('Review dan tanda tangan dilakukan pada bagian Approval setelah daftar scope diterima/ditunda dan keputusan OPEN yang dikecualikan dicatat. Tanggal dan nama reviewer harus dikonfirmasi GPE. Tidak ada otorisasi perubahan produksi melalui dokumen draft ini.')
head('Source Document Register',2)
table([['Source','Usage'],['Summary MOM dalam percakapan','Sumber utama kebutuhan dan pengelompokan S1-S6.'],['18072026 MOM - GPE - UREQ HRIS PEOPLE PAYROLL (Jaga).docx','Rujukan topik rapat 18, 21 dan 22 Juli 2026; bukan validasi regulasi.'],['Blueprint referensi pengguna','Format cover, bab, approval, heading, tabel aktivitas dan header/footer; bukan sumber aturan bisnis GPE.']])
body.append(final_sect)

# Update running header branding using existing frame/cell/paragraph formatting.
hdr=E.fromstring(parts['word/header2.xml'])
ht=hdr.find(W+'tbl');hcs=ht.find(W+'tr').findall(W+'tc')
for idx,value in [(0,'HRIS'),(1,'GPE'),(3,'ODOO')]:
    p=hcs[idx].find(W+'p');replace_p(p,value)
    prop(getpr(p),'jc',val='center')
    rp=p.find('w:r/w:rPr',NS)
    if rp is None:rp=node('rPr');p.find(W+'r').insert(0,rp)
    prop(rp,'sz',val=22);prop(rp,'b')
    tcp=hcs[idx].find(W+'tcPr');prop(tcp,'vAlign',val='center')
ftr=E.fromstring(parts['word/footer3.xml'])
for p in ftr.findall('.//'+W+'p'):
    value=txt(p)
    if 'Document' in value and 'Name' in value:replace_p(p,'Document Name: GPE HRIS | v0.1 - Draft')
    elif 'All rights' in value:replace_p(p,'INTERNAL - Draft for Review. Requirement GPE; persetujuan dan scope final mengikuti daftar keputusan.')
    for fc in p.findall('.//'+W+'fldChar'):fc.set(W+'dirty','true')
    if any('page' in (n.text or '').lower() for n in p.findall('.//'+W+'instrText')):
        for t in p.findall('.//'+W+'t'):
            if (t.text or '').strip().isdigit():t.text=''

# Rebuild the current TOC cache inside the original doc-part SDT, preserving sdtPr.
for n in root.xpath('.//w:bookmarkStart|.//w:bookmarkEnd',namespaces=NS):n.getparent().remove(n)
entries=[];bookid=1000
for p in body.findall(W+'p'):
    st=p.find('w:pPr/w:pStyle',NS)
    if st is not None and st.get(W+'val') in ['BPHead1','BPHead2']:
        name='_GPE_'+str(bookid);start=node('bookmarkStart',id=bookid,name=name);end=node('bookmarkEnd',id=bookid)
        p.insert(1,start);p.append(end)
        entries.append((name,txt(p),st.get(W+'val')));bookid+=1
sdt=body.find(W+'sdt');content=sdt.find(W+'sdtContent')
toc_samples={}
for p in content.findall(W+'p'):
    s=p.find('w:pPr/w:pStyle',NS)
    if s is not None:toc_samples.setdefault(s.get(W+'val'),deepcopy(p))
for n in list(content):content.remove(n)
for i,(anchor,label,sty) in enumerate(entries):
    sample=toc_samples.get('TOC1' if sty=='BPHead1' else 'TOC2',next(iter(toc_samples.values())))
    p=clone_p(sample,'')
    for child in list(p):
        if child.tag!=W+'pPr':p.remove(child)
    if i==0:
        for tag,attrs,text in [('fldChar',{'fldCharType':'begin','dirty':'true'},None),('instrText',{},' TOC \\o "1-2" \\h \\z \\u '),('fldChar',{'fldCharType':'separate'},None)]:
            r=node('r');n=node(tag,**attrs);n.text=text;r.append(n);p.append(r)
    link=node('hyperlink',anchor=anchor,history=1);r=node('r');rp=node('rPr');rp.append(node('rStyle',val='Hyperlink'));r.append(rp);t=node('t');t.text=label;r.append(t);link.append(r);p.append(link)
    if i==len(entries)-1:r=node('r');r.append(node('fldChar',fldCharType='end'));p.append(r)
    content.append(p)
settings=E.fromstring(parts['word/settings.xml']);prop(settings,'updateFields',val='true')

# Package-level source content cleanup; preserve all unaffected parts exactly.
removed={n for n in parts if n.startswith('word/media/') or n.startswith('word/embeddings/')}
for relname in ['word/_rels/document.xml.rels','word/_rels/header2.xml.rels']:
    rr=E.fromstring(parts[relname])
    for rel in list(rr):
        target=posixpath.normpath('word/'+rel.get('Target',''))
        if target in removed:rr.remove(rel)
    parts[relname]=E.tostring(rr,xml_declaration=True,encoding='UTF-8',standalone=True)
types=E.fromstring(parts['[Content_Types].xml'])
for n in list(types):
    if n.get('PartName','').lstrip('/') in removed:types.remove(n)
parts['[Content_Types].xml']=E.tostring(types,xml_declaration=True,encoding='UTF-8',standalone=True)
core=E.fromstring(parts['docProps/core.xml'])
for n in core:
    key=E.QName(n).localname
    if key=='title':n.text='GPE - Requirement Document HRIS, People & Payroll'
    elif key=='subject':n.text='Draft v0.1 - review requirement dan keputusan terbuka'
    elif key in ['creator','lastModifiedBy']:n.text=''
    elif key in ['created','modified']:n.text='2026-09-02T00:00:00Z'
app=E.fromstring(parts['docProps/app.xml'])
for n in list(app):
    if E.QName(n).localname in ['Pages','Words','Characters','Lines','Paragraphs','CharactersWithSpaces','HeadingPairs','TitlesOfParts']:app.remove(n)
    elif E.QName(n).localname in ['Company','Manager']:n.text=''
for name,e in [('word/document.xml',root),('word/header2.xml',hdr),('word/footer3.xml',ftr),('word/settings.xml',settings),('docProps/core.xml',core),('docProps/app.xml',app)]:
    parts[name]=E.tostring(e,xml_declaration=True,encoding='UTF-8',standalone=True)
for name in removed:del parts[name]
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as zout:
    for info in zin.infolist():
        if info.filename in parts:zout.writestr(deepcopy(info),parts[info.filename])

# Audit copied package, data coverage, fields and exact preserve-only subtrees.
allowed={'word/document.xml','word/header2.xml','word/footer3.xml','word/settings.xml','word/_rels/document.xml.rels','word/_rels/header2.xml.rels','[Content_Types].xml','docProps/core.xml','docProps/app.xml'}
changed=[n for n in parts if parts[n]!=zin.read(n)]
assert set(changed)<=allowed
assert set(all_covered)=={r['id'] for r in reqs if not r['id'].startswith('NFR')}
assert len(all_covered)==43
assert E.tostring(root.findall('.//'+W+'sectPr')[0])==E.tostring(original[45].find('w:pPr/w:sectPr',NS))
assert E.tostring(root.findall('.//'+W+'sectPr')[1])==E.tostring(final_sect)
assert parts['word/styles.xml']==zin.read('word/styles.xml')
assert parts['word/numbering.xml']==zin.read('word/numbering.xml')
textall=' '.join(txt(E.fromstring(v)) for k,v in parts.items() if k.startswith('word/') and k.endswith('.xml') and '/_rels/' not in k)
for bad in ['Hogy Indonesia','HOGY_','D365FO','MICROSOFT DYNAMICS','Port Agency','HG.QC','Bank Mandiri','Alisa Nida','Tri Mardiyanti','Oliver Raka','Nusantara Secom Infotech']:
    assert bad not in textall,bad
for r in reqs:
    assert r['id'] in textall,r['id']
    assert r['ac'] in textall,r['id']+' AC missing'
for prefix,count in [('D',16),('INT-',7),('RPT-',8),('UAT-',14)]:
    for i in range(1,count+1):assert f'{prefix}{i:02d}' in textall
anchors={n.get(W+'name') for n in root.findall('.//'+W+'bookmarkStart')}
assert len(anchors)==len(entries)
assert all(n.get(W+'anchor') in anchors for n in root.findall('.//'+W+'hyperlink') if n.get(W+'anchor'))
for relname in [k for k in parts if k.endswith('.rels')]:
    rr=E.fromstring(parts[relname]);base=posixpath.dirname(posixpath.dirname(relname)) if relname!='_rels/.rels' else ''
    for rel in rr:
        if rel.get('TargetMode')!='External':assert posixpath.normpath(posixpath.join(base,rel.get('Target'))) in parts,(relname,rel.get('Target'))
for name,data in parts.items():
    if name.endswith('.xml'):E.fromstring(data)
for partname in ['word/document.xml','word/header2.xml','word/footer3.xml']:
    e=E.fromstring(parts[partname]);relpath=posixpath.dirname(partname)+'/_rels/'+posixpath.basename(partname)+'.rels'
    relids={n.get('Id') for n in E.fromstring(parts[relpath])} if relpath in parts else set()
    used=e.xpath('.//@r:embed|.//@r:id|.//@r:link',namespaces=NS)
    assert set(used)<=relids,(partname,set(used)-relids)
assert hashlib.sha256(REF.read_bytes()).hexdigest()==EXPECTED
report={'output':str(OUT),'bytes':OUT.stat().st_size,'functional_requirements':43,'nfr':4,'open_decisions':16,'uat':14,'integration_points':7,'reports':8,'activity_matrices':len(groups),'sections':2,'preserve_only_parts_unchanged':True,'changed_parts':changed,'removed_from_output_only':sorted(removed),'source_unchanged':True,'toc_links':len(entries),'visual_qa':'NOT COMPLETED - soffice unavailable','field_refresh':'updateFields=true; live TOC with current no-page-number cache; Word refresh required for layout-dependent fields'}
(HERE/'hogy_format_qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
