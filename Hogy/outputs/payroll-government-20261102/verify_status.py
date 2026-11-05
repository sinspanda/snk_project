import zipfile,xml.etree.ElementTree as E,os,openpyxl
d='outputs/payroll-government-20261102/'
p=d+'HOGY_Komponen_Gaji_Konsolidasi_BPJS_Pajak_Status.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z:data={n:z.read(n) for n in z.namelist()}
for n in list(data):
    if not n.startswith('xl/worksheets/sheet') or not n.endswith('.xml'):continue
    root=E.fromstring(data[n]);changed=False
    for c in root.findall('.//s:c',ns):
        f=c.find('s:f',ns)
        if f is not None and f.text and f.text.startswith('HYPERLINK('):
            label=f.text.split(',"',1)[1][:-2].replace('""','"')
            v=c.find('s:v',ns)
            if v is None:v=E.SubElement(c,'{'+ns['s']+'}v')
            v.text=label;c.set('t','str');changed=True
    if changed:
        E.register_namespace('',ns['s']);data[n]=E.tostring(root,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(p+'.tmp','w',zipfile.ZIP_DEFLATED) as z:
    for n,v in data.items():z.writestr(n,v)
os.replace(p+'.tmp',p)
a=openpyxl.load_workbook(d+'HOGY_Komponen_Gaji_Konsolidasi_BPJS_Pajak.xlsx')
b=openpyxl.load_workbook(p)
for s in a:
    for row in s:
        for c in row:assert c.value==b[s.title][c.coordinate].value,(s.title,c.coordinate)
s=b['Komponen Final'];assert s.tables['MasterKomponen'].ref=='A6:N57'
v=[s.cell(r,14).value for r in range(7,58)]
assert v.count('Clear')==10 and v.count('Need Confirmation')==41
c=openpyxl.load_workbook(p,data_only=True)
assert not [(s.title,x.coordinate) for s in c for row in s for x in row if x.data_type=='e']
print('Verified: existing values/formulas unchanged; 51 statuses; table filter includes Status; no cached formula errors.')
