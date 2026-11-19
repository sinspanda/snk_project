# Technical Implementation Plan Bank Book

## 1. Identitas dan tujuan

- Project: MITO — PT MAHAKARYA SUKSES INDONESIA.
- Platform: Odoo 18 Enterprise.
- Versi plan: 1.1, 19 November 2026.
- Status: scope berdasarkan summary yang disetujui; source code existing belum diperiksa pada penyusunan plan ini.
- Tujuan: menyediakan Bank Book interaktif untuk memantau Opening, detail mutasi, dan Ending atas Account In/Out journal yang diizinkan untuk user.
- Konfirmasi terbaru: `res.users.snk_allowed_journal_ids`, tipe `many2many`, sudah disepakati. Field ini bukan lagi usulan.

Dokumen ini adalah panduan pekerjaan tech, bukan pernyataan bahwa fitur sudah diimplementasikan. Nama handler, XML ID, dependency custom, dan field Account In/Out wajib diperoleh dari source existing sebelum coding.

## 2. Scope final

1. Tambahkan Allowed Journals pada User, setelah Operating Unit.
2. Tambahkan menu Accounting > Reporting > Statement Reports > Bank Book, setelah Tax Return.
3. Gunakan tampilan accounting report seperti General Ledger dengan filter toolbar, tanpa wizard Generate.
4. Journal pilihan menentukan Account In/Out; transaksi diambil berdasarkan account hasil mapping, termasuk transaksi dari journal asal lain.
5. Kelompokkan report per Account dengan Opening, detail, dan Ending.
6. Sediakan Search serta ekspor PDF dan XLSX.
7. Tidak membuat model bisnis header–lines atau tabel tampungan transaksi. Definisi report dan abstract handler mengikuti framework existing.

Pembatasan Allowed Journals pada fitur ini tidak otomatis mengubah hak akses Journal Entries, Chart of Accounts, atau report accounting lain.

## 3. Pemeriksaan source sebelum development

| ID | Pemeriksaan | Output wajib |
| --- | --- | --- |
| DISC-01 | Temukan module accounting report dan handler General Ledger pada source Odoo Enterprise 18 yang digunakan | Catat module, model, method, report/action XML ID, dan mekanisme extension yang benar |
| DISC-02 | Temukan field Account In dan Account Out pada journal | Catat nama teknis, model pemilik, comodel, company, dan module penyedia; jangan mengasumsikan default account journal sebagai penggantinya |
| DISC-03 | Temukan field Operating Unit dan view User yang digunakan | Catat field dan inherited view XML ID untuk posisi Allowed Journals |
| DISC-04 | Periksa pengelolaan user melalui Roles | Pastikan pembaruan Roles tidak menghapus Allowed Journals |
| DISC-05 | Periksa ACL dan record rules journal, account, Journal Item, company, serta Operating Unit | Dokumentasikan konflik terhadap kebutuhan transaksi lintas journal dan penyelesaiannya |
| DISC-06 | Periksa pipeline filter, unfold/load-more, PDF, dan XLSX existing | Tetapkan titik extension tanpa menebak API atau menggandakan engine report |

Selesaikan DISC-01 sampai DISC-06 sebelum mengunci desain teknis. Jika existing rule membatasi transaksi yang seharusnya masuk, sampaikan ke functional untuk keputusan akses; jangan diam-diam menampilkan saldo parsial.

## 4. Rencana komponen module

Nama module `snk_bank_book` adalah usulan; sesuaikan naming repository. Struktur berikut merupakan rencana, bukan API existing yang telah diverifikasi.

```text
snk_bank_book/
  __init__.py
  __manifest__.py
  models/
    __init__.py
    res_users.py
  report/
    __init__.py
    bank_book_handler.py
  views/
    res_users_views.xml
    bank_book_menu.xml
  data/
    bank_book_report.xml
  security/
    bank_book_security.xml
```

Gunakan dependency accounting/report, module Operating Unit, Roles, dan penyedia Account In/Out sesuai hasil discovery. Tambahkan ACL hanya bila ada model yang memerlukannya; abstract handler tidak dijadikan tabel transaksi. Tambahkan template export atau asset UI hanya bila framework existing belum memenuhi kebutuhan.

## 5. Model dan konfigurasi User

| No | Field Label | EDT/Type | Note |
| --- | --- | --- | --- |
| 1 | Allowed Journals | Model: `res.users`<br>Field: `snk_allowed_journal_ids`<br>Type: `many2many` | Relation: `account.journal`. Stored, widget tags, posisi setelah Operating Unit. Identitas field disepakati. |

Ketentuan implementasi:

- Batasi pilihan konfigurasi pada journal dari company yang dapat diakses user terkait.
- Jangan membatasi pilihan hanya journal bertipe Bank atau Cash; jenis journal dibiarkan terbuka.
- Administrator berwenang dapat mengubah field; user biasa tidak dapat memberi akses journal kepada dirinya sendiri.
- Terapkan pembatasan write di server; readonly pada view saja tidak cukup.
- Tentukan relation table M2M mengikuti konvensi module dan hindari benturan dengan existing field.
- Allowed Journals kosong menghasilkan pesan konfigurasi, bukan akses ke seluruh journal.
- Perubahan Roles harus mempertahankan nilai Allowed Journals.

## 6. Filter dan parameter report

Parameter disimpan sebagai options report, bukan header bisnis atau data transaksi baru. Nama key di bawah adalah usulan dan harus disesuaikan framework existing.

| Parameter | Nama usulan | Perilaku |
| --- | --- | --- |
| Company | `company_id` | Satu company aktif yang diizinkan; perhitungan dan mata uang mengikuti company ini |
| Period | `date_from`, `date_to` | Batas inklusif untuk detail; tolak tanggal awal setelah tanggal akhir |
| Journals | `journal_ids` | Multi-select, subset Allowed Journals pada company aktif |
| Entries | `entries` | Posted = posted; All = posted dan draft; canceled dikecualikan |
| Search field | `search_field` | Account, journal asal, partner, atau journal entry |
| Search value | `search_value` | Nilai pencarian untuk field yang dipilih |

- Default Entries: Posted.
- Default periode bulan berjalan dan seluruh journal valid: usulan yang masih perlu dikunci functional sebelum implementasi default.
- Jika journal pilihan kosong, minta user memilih atau memperbaiki konfigurasi; jangan membuang pembatas journal secara otomatis.
- Saat Company berubah, hitung ulang pilihan journal valid dan keluarkan pilihan yang tidak sesuai.
- Perubahan filter memperbarui report langsung tanpa Generate, Save, atau Discard report.
- Date pada detail tetap satu kolom tanggal transaksi; date_from/date_to merupakan parameter periode, bukan dua tanggal pada setiap transaksi.

## 7. Algoritma sumber data

### 7.1 Validasi dan mapping

1. Identifikasi user request di server; jangan menerima user pemilik akses dari client sebagai otoritas.
2. Validasi Company terhadap company yang boleh diakses user.
3. Ambil Allowed Journals user, batasi pada Company aktif.
4. Validasi journal pilihan merupakan subset dari daftar tersebut. Tolak ID tidak valid atau tidak berizin, termasuk request yang dimanipulasi.
5. Baca Account In/Out setiap journal melalui field existing hasil DISC-02.
6. Gabungkan seluruh account yang terisi menjadi himpunan account unik; validasi kesesuaiannya dengan Company.
7. Jika hanya satu sisi In/Out terisi, gunakan account yang tersedia. Jika hasil mapping keseluruhan kosong, tampilkan pesan konfigurasi.

### 7.2 Domain transaksi

Sumber detail adalah `account.move.line`. Batasi menggunakan account hasil mapping, Company aktif, status Entries, serta tanggal sesuai kebutuhan agregasi/detail.

**Jangan menambahkan domain journal asal = journal pilihan.** Journal pilihan hanya dipakai untuk memperoleh account. Journal asal lain tetap masuk bila Journal Item menggunakan account hasil mapping.

- Satu detail mewakili satu Journal Item, bukan satu Journal Entry atau total per partner.
- Account yang dipetakan oleh beberapa journal ditampilkan sekali.
- Account In = Account Out tidak menyebabkan penghitungan ganda.
- Hindari join ke daftar mapping yang menggandakan Journal Item.
- Urutan detail: `date ASC, id ASC`.
- Terapkan filter company dan Entries yang sama pada saldo awal dan transaksi periode.
- Parameterisasi query jika SQL diperlukan; jangan menyusun input Search/ID langsung ke string SQL.

## 8. Perhitungan dan kolom

| Baris | Debit | Credit | Balance |
| --- | --- | --- | --- |
| Opening | Kosong | Kosong | SUM(debit − credit) dengan date < date_from |
| Detail | Debit Journal Item | Credit Journal Item | Debit − Credit pada baris tersebut |
| Ending | Total debit periode | Total credit periode | Opening + total debit periode − total credit periode |

Detail periode memenuhi `date_from <= date <= date_to`. Balance detail bukan running balance. Angka pada header grup Account tidak ditambahkan sebagai ringkasan baru; ringkasan hanya Opening dan Ending.

| Kolom | Sumber atau perilaku |
| --- | --- |
| Account | Grup dari `account.move.line.account_id`; tampilkan kode dan nama |
| Date | `account.move.line.date` |
| Journal Entry / Move | `account.move.line.move_id`; tampilkan nomor move dan link mengikuti akses sumber |
| Journal | `account.move.line.journal_id`; journal asal transaksi |
| Partner | `account.move.line.partner_id`; boleh kosong |
| Label / Ref | Label dari `account.move.line.name`; tetapkan fallback reference move setelah memeriksa field existing |
| Debit | `account.move.line.debit` |
| Credit | `account.move.line.credit` |
| Balance | Nilai mutasi baris; Opening/Ending dihitung oleh report |

Gunakan nilai company currency untuk debit/credit/balance. Jangan menjumlahkan nominal berbagai transaction currency secara langsung. Semua nilai report readonly.

## 9. Search dan expand detail

- Account: kode/nama account.
- Journal: kode/nama journal asal transaksi; berbeda dari selector Journals untuk mapping account.
- Partner: nama partner.
- Journal Entry: nomor move.
- Search menyaring detail terlihat saja; tidak mengubah Opening, total mutasi periode, dan Ending.
- Search Account tetap berada di dalam account hasil mapping; tidak membuka account di luar cakupan izin.
- Tampilkan keterangan ketika Search aktif: ringkasan memakai cakupan periode penuh, sehingga detail hasil Search dapat berbeda dari total periode.
- Expand/collapse dan load-more tidak boleh mengubah saldo, menggandakan atau melewatkan detail.
- Hitung ringkasan terhadap seluruh transaksi yang memenuhi cakupan periode, bukan hanya halaman detail yang sedang termuat.

## 10. PDF dan XLSX

- Sediakan tombol PDF dan XLSX pada toolbar report.
- Gunakan satu logika validasi, mapping, domain, dan perhitungan untuk layar maupun kedua format export.
- Cantumkan Company, periode, journal pilihan, Entries, currency, dan Search aktif.
- Export Opening, detail sesuai Search, serta Ending dan total periode penuh; sertakan penjelasan perilaku Search.
- Detail yang memenuhi filter/Search tetap diekspor walaupun grup collapse atau belum dimuat seluruhnya di layar.
- Nilai XLSX harus numerik, bukan string dengan awalan Rp; tanggal harus berupa nilai tanggal Excel.
- Verifikasi page header, pemotongan tabel, format nominal, serta pengulangan header kolom PDF.

## 11. Keamanan dan performa

- Validasi ulang izin pada report awal, refresh, expand/load-more, pembukaan sumber, PDF, dan XLSX.
- Hasil request setelah akses dicabut harus mengikuti izin terbaru; jangan memakai cache tanpa mempertimbangkan user, company, options, dan perubahan akses.
- Bedakan hak membaca report dari hak membuka Journal Entry sumber. Link yang ditolak tidak mengubah perhitungan saldo.
- Selesaikan konflik record rules lintas journal sebelum rilis; jangan melakukan bypass menyeluruh dengan sudo atau mengabaikan rule melalui SQL.
- Gunakan agregasi database per account untuk Opening dan total periode; hindari query per Journal Item.
- Gunakan mekanisme pemuatan detail framework untuk layar; export harus tetap lengkap.
- Evaluasi query plan dan index existing dengan volume UAT representatif sebelum menambahkan index baru.
- Ukur waktu report dan export menggunakan dataset yang disepakati; tidak menetapkan SLA numerik tanpa baseline.

## 12. Work packages dan urutan implementasi

| ID | Pekerjaan | Dependency | Kriteria selesai |
| --- | --- | --- | --- |
| WP-01 | Discovery source DISC-01–06 | Akses source dan environment development | Identitas teknis, dependency, serta potensi konflik akses terdokumentasi |
| WP-02 | Tambah field User dan view | WP-01 | Field tersimpan, posisi benar, pengubahan izin terlindungi, tidak hilang saat update Roles |
| WP-03 | Tambah definisi report, menu dan handler | WP-01 | Menu setelah Tax Return, report GL terbuka tanpa wizard |
| WP-04 | Implementasi options, validasi dan mapping account | WP-02, WP-03 | Journal terotorisasi, account unik dan pesan konfigurasi sesuai |
| WP-05 | Implementasi query, saldo dan detail | WP-04 | Transaksi lintas journal masuk, saldo dan urutan detail benar |
| WP-06 | Implementasi Search dan unfold/load-more | WP-05 | Detail tersaring, ringkasan tetap, tidak ada duplikasi pagination |
| WP-07 | Integrasi PDF dan XLSX | WP-05, WP-06 | Output konsisten dan seluruh detail relevan diekspor |
| WP-08 | Pengujian manual keamanan, regresi dan performa | WP-02–07 | Skenario berikut lolos dan bukti hasil dicatat |
| WP-09 | UAT Accounting dan perbaikan | WP-08 | Hasil UAT diterima functional/Accounting |
| WP-10 | Deployment dan pemeriksaan hasil | WP-09 | Konfigurasi akses diisi dan saldo sampel sesuai hasil UAT |

Estimasi mandays, PIC, serta tanggal deployment ditetapkan setelah WP-01; tidak diasumsikan dalam plan ini.

## 13. Skenario pengujian manual dan UAT

| ID | Skenario | Expected result |
| --- | --- | --- |
| TC-01 | Admin mengisi Allowed Journals lalu membuka ulang user dan memperbarui Roles | Nilai tetap tersimpan |
| TC-02 | User biasa mencoba mengubah akses journal sendiri melalui UI/request langsung | Ditolak di server |
| TC-03 | Allowed Journals kosong atau semua journal pilihan tidak sesuai company | Pesan konfigurasi/pilihan; tidak mengambil seluruh journal |
| TC-04 | Manipulasi request dengan journal/account/company tidak berizin | Ditolak atau dibatasi server tanpa membocorkan data |
| TC-05 | Journal A memetakan account X; transaksi account X berasal dari Journal C | Transaksi Journal C tetap masuk |
| TC-06 | Journal A dan B memetakan account sama, termasuk In = Out | Account dan Journal Item dihitung sekali |
| TC-07 | Opening 100 juta; debit 25 juta; credit 10 juta; debit 15 juta | Balance detail 25 juta, −10 juta, 15 juta; Ending 130 juta; total debit 40 juta, credit 10 juta |
| TC-08 | Transaksi sebelum From, tepat From, tepat To, dan setelah To | Sebelum From masuk Opening; From/To masuk detail; setelah To dikecualikan |
| TC-09 | Posted dibanding All dengan transaksi draft dan canceled | All menambah draft; canceled tidak masuk; aturan konsisten pada Opening dan detail |
| TC-10 | Search account, journal asal, partner, dan move secara terpisah | Detail sesuai pencarian; ringkasan tetap; keterangan tampil |
| TC-11 | Salah satu Account In/Out kosong lalu seluruh mapping kosong | Satu account tetap dipakai; seluruh mapping kosong menghasilkan pesan |
| TC-12 | Tidak ada transaksi periode tetapi ada Opening | Ringkasan tetap valid; Ending sama dengan Opening |
| TC-13 | Expand/collapse, load-more dan export dengan Search aktif | Tidak ada detail ganda/terlewat; export lengkap sesuai Search meski collapse |
| TC-14 | Company berubah atau akses dicabut saat report masih terbuka | Journal/options divalidasi ulang; data mengikuti izin terbaru |
| TC-15 | Link move yang tidak dapat dibuka oleh user | Pembukaan ditolak mengikuti hak sumber tanpa mengubah saldo |
| TC-16 | Bandingkan layar, PDF, dan XLSX pada options identik | Account, Opening, total periode, detail sesuai Search, dan Ending konsisten |

Jalankan skenario di atas secara manual melalui aplikasi dan pemeriksaan hasil oleh tech/functional, kemudian UAT Accounting. Jangan membuat folder tests/, file test_*.py, atau automated testing Python untuk scope ini. Catat hasil aktual dan bukti pengujian; jangan mengisi PASS sebelum skenario dijalankan.

## 14. Checklist deployment

- [ ] Kunci field Account In/Out, XML ID, handler, dependency module, dan keputusan default options.
- [ ] Selesaikan keputusan akses jika existing rules berbenturan dengan cakupan transaksi lintas journal.
- [ ] Lakukan backup dan uji upgrade module pada staging.
- [ ] Upgrade module tanpa mengubah saldo/transaksi accounting existing.
- [ ] Isi Allowed Journals user yang membutuhkan Bank Book melalui administrator berwenang.
- [ ] Verifikasi mapping Account In/Out journal terkait dan company-nya.
- [ ] Cocokkan report sampel dengan data Journal Items sebagai sumber pembanding.
- [ ] Uji PDF/XLSX menggunakan user operasional, bukan hanya administrator.
- [ ] Dapatkan konfirmasi hasil UAT dan persetujuan jadwal rilis.
- [ ] Setelah rilis, ulangi pemeriksaan menu, izin, saldo sampel, dan export.

Jika deployment bermasalah, ikuti prosedur rollback repository/environment yang sudah diuji. Jangan menghapus transaksi atau mengubah saldo sebagai langkah rollback fitur report.

## 15. Definition of done

Fitur selesai ketika seluruh scope final tersedia, izin tervalidasi server, transaksi account dari journal lain tetap tercakup, saldo sesuai rumus, Search dan export konsisten, tidak ada data ganda, serta hasil UAT diterima. Tech menyerahkan source module, catatan dependency/konfigurasi, hasil pengujian, dan panduan deployment singkat.
