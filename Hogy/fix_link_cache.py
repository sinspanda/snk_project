import zipfile, xml.etree.ElementTree as E, os, openpyxl
p='outputs/payroll-analysis-20261102/HOGY_Analisis_Formula_Komponen_Gaji_v2.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(p) as z: data={n:z.read(n) for n in z.namelist()}
root=E.fromstring(data['xl/worksheets/sheet1.xml'])
for c in root.findall('.//s:c',ns):
    f=c.find('s:f',ns)
    if f is not None and f.text and f.text.startswith('HYPERLINK('):
        label=f.text.split(',"',1)[1][:-2].replace('""','"')
        v=c.find('s:v',ns)
        if v is None: v=E.SubElement(c,'{'+ns['s']+'}v')
        v.text=label
        c.set('t','str')
E.register_namespace('',ns['s'])
data['xl/worksheets/sheet1.xml']=E.tostring(root,encoding='utf-8',xml_declaration=True)
with zipfile.ZipFile(p+'.tmp','w',zipfile.ZIP_DEFLATED) as z:
    for n,b in data.items():z.writestr(n,b)
os.replace(p+'.tmp',p)
a=openpyxl.load_workbook('outputs/payroll-analysis-20261102/HOGY_Analisis_Formula_Komponen_Gaji.xlsx')
b=openpyxl.load_workbook(p)
changes=[(s.title,c.coordinate) for s in a for row in s for c in row if c.value!=b[s.title][c.coordinate].value]
assert len(changes)==88 and all(s=='Analisis Komponen' and c[0] in ['K','M'] for s,c in changes)
cached=openpyxl.load_workbook(p,data_only=True)
assert cached.worksheets[0]['K7'].value=='Rules HI 2025!B14:E15'
print('Verified 88 hyperlink formulas; only intended references changed; cached labels valid.')
