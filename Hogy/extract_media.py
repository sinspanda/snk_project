import zipfile, pathlib, xml.etree.ElementTree as E
from PIL import Image,ImageOps,ImageDraw
src=r'C:\Users\SAYID\OneDrive\02. Project\HOGY\03. Design\Payroll (Phase 2)\Blueprint NSI HOGY - Payroll System V1.5.docx'
out=pathlib.Path(r'E:\Panda\Hogy\analysis_media');out.mkdir(exist_ok=True)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with zipfile.ZipFile(src) as z:
 rel={r.attrib['Id']:r.attrib['Target'] for r in E.fromstring(z.read('word/_rels/document.xml.rels'))}
 root=E.fromstring(z.read('word/document.xml'));prev=[];items=[]
 for p in root.findall('.//w:body//w:p',ns):
  t=''.join(p.itertext()) if False else ''.join(x.text or '' for x in p.findall('.//w:t',ns))
  if t:prev.append(t)
  for b in p.findall('.//a:blip',ns):
   target=rel.get(b.attrib.get('{'+ns['r']+'}embed'),'')
   if 'media/' in target:
    f=out/pathlib.Path(target).name
    f.write_bytes(z.read('word/'+target))
    if f not in items:items.append(f);print(f.name,' | '.join(prev[-2:])[:200])
 for batch in range(0,len(items),12):
  canvas=Image.new('RGB',(1500,1800),'white');d=ImageDraw.Draw(canvas)
  for j,f in enumerate(items[batch:batch+12]):
   im=Image.open(f).convert('RGB');im.thumbnail((480,410))
   x=(j%3)*500;y=(j//3)*450
   canvas.paste(im,(x,y+30));d.text((x+5,y+5),f.name,fill='black')
  canvas.save(out/f'contact_{batch//12}.jpg')
