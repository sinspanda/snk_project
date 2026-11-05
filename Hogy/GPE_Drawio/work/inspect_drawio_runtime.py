import json
import struct
import sys
from pathlib import Path

ARCHIVE = Path(r'C:\Program Files\draw.io\resources\app.asar')

def index():
    with ARCHIVE.open('rb') as stream:
        sizes = struct.unpack('<4I', stream.read(16))
        header = json.loads(stream.read(sizes[3]))
    files = {}
    def walk(directory, prefix=''):
        for name, entry in directory.get('files', {}).items():
            path = prefix + '/' + name
            if 'files' in entry:
                walk(entry, path)
            else:
                files[path] = entry
    walk(header)
    return sizes[1] + 8, files

def read(path):
    base, files = index()
    entry = files[path]
    with ARCHIVE.open('rb') as stream:
        stream.seek(base + int(entry['offset']))
        return stream.read(entry['size']).decode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        content = read(sys.argv[1])
        if len(sys.argv) > 2:
            lines = content.splitlines()
            matched = {j for i, line in enumerate(lines) if sys.argv[2].lower() in line.lower() for j in range(max(0,i-2),min(len(lines),i+4))}
            print('\n'.join(f'{i+1}: {lines[i]}' for i in sorted(matched)))
        else:
            print(content)
    else:
        _, files = index()
        print('\n'.join(k for k in files if ('bpmn' in k.lower() or k.startswith('/src/main/') or k.endswith('export.html')) and 'node_modules' not in k))
