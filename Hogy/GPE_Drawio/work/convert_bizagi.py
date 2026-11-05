"""Preserve Bizagi's eight XPDL diagrams as editable, positioned draw.io objects."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import io
import json
import math
from pathlib import Path
import zipfile
from lxml import etree as E
from PIL import ImageFont

SOURCE = Path(r'C:\Users\SAYID\OneDrive\02. Project\GPE\10. Data Client\Flow Process\Plan to be\Plan to be\Asset To Be\Flow Asset to be 16.7.26.bpm')
DEST = Path(r'E:\Panda\Hogy\GPE_Drawio\Flow Asset to be 16.7.26.drawio')
NS = {'x': 'http://www.wfmc.org/2009/XPDL2.2'}

def find(node, path):
    return node.find(path, NS)

def many(node, path):
    return node.findall(path, NS)

def fmt(number):
    return f'{number:.5f}'.rstrip('0').rstrip('.') if number else '0'

def color(value, default='#000000'):
    return f'#{int(value) & 0xFFFFFF:06x}' if value is not None else default

def rich(text):
    return html.escape(text or '').replace('\r\n', '\n').replace('\r', '\n').replace('\n', '<br>')

def graphics(node, edge=False):
    return find(node, 'x:ConnectorGraphicsInfos/x:ConnectorGraphicsInfo' if edge else 'x:NodeGraphicsInfos/x:NodeGraphicsInfo')

def bounds(node):
    g = graphics(node)
    c = find(g, 'x:Coordinates')
    return tuple(float(v) for v in (c.get('XCoordinate', '0'), c.get('YCoordinate', '0'), g.get('Width'), g.get('Height')))

def label_bounds(g, fallback):
    return tuple(float(g.get(k, str(d))) for k, d in zip(('TextX', 'TextY', 'TextWidth', 'TextHeight'), fallback))

def text_style(g):
    f = find(g, 'x:Formatting')
    def field(name, default):
        n = find(f, 'x:' + name) if f is not None else None
        return n.text if n is not None and n.text else default
    font_bits = sum(bit for name, bit in [('Bold', 1), ('Italic', 2), ('Underline', 4), ('Strikeout', 8)] if field(name, 'false') == 'true')
    return (f'fontFamily={field("FontName", "Segoe UI")};fontSize={fmt(float(field("SizeFont", "8"))*4/3)};'
            f'fontColor={color(field("ColorFont", "-16777216"))};fontStyle={font_bits};'
            f'align={field("Alignment", "Center").lower()};verticalAlign=middle;whiteSpace=wrap;html=1;')

def style_colors(g):
    return f'strokeColor={color(g.get("BorderColor"))};fillColor={color(g.get("FillColor"), "#ffffff")};'

def task_label_size(text, box):
    """Fit text below the native 16px task marker without changing node bounds."""
    width, height = box[2]-9, box[3]-27
    for size in (10.66667, 10, 9.33333, 9, 8.66667, 8, 7.5):
        font = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', round(size*6))
        lines = 0
        for paragraph in text.replace('\r\n','\n').replace('\r','\n').split('\n'):
            row = ''
            for word in paragraph.split():
                candidate = (row + ' ' + word).strip()
                if row and font.getlength(candidate)/6 > width:
                    lines += 1
                    row = word
                else:
                    row = candidate
            lines += 1
        if lines*size*1.25 <= height:
            return size
    return 7.5

def vertex(root, identity, parent, value, style, box, source=None, kind=None):
    container = root
    if source is not None:
        attrs = {'id': identity, 'label': rich(value), 'sourceId': source.get('Id'),
                 'sourceType': kind or E.QName(source).localname, 'sourceName': source.get('Name', source.get('TextAnnotation', ''))}
        for tag in ('Description', 'Documentation'):
            content = find(source, 'x:' + tag)
            if content is not None and ''.join(content.itertext()).strip():
                attrs[tag.lower()] = ''.join(content.itertext())
        attrs['sourceProperties'] = json.dumps(dict(source.attrib), ensure_ascii=False)
        container = E.SubElement(root, 'object', **attrs)
    cell = E.SubElement(container, 'mxCell', **({'id': identity, 'value': rich(value)} if source is None else {}), style=style, parent=parent, vertex='1')
    E.SubElement(cell, 'mxGeometry', x=fmt(box[0]), y=fmt(box[1]), width=fmt(box[2]), height=fmt(box[3]), **{'as': 'geometry'})
    return cell

def midpoint(points):
    lengths = [math.dist(a, b) for a, b in zip(points, points[1:])]
    distance = sum(lengths) / 2
    for (a, b), length in zip(zip(points, points[1:]), lengths):
        if distance <= length and length:
            return tuple(x + (y-x)*distance/length for x,y in zip(a,b))
        distance -= length
    return points[0]

def activity_shape(a):
    event = find(a, 'x:Event')
    route = find(a, 'x:Route')
    if event is not None:
        subtype = event[0]
        name = E.QName(subtype).localname
        trigger = subtype.get('Trigger', subtype.get('Result', 'None'))
        outline = 'standard' if name == 'StartEvent' else 'end' if name == 'EndEvent' else 'catching'
        link = find(subtype, 'x:TriggerResultLink')
        if link is not None and link.get('CatchThrow') == 'THROW':
            outline = 'throwing'
        if trigger == 'Escalation':
            outline = 'throwing'
        symbol = {'None': 'general', 'Link': 'link', 'Signal': 'signal', 'Escalation': 'escalation'}.get(trigger)
        if symbol is None:
            raise ValueError(('Unhandled event', name, trigger))
        return f'shape=mxgraph.bpmn.event;outline={outline};symbol={symbol};perimeter=ellipsePerimeter;outlineConnect=0;', name + ':' + trigger
    if route is not None:
        typ = route.get('GatewayType', 'Exclusive')
        if typ == 'Inclusive':
            extra = 'outline=end;symbol=general;'
        elif typ == 'Parallel':
            extra = 'outline=none;symbol=none;gwType=parallel;'
        elif typ == 'Exclusive':
            extra = 'outline=none;symbol=none;' + ('gwType=exclusive;' if route.get('MarkerVisible') == 'true' else '')
        else:
            raise ValueError(('Unhandled gateway', typ))
        return 'shape=mxgraph.bpmn.gateway2;perimeter=rhombusPerimeter;outlineConnect=0;' + extra, 'Gateway:' + typ
    task = find(a, 'x:Implementation/x:Task')
    subtype = E.QName(task[0]).localname if task is not None and len(task) else 'Task'
    marker = {'Task': 'abstract', 'TaskService': 'service', 'TaskUser': 'user', 'TaskManual': 'manual', 'TaskReceive': 'receive'}[subtype]
    sub = find(a, 'x:Implementation/x:SubFlow') is not None
    shape = f'shape=mxgraph.bpmn.task2;rectStyle=rounded;size=10;taskMarker={marker};'
    if sub:
        shape += 'isLoopSub=1;'
    loop = find(a, 'x:Loop')
    if loop is not None and loop.get('LoopType', 'None') != 'None':
        raise ValueError(('Unhandled loop', dict(loop.attrib)))
    return shape, 'Subprocess' if sub else subtype

def convert_page(package, diagram_id, mxfile):
    page = E.SubElement(mxfile, 'diagram', id=diagram_id, name=package.get('Name'))
    model = E.SubElement(page, 'mxGraphModel', dx='1422', dy='794', grid='1', gridSize='10', guides='1', tooltips='1', connect='1', arrows='1', fold='1', page='0', pageScale='1', pageWidth='1169', pageHeight='827', math='0', shadow='0', background='#ffffff')
    root = E.SubElement(model, 'root')
    E.SubElement(root, 'mxCell', id='0')
    E.SubElement(root, 'mxCell', id='1', parent='0')
    positions, lanes, pool_processes = {}, [], {}
    counted = Counter()
    def choose_parent(box, process=None):
        x,y,w,h = box
        matches = [(lid, pbox) for lid, pbox, proc in lanes if (process is None or proc == process) and pbox[0] <= x+w/2 <= pbox[0]+pbox[2] and pbox[1] <= y+h/2 <= pbox[1]+pbox[3]]
        if matches:
            return matches[0]
        if process in pool_processes:
            pool_id = pool_processes[process]
            return pool_id, positions[pool_id]
        return '1', (0,0,0,0)
    for pool in many(package, 'x:Pools/x:Pool'):
        if pool.get('BoundaryVisible') == 'false':
            continue
        pid = pool.get('Id')
        box = bounds(pool)
        positions[pid] = box
        pool_processes[pool.get('Process')] = pid
        lane_nodes = many(pool, 'x:Lanes/x:Lane')
        start = bounds(lane_nodes[0])[0] if lane_nodes else 50
        pg = graphics(pool)
        vertex(root, pid, '1', pool.get('Name', ''), f'swimlane;horizontal=0;startSize={fmt(start)};collapsible=0;recursiveResize=0;container=1;swimlaneLine=1;swimlaneFillColor=#ffffff;strokeWidth=1;' + text_style(pg) + style_colors(pg), box, pool)
        counted['pools'] += 1
        for lane in lane_nodes:
            lid = lane.get('Id')
            lb = bounds(lane)
            ab = (box[0]+lb[0], box[1]+lb[1], lb[2], lb[3])
            positions[lid] = ab
            lanes.append((lid, ab, pool.get('Process')))
            lg = graphics(lane)
            vertex(root, lid, pid, lane.get('Name', ''), 'swimlane;horizontal=0;startSize=30;collapsible=0;recursiveResize=0;container=1;swimlaneLine=1;swimlaneFillColor=#ffffff;strokeWidth=1;' + text_style(lg) + style_colors(lg), lb, lane)
            counted['lanes'] += 1
    for tag, path in [('activities', './/x:Activity'), ('annotations', './/x:Artifact'), ('dataObjects', './/x:DataObject')]:
        for source in many(package, path):
            identity = source.get('Id')
            box = bounds(source)
            g = graphics(source)
            positions[identity] = box
            name = source.get('Name', source.get('TextAnnotation', ''))
            process_node = next((p for p in source.iterancestors() if E.QName(p).localname == 'WorkflowProcess'), None)
            process_id = process_node.get('Id') if process_node is not None else None
            parent, pbox = choose_parent(box, process_id)
            local_box = (box[0]-pbox[0], box[1]-pbox[1], box[2], box[3])
            if tag == 'activities':
                shape, kind = activity_shape(source)
            elif tag == 'annotations':
                shape, kind = 'shape=note;size=10;', 'Annotation'
            else:
                shape, kind = 'shape=mxgraph.bpmn.data2;size=10;', 'DataObject'
            tb = label_bounds(g, box)
            external_label = bool(name.strip()) and any(abs(a-b) > .01 for a,b in zip(tb,box))
            # Tasks have internal names. One source task has stale TextX after a move.
            if kind.startswith('Task'):
                external_label = False
            style = shape + text_style(g) + style_colors(g) + 'strokeWidth=1;spacing=3;'
            if kind in ('TaskService', 'TaskUser', 'TaskManual', 'TaskReceive'):
                style += f'spacingTop=19;fontSize={fmt(task_label_size(name,box))};'
            vertex(root, identity, parent, '' if external_label else name, style, local_box, source, kind)
            if external_label:
                label = vertex(root, identity+'-label', identity, name, 'text;strokeColor=none;fillColor=none;spacing=0;' + text_style(g), (tb[0]-box[0],tb[1]-box[1],tb[2],tb[3]))
                label.set('connectable','0')
            counted[tag] += 1
    for tag, path in [('transitions', './/x:Transition'), ('associations', './/x:Association')]:
        for source in many(package, path):
            identity = source.get('Id')
            src, tgt = (source.get('From'), source.get('To')) if tag == 'transitions' else (source.get('Source'), source.get('Target'))
            assert src in positions and tgt in positions, (package.get('Name'), identity, src,tgt)
            g = graphics(source, True)
            points = [(float(p.get('XCoordinate')), float(p.get('YCoordinate'))) for p in many(g, 'x:Coordinates')]
            assert len(points) >= 2, identity
            style = 'edgeStyle=none;noEdgeStyle=1;rounded=0;html=1;' + text_style(g) + f'strokeColor={color(g.get("BorderColor"))};strokeWidth=1;'
            if tag == 'transitions':
                style += 'endArrow=block;endFill=1;endSize=6;'
            else:
                style += 'dashed=1;dashPattern=3 3;startArrow=none;endArrow=none;'
            for prefix, point, node_id in [('exit', points[0], src), ('entry', points[-1], tgt)]:
                box = positions[node_id]
                style += f'{prefix}X={fmt((point[0]-box[0])/box[2])};{prefix}Y={fmt((point[1]-box[1])/box[3])};{prefix}Dx=0;{prefix}Dy=0;{prefix}Perimeter=0;'
            name = source.get('Name', '')
            ob = E.SubElement(root, 'object', id=identity, label=rich(name), sourceId=identity, sourceType=tag, sourceName=name, sourceProperties=json.dumps(dict(source.attrib),ensure_ascii=False))
            cell = E.SubElement(ob, 'mxCell', edge='1', parent='1', source=src, target=tgt, style=style)
            geometry = E.SubElement(cell, 'mxGeometry', relative='1', **{'as':'geometry'})
            if len(points)>2:
                array = E.SubElement(geometry,'Array', **{'as':'points'})
                for x,y in points[1:-1]:
                    E.SubElement(array, 'mxPoint', x=fmt(x), y=fmt(y))
            if name:
                tb = label_bounds(g, (points[0][0],points[0][1],90,30))
                mid = midpoint(points)
                E.SubElement(geometry,'mxPoint', x=fmt(tb[0]+tb[2]/2-mid[0]), y=fmt(tb[1]+tb[3]/2-mid[1]), **{'as':'offset'})
                cell.set('style', style + f'labelWidth={fmt(tb[2])};labelBackgroundColor=#ffffff;')
            counted[tag] += 1
    ids = [n.get('id') for n in root.iter() if n.get('id')]
    assert len(ids) == len(set(ids)), ('duplicate id', package.get('Name'))
    for cell in root.iter('mxCell'):
        for attribute in ('parent', 'source', 'target'):
            if cell.get(attribute):
                assert cell.get(attribute) in ids
    return {'name': package.get('Name'), **dict(counted), 'drawioObjectsIncludingLabels': len(ids)-2}

def main():
    data = SOURCE.read_bytes()
    archive = zipfile.ZipFile(io.BytesIO(data))
    preferences = E.fromstring(archive.read('Users/Default/UserPreferences.xml'))
    order = [n.get('DiagramId') for n in preferences.findall('.//ModelItem')]
    remaining = [Path(n).stem for n in archive.namelist() if n.endswith('.diag') and Path(n).stem not in order]
    order += remaining
    mxfile = E.Element('mxfile', host='app.diagrams.net', modified=datetime.now(timezone.utc).isoformat(), agent='Bizagi XPDL geometry-preserving converter', version='29.7.9', type='device', compressed='false', pages=str(len(order)))
    reports = []
    for diagram_id in order:
        nested = zipfile.ZipFile(io.BytesIO(archive.read(diagram_id+'.diag')))
        package = E.fromstring(nested.read('Diagram.xml'))
        reports.append(convert_page(package, diagram_id, mxfile))
    DEST.parent.mkdir(parents=True, exist_ok=True)
    E.ElementTree(mxfile).write(str(DEST),encoding='UTF-8',xml_declaration=True,pretty_print=True)
    assert hashlib.sha256(SOURCE.read_bytes()).digest() == hashlib.sha256(data).digest()
    report = {'source': str(SOURCE), 'sourceSha256':hashlib.sha256(data).hexdigest(), 'output':str(DEST), 'pages':reports,
              'verification':'All visible process nodes, lanes, transitions, annotations, data objects and associations preserved. All endpoints resolve. Source unchanged.',
              'scope':'Editable diagram conversion. Bizagi execution and simulation settings are not draw.io executable semantics.'}
    DEST.with_suffix('.qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
