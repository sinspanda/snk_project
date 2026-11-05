import zipfile,xml.etree.ElementTree as E,os,re,json,openpyxl
folder='outputs/payroll-government-20261102/'
p=folder+'HOGY_Komponen_Gaji_Konsolidasi_BPJS_Pajak.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:data={n:z.read(n) for n in z.namelist()}
links=0
for name,blob in list(data.items()):
    if not re.fullmatch(r'xl/worksheets/sheet\d+.xml',name):continue
    root=E.fromstring(blob)
    changed=False
    for c in root.findall('.//s:c',ns):
        f=c.find('s:f',ns)
        if f is not None and f.text and f.text.startswith('HYPERLINK('):
            label=f.text.split(',"',1)[1][:-2].replace('""','"')
            v=c.find('s:v',ns)
            if v is None:v=E.SubElement(c,'{'+ns['s']+'}v')
            v.text=label;c.set('t','str');links+=1;changed=True
    if changed:
        E.register_namespace('',ns['s'])
        data[name]=E.tostring(root,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(p+'.tmp','w',zipfile.ZIP_DEFLATED) as z:
    for n,b in data.items():z.writestr(n,b)
os.replace(p+'.tmp',p)
w=openpyxl.load_workbook(p,data_only=True)
f=openpyxl.load_workbook(p,data_only=False)
assert w['Komponen Final'].max_row==57
ids=[i for r in w['Komponen Final'].iter_rows(min_row=7,max_row=57,values_only=True) for i in str(r[0]).replace(' ','').split(',')]
assert sorted(map(int,ids))==list(range(1,54))
assert sum(r[1]=='Basic Salary' for r in w['Komponen Final'].iter_rows(min_row=7,values_only=True))==1
errors=[(s.title,c.coordinate,c.value) for s in w for row in s for c in row if c.data_type=='e']
assert not errors,errors
assert w['Simulasi Bulanan']['B32'].value==499975
assert w['Simulasi Bulanan']['B37'].value==11060000
assert w['Rekonsiliasi Tahunan']['B22'].value==13750000
baseline=json.load(open(folder+'baseline.json',encoding='utf8'))
for sname,index in [('Setup Asal',2),('Data Sumber Asal',3),('Rules HI 2025',4)]:
    old=baseline[index]['rows']
    for r,row in enumerate(old,1):
        for c,val in enumerate(row,1):assert w[sname].cell(r,c).value==val,(sname,r,c)
for s in f:
    for row in s:
        for c in row:
            if c.data_type=='f' and c.value.startswith('=HYPERLINK("#'):
                match=re.search(r"#'([^']+)'!([A-Z]+\d+(?::[A-Z]+\d+)?)",c.value)
                assert match and match[1] in f.sheetnames
                f[match[1]][match[2]]
print('Verified: 53 source IDs map to 51 rows; one BS; all source values unchanged; no formula error caches; sample outputs and internal link targets valid; links',links)
