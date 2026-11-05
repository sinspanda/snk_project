"""Apply the supplied process style to Registrasi only, preserving other pages."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json
from lxml import etree as E

SOURCE = Path(r'E:\Panda\Hogy\GPE_Drawio\Flow Asset to be 16.7.26.drawio')
OUTPUT = SOURCE.with_name('Flow Asset to be 16.7.26 - Trial Style Registrasi.drawio')
STYLE = 'shape=mxgraph.bpmn.task2;rectStyle=rounded;size=10;taskMarker=abstract;fontFamily=Segoe UI;fontSize=10.66667;fontColor=#ffffff;fontStyle=0;align=center;verticalAlign=middle;whiteSpace=wrap;html=1;strokeColor=#001DBC;fillColor=#0050ef;strokeWidth=1;spacing=3;'

def equivalent(before, after):
    assert before.tag == after.tag
    assert dict(before.attrib) == dict(after.attrib)
    assert before.text == after.text and before.tail == after.tail
    assert len(before) == len(after)
    for left, right in zip(before, after):
        equivalent(left, right)

def main():
    assert not OUTPUT.exists(), f'Output already exists: {OUTPUT}'
    source_bytes = SOURCE.read_bytes()
    document = E.fromstring(source_bytes)
    original = deepcopy(document)
    page = document.find("diagram[@name='Registrasi']")
    assert page is not None
    changed = []
    matched = []
    for cell in page.iter('mxCell'):
        if 'shape=mxgraph.bpmn.task2;' in cell.get('style', '') and cell.get('vertex') == '1':
            identity = cell.get('id') or cell.getparent().get('id')
            matched.append(identity)
            if cell.get('style') != STYLE:
                changed.append(identity)
            cell.set('style', STYLE)
    assert len(matched) == 19, matched
    # Verify all geometry, labels, connections, and other pages remain untouched.
    for before_page, after_page in zip(original, document):
        if after_page.get('name') != 'Registrasi':
            assert E.tostring(before_page) == E.tostring(after_page)
        else:
            before_cells = list(before_page.iter('mxCell'))
            after_cells = list(after_page.iter('mxCell'))
            assert len(before_cells) == len(after_cells)
            for before, after in zip(before_cells, after_cells):
                restored = deepcopy(after)
                restored.set('style', before.get('style')) if before.get('style') is not None else None
                equivalent(before, restored)
    OUTPUT.write_bytes(E.tostring(document, xml_declaration=True, encoding='UTF-8', pretty_print=True))
    assert sha256(SOURCE.read_bytes()).digest() == sha256(source_bytes).digest()
    print(json.dumps({'output':str(OUTPUT), 'page':'Registrasi', 'processesWithStyle':len(matched), 'newlyChanged':len(changed), 'otherPagesUnchanged':len(document)-1, 'sourceUnchanged':True}, indent=2))

if __name__ == '__main__':
    main()
