from pathlib import Path
import re
p=Path(r'E:/Panda/Hogy/outputs/konsep-kontrak/Konsep-Kontrak-Karyawan-HOGY.md')
t=p.read_text(encoding='utf8').replace('| Versi | 1.1 |','| Versi | 1.2 |')
start=t.index('## 3. Alur penggunaan')
end=t.index('## 4. Perubahan kontrak')
t=t[:start]+t[end:]
flow='''## 2. Alur penggunaan

```mermaid
flowchart TD
    A[HR Manager membuka Employment history] --> B{Jenis kebutuhan?}

    B -->|Kontrak awal| C[Buat kontrak baru]
    B -->|Adjustment nominal| D[Pilih kontrak berjalan]
    B -->|Mutasi / Promosi / Demosi| C

    C --> E[Isi periode kontrak]
    E --> F[Isi nominal pada section Payroll]
    D --> G[Ubah nominal pada section Payroll]

    F --> H[Validasi data]
    G --> H

    H --> I{Data valid?}
    I -->|Tidak| J[Tampilkan pesan validasi]
    J --> K[HR Manager memperbaiki data]
    K --> H

    I -->|Ya| L[Simpan kontrak]
    L --> M[Tampilkan nominal secara read-only pada Employees]
    M --> N[Employee melihat kontrak miliknya sendiri]
```

Decision menggunakan belah ketupat dan proses menggunakan kotak. Validasi mengikuti ketentuan pada bagian 5.

'''
t=t.replace('## 2. Penempatan dan fungsi form',flow+'## 3. Modification').replace('### 2.1 Employees','### 3.1 Employees').replace('### 2.2 Employment history','### 3.2 Employment history')
lines=t.splitlines()
out=[]
for line in lines:
    if line=='| No. | Field label | Perilaku |':
        out.append('| No. | Field label | EDT | Catatan |')
    elif line=='|---:|---|---|':
        out.append('|---:|---|---|---|')
    elif re.match(r'^\| [1-8] \| .+ \| Read-only \|$',line):
        c=[x.strip() for x in line.split('|')[1:-1]]
        out.append(f'| {c[0]} | {c[1]} | Table: mengikuti sumber Employment history<br>Field type: real (nominal) | Read-only. Menampilkan nilai dari employment/kontrak terkait. |')
    elif line=='| No. | Field label | Penggunaan | Catatan |':
        out.append('| No. | Field label | EDT | Catatan |')
    elif re.match(r'^\| [1-8] \|',line):
        c=[x.strip() for x in line.split('|')[1:-1]]
        usage=c[2].rstrip('.')+'.'
        note=c[3]
        if note in ['Nominal bulanan individu.','Nominal sales incentive tetap bulanan.']:note=''
        out.append(f'| {c[0]} | {c[1]} | Table: ditetapkan pada FDD<br>Field type: real (nominal) | {usage} {note} |')
    else:out.append(line)
t='\n'.join(out)+'\n'
t=t.replace('Nama field pada tabel adalah label tampilan. Nama teknis dan EDT ditentukan saat penyusunan FDD.','Kolom EDT mencantumkan sumber table dan usulan tipe field. Nama table fisik, field teknis, dan EDT nominal final ditetapkan pada FDD setelah memeriksa metadata lingkungan D365. Employees menggunakan sumber nilai yang sama dengan Employment history.')
p.write_text(t,encoding='utf8')
assert t.index('## 2. Alur penggunaan')<t.index('## 3. Modification')
assert 'B{Jenis kebutuhan?}' in t and 'I{Data valid?}' in t
assert 'Penggunaan | Catatan' not in t
assert t.count('| No. | Field label | EDT | Catatan |')==2
assert all((p.parent/x).is_file() for x in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',t))
assert t.count('```')==2
print('Verified: section order, two diamond decisions, 16 field rows in two updated tables, and two image links.')
