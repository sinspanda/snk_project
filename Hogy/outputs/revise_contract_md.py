from pathlib import Path
import re
p=Path(r'E:/Panda/Hogy/outputs/konsep-kontrak/Konsep-Kontrak-Karyawan-HOGY.md')
t=p.read_text(encoding='utf8').replace('| Versi | 1.0 |','| Versi | 1.1 |').replace('| Status | Konsep untuk review |','| Status | Konsep untuk pembahasan teknis |')
t=t.replace('Adjustment nominal dilakukan melalui kontrak baru. Kontrak lama menjadi riwayat, tanpa membuat versi nominal tambahan di dalam satu kontrak.','Adjustment nominal dapat dilakukan pada kontrak yang sedang berjalan. Perubahan terkait mutasi, promosi, demosi, atau perubahan penugasan sejenis menggunakan kontrak baru.')
start=t.index('Desain mengikuti dua layar standard')
end=t.index('### 2.1 Mockup Employees')
t=t[:start]+t[end:]
t=t.replace('### 2.1 Mockup Employees','### 2.1 Employees\n\nPada **Employees > Work history**, tambahkan subtab **Payroll** di dalam employment terkait, di antara **Employment details** dan **Financial dimensions**.')
t=t.replace('### 2.2 Mockup Employment history','### 2.2 Employment history\n\nPada **Employment history**, tambahkan section **Payroll** di bawah **General** dan di atas **Financial dimensions**. Section ini menjadi tempat HR Manager memelihara nominal komponen gaji tetap individu.')
fields=t[t.index('Semua field berikut'):t.index('## 5. Pembagian kontrak dan payroll')]
fields=fields.replace('Jika tarif sepenuhnya seragam per jabatan, penempatan nilainya dapat dipindahkan ke setting payroll setelah dikonfirmasi.','Nominal bulanan individu.').replace('Masih perlu konfirmasi. Jika berdasarkan target/penjualan, kelola melalui formula payroll.','Nominal sales incentive tetap bulanan.').replace('Jika tarif seragam per skill, dapat menggunakan tabel payroll setelah dikonfirmasi.','Nominal bulanan individu.').replace('Jika tarif seragam untuk seluruh UO, dapat menggunakan master rate payroll setelah dikonfirmasi.','Nominal bulanan individu.')
start=t.index('## 3. Informasi kontrak')
end=t.index('## 6. Alur penggunaan')
t=t[:start]+fields+'\n'+t[end:]
labels=['Basic Salary','Fixed Transport Allowance','Position Allowance','Fixed Incentive','USD Allowance','Sales Incentive','Skill Allowance','Utility Operator Allowance']
table='Field yang ditampilkan pada subtab Payroll:\n\n| No. | Field label | Perilaku |\n|---:|---|---|\n'+''.join(f'| {i} | {x} | Read-only |\n' for i,x in enumerate(labels,1))+'\n'
anchor='Field nominal ditampilkan sebagai read-only.'
t=t.replace(anchor,table+anchor)
t=t.replace('Section Payroll berisi delapan field nominal.','Field yang ditambahkan pada section Payroll dijabarkan pada tabel berikut.')
t=t.replace('7. Jika ada adjustment, HR Manager membuat kontrak baru.','7. Untuk adjustment nominal, HR Manager dapat memperbarui kontrak berjalan. Untuk mutasi, promosi, demosi, atau perubahan penugasan sejenis, HR Manager membuat kontrak baru.')
t=t.replace('6. Payroll membaca nominal dari kontrak yang berlaku sesuai periode perhitungan. Status dan saat record dapat dibaca payroll masih perlu ditentukan.','6. Nilai yang ditampilkan pada Employees mengikuti record employment/kontrak terkait yang sedang dibuka.')
start=t.index('Satu kontrak mewakili satu paket nominal')
end=t.index('## 8. Validasi dan hak akses')
t=t[:start]+'''| Jenis perubahan | Perlakuan |
|---|---|
| Adjustment nominal pada kontrak berjalan | HR Manager dapat mengubah nominal pada kontrak yang sedang berjalan. Tidak selalu membuat kontrak baru. |
| Mutasi | Membuat kontrak baru sesuai perubahan penugasan dan periode berlakunya. |
| Promosi | Membuat kontrak baru sesuai posisi dan nominal yang ditetapkan. |
| Demosi | Membuat kontrak baru sesuai posisi dan nominal yang ditetapkan. |
| Perubahan penugasan sejenis | Membuat kontrak baru sesuai perubahan terkait. |

Untuk perubahan melalui kontrak baru, kontrak lama tetap menjadi riwayat. Nominal pada Employees mengikuti record employment/kontrak terkait yang sedang dibuka.

'''+t[end:]
t=t.replace('| Adjustment | Perubahan paket nominal menggunakan kontrak baru. | Tidak membuat versi nominal tambahan di dalam kontrak lama. |','| Adjustment | Perubahan nominal dapat dilakukan pada kontrak berjalan oleh HR Manager. Mutasi, promosi, demosi, dan perubahan penugasan sejenis menggunakan kontrak baru. | Validasi nominal saat perubahan pada kontrak berjalan. Terapkan validasi tanggal dan overlap ketika membuat kontrak baru. |')
start=t.index('## 9. Keputusan yang masih terbuka')
end=t.index('## 10. Referensi')
t=t[:start]+t[end:]
t=t.replace('## 6. Alur penggunaan','## 3. Alur penggunaan').replace('## 7. Perubahan dan histori','## 4. Perubahan kontrak').replace('## 8. Validasi dan hak akses','## 5. Validasi dan hak akses').replace('## 10. Referensi','## 6. Referensi')
t=t.replace('Dokumen ini menjadi dasar penyusunan FDD setelah keputusan terbuka disepakati. Mockup menunjukkan usulan tampilan, bukan perubahan yang sudah diterapkan pada D365.','Dokumen ini menjadi dasar pembahasan teknis dan penyusunan FDD kontrak karyawan. Mockup menunjukkan usulan tampilan untuk pengembangan.')
t=t.replace('Akses proses payroll ditentukan terpisah.','')
p.write_text(t,encoding='utf8')
assert all((p.parent/x).is_file() for x in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',t))
assert not any(x in t for x in ['## 3. Informasi kontrak','Pembagian kontrak dan payroll','Keputusan yang masih terbuka','Adjustment nominal dilakukan melalui kontrak baru.'])
print('Verified revised sections, adjustment rules, 8 field labels and both image references.')
