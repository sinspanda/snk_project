from pathlib import Path
import zipfile, hashlib, json
from lxml import etree as E

ROOT=Path(__file__).resolve().parent
REF=Path(r'E:\Panda\Hogy\Blueprint_NSI HOGY_Payroll System V1.0.docx')
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def attrs(e):
    return [(E.QName(n).localname, {E.QName(k).localname:v for k,v in n.attrib.items()}, n.text) for n in e.iter() if n.attrib or (n.text and n.text.strip())]
z=zipfile.ZipFile(REF)
editable={'word/document.xml','word/settings.xml','word/header2.xml','word/footer3.xml','word/_rels/document.xml.rels','word/_rels/header2.xml.rels','[Content_Types].xml','docProps/core.xml','docProps/app.xml'}
remove={'word/media/image1.png','word/media/image3.emf','word/media/image4.emf','word/embeddings/oleObject1.bin','word/embeddings/oleObject2.bin'}
inventory=[{'path':n,'size':len(z.read(n)),'sha256':hashlib.sha256(z.read(n)).hexdigest(),'action':'editable' if n in editable else 'remove obsolete HOGY/QC assets' if n in remove else 'preserve-only'} for n in z.namelist()]
(ROOT/'reference_inventory.json').write_text(json.dumps({'reference':str(REF),'sha256':hashlib.sha256(REF.read_bytes()).hexdigest(),'parts':inventory},indent=2),encoding='utf-8')
for n in ['word/media/image1.png','word/media/image2.jpeg','word/media/image5.png']:
    (ROOT/Path(n).name).write_bytes(z.read(n))
body=E.fromstring(z.read('word/document.xml')).find('w:body',NS)
print('SAMPLE TABLE CELL',attrs(body[49].find('w:tr',NS).find('w:tc',NS)))
print('HEADER2',attrs(E.fromstring(z.read('word/header2.xml'))))
print('HEADER RELS',z.read('word/_rels/header2.xml.rels').decode())
print('SHAPE PARAS')
for idx in [0,4,16,34]:
    print(idx,[( ''.join(p.xpath('.//w:t/text()',namespaces=NS)),attrs(p.find('w:pPr',NS)) if p.find('w:pPr',NS) is not None else [],[attrs(r.find('w:rPr',NS)) if r.find('w:rPr',NS) is not None else [] for r in p.findall('w:r',NS)]) for p in body[idx].xpath('.//w:txbxContent/w:p',namespaces=NS)])
