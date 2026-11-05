# REQUIREMENT DOCUMENT
## GPE | HRIS, People & Payroll

Document ID: GPE-URD-HRIS-001
Versi: 0.1 - Draft for Review
Tanggal penyusunan: 2 September 2026
Referensi pembahasan: MOM 18, 21, dan 22 Juli 2026
Lingkup organisasi: AKP, GAM, dan Head Office
Klasifikasi: Internal - bahan review GPE dan tim implementasi

> Dokumen ini menerjemahkan summary MOM menjadi kebutuhan bisnis dan fungsional untuk review. Dokumen ini belum merupakan baseline yang disetujui, desain teknis final, komitmen jadwal, atau persetujuan biaya implementasi.

### Tujuan dokumen

Menyediakan acuan bersama untuk memvalidasi kebutuhan HRIS, menetapkan batas proses, menyiapkan fit-gap Odoo, serta menyusun skenario User Acceptance Test (UAT). Informasi yang belum konsisten atau belum tersedia tetap dicatat sebagai keputusan terbuka, bukan diasumsikan sudah disepakati.

### Dasar penyusunan

Sumber utama adalah summary MOM dalam percakapan yang dirangkum dari dokumen “18072026 MOM - GPE - UREQ HRIS PEOPLE  PAYROLL (Jaga).docx”. Rujukan sumber menggunakan topik, bukan nomor halaman, karena halaman sumber belum diverifikasi secara visual.

Kode sumber: S1 Payroll dan attendance; S2 Recruitment dan manpower planning; S3 Cuti, perubahan status, dan administrasi karyawan; S4 Layanan GA; S5 Asset, pengadaan, dan exit clearance; S6 Accounting, loan, dan cash advance. Rincian pendukung menggunakan judul topik pada MOM asli.

### Cara membaca

- Tercatat: kebutuhan disebutkan pada summary/MOM; tetap membutuhkan review dan persetujuan bisnis.
- Terbuka: tujuan kebutuhan tercatat, tetapi sebagian aturan atau alurnya belum final; lihat kode D pada daftar keputusan.
- Usulan: kontrol, kriteria pengujian, atau pendekatan implementasi yang ditambahkan untuk kelengkapan requirement; bukan keputusan rapat.
- Kriteria penerimaan pada setiap requirement merupakan usulan terukur untuk review. Angka payroll/rate yang belum disetujui harus memakai test fixture yang ditandatangani pemilik proses.
- Seluruh requirement belum memiliki komitmen fase atau prioritas delivery. Penetapannya dilakukan setelah fit-gap dan persetujuan scope.

### Navigasi dokumen

Konteks dan scope; peran dan akses; requirement fungsional; integrasi dan data; reporting; non-functional requirement; UAT; keputusan terbuka; kebutuhan data GPE; persetujuan baseline.

---

# Konteks dan batas scope

## Kondisi saat ini

Data attendance, roster, SPL, insentif, dan payroll masih diproses melalui kombinasi fingerprint export, Excel, form manual, serta pertukaran data site-HO. Payroll menggunakan slip bayangan untuk koreksi sebelum finalisasi. Layanan GA memiliki pencatatan dan rekonsiliasi terpisah; sebagian tagihan masih diajukan melalui memo.

Perbedaan aturan AKP, GAM, dan HO harus dipertahankan secara eksplisit. Operating unit/site tidak otomatis dianggap sebagai legal company yang berbeda; pemetaan struktur organisasi perlu diputuskan terlebih dahulu.

## Hasil bisnis yang diharapkan

- Data karyawan dan transaksi dapat ditelusuri dari pengajuan, verifikasi, approval, hingga pencatatan akhir.
- Perhitungan payroll dapat direkonsiliasi terhadap attendance, kontrak, insentif, serta potongan yang disetujui.
- Hak akses membatasi data sensitif sesuai site, perusahaan, dan peran pengguna.
- Biaya payroll dan GA dapat dianalisis menggunakan dimensi organisasi yang disepakati.
- Kebutuhan data, keputusan tertunda, dan skenario uji memiliki referensi yang konsisten.

## Cakupan yang dibahas

People dan employee master; recruitment/PTK/MPP; attendance/roster/SPL; payroll; cuti; mutasi/promosi/appraisal; SP dan offboarding; dokumen karyawan; travel, mess, laundry, meals dan survey GA; custody/APD/exit clearance; pengadaan terkait GA; employee loan, cash advance, vendor bill, accrued, dan reporting terkait.

## Batas yang belum dikomitmenkan

- Integrasi langsung mesin fingerprint, API job portal, WhatsApp otomatis, bank transfer otomatis, serta pengadaan perangkat tidak dianggap sudah termasuk scope.
- Migrasi seluruh histori, jumlah tahun data, volume pengguna, SLA, hosting, versi/edisi Odoo, lisensi, dan timeline belum ditetapkan.
- SPL HO disebut sebagai kebutuhan lanjutan pada MOM. Fase implementasinya perlu disetujui; tidak otomatis masuk fase awal.
- Pengadaan dan accounting dibatasi pada titik integrasi yang terkait HR/GA dalam dokumen ini, bukan penggantian seluruh proses ERP.
- Rumus PPh 21, BPJS, PKWT/PKWTT, pesangon, pensiun, dan hak akhir karyawan belum divalidasi terhadap regulasi. HR/Finance/Legal GPE harus menyetujui aturan beserta tanggal efektif sebelum konfigurasi.

## Alur lintas fungsi utama

Payroll: sumber attendance/roster/SPL/insentif → verifikasi site/HO → perhitungan dan slip bayangan → koreksi pada tahap yang diizinkan → approval final dan lock → output Finance, jurnal, dan distribusi slip.

Employee lifecycle: MPP/PTK → recruitment → onboarding/employee master → attendance, cuti, payroll dan layanan GA → perubahan jabatan/site → offboarding dan exit clearance.

GA: permintaan layanan/barang → pencatatan pemakaian → rekonsiliasi → approval sesuai matriks → vendor bill/accrued → monitoring biaya. Mekanisme travel masih menunggu keputusan D03.

---

# Peran, akses, dan approval

## Peran yang terlibat

Matriks berikut adalah rancangan untuk validasi. Pembatasan payroll per site dan akses seluruh site oleh HR HO tercatat di MOM; rincian hak create/read/write/approve/export lainnya masih perlu disepakati pada D01 dan D14.

| Peran | Tanggung jawab proses | Batas akses yang perlu diterapkan |
| --- | --- | --- |
| HR Site | Verifikasi data site, roster, administrasi karyawan | Payroll hanya site yang diizinkan |
| HR HO | Konsolidasi dan pengelolaan HR/payroll lintas site | Seluruh site sesuai mandat perusahaan |
| Admin departemen / pengawas | Input form, SPL, cuti dan data pendukung | Departemen/site terkait; tanpa akses payroll penuh secara default |
| GA | Travel, mess, meals, laundry, custody dan survey | Data operasional yang diperlukan; bukan seluruh data gaji |
| Finance / Accounting | Pajak, loan, CA, tagihan, jurnal dan pembayaran | Data keuangan sesuai perusahaan dan kewenangan |
| Management / approver | Persetujuan transaksi sesuai hierarki | Hanya pengajuan dalam jalur approval yang ditetapkan |
| MCC / Engineering site | Sumber HM dan productivity | Data operasional yang relevan |
| Employee / kandidat | Pengajuan atau akses portal sesuai proses | Data sendiri; tidak mengakses data karyawan lain |
| IT / HSE / departemen pemilik barang | Clearance dan pengelolaan barang terkait | Barang dan kewajiban dalam tanggung jawab departemen |

## Requirement akses dan approval

### SEC-01 | Pembatasan payroll per site

Status: Tercatat | Sumber: S1 / Payroll Roster | Pemilik proses: HR HO dan HR Site.

Sistem harus membatasi HR Site agar tidak dapat melihat payroll site lain. HR HO dapat melihat payroll lintas site sesuai kewenangannya. Pemetaan legal company, operating unit, site, dan peran mengikuti D01.

Kriteria penerimaan: akun HR AKP tidak dapat membuka payroll GAM melalui daftar, pencarian, tautan langsung, maupun ekspor; akun HR HO yang ditunjuk dapat membuka kedua site. Pengujian lintas company dilakukan bila struktur tersebut digunakan.

### SEC-02 | Approval, alasan penolakan, dan jejak keputusan

Status: Terbuka - D02, D10, D14 | Sumber: S1-S3 / Payroll Roster, PTK, MPP.

Sistem harus mendukung approval per jenis transaksi. Alasan reject wajib untuk PTK dan loan. Payroll mengikuti aturan revisi/lock pada PAY-04. Jalur loan, PTK, MPP, kontrak, evaluasi, dan pengeluaran barang harus dipetakan sebelum konfigurasi.

Kriteria penerimaan: pengguna di luar approver aktif tidak dapat menyetujui; reject PTK/loan tanpa alasan ditolak; identitas, waktu, dan hasil keputusan dapat ditelusuri. PTK yang ditolak tidak langsung diteruskan sebagai pengajuan yang sama.

---

# Requirement fungsional - People dan recruitment

## Employee master dan manpower

### EMP-01 | Identitas dan histori karyawan

Status: Terbuka - D01, D11 | Sumber: S2-S3 / Recruitment, Mutasi.

Sistem harus membedakan NIK KTP dari nomor/NIK employee, menyimpan status tetap/kontrak, jabatan, departemen, site, serta lokal/nonlokal. Histori perpindahan site dan jabatan harus tersimpan. Mutasi AKP-GAM tidak mengubah NIK employee.

Kriteria penerimaan: mutasi mempertahankan identitas employee dan menampilkan posisi/site sebelum-sesudah beserta tanggal efektif. Pembuatan nomor employee mengikuti tahap dan pola yang disetujui pada D11.

### REC-01 | Manpower planning

Status: Tercatat | Sumber: S2 / MPP.

Sistem harus mencatat MPP per operating unit, departemen, posisi, forecast, dan periode. Pengajuan dilakukan departemen terkait dengan pengecekan budget per departemen/jabatan serta approval yang disetujui.

Kriteria penerimaan: kebutuhan dan budget dapat dibandingkan per posisi/periode; status verifikasi dan approval terlihat. Aksi ketika budget terlampaui, termasuk warning atau blokir, mengikuti D14.

### REC-02 | Permintaan tenaga kerja

Status: Terbuka - D14 | Sumber: S2 / PTK.

Sistem harus menyediakan PTK, verifikasi, approval bertingkat, serta penandaan pemenuhan internal/eksternal. PTK yang ditolak wajib memiliki alasan; pemohon membuat PTK baru. Kebutuhan portal dan hierarki final ditetapkan pada D12/D14.

Kriteria penerimaan: PTK hanya maju setelah persetujuan tahap yang diwajibkan; penolakan tersimpan dengan alasan; pengajuan pengganti memiliki nomor berbeda dan dapat ditelusuri ke permintaan sebelumnya sebagai usulan kontrol.

### REC-03 | Pipeline recruitment dan dokumen kandidat

Status: Tercatat | Sumber: S2 / Recruitment.

Sistem harus melacak verifikasi CV, tes tertulis, interview, offering letter, MCU/follow-up, verifikasi MCU site, pengiriman ke site, tes praktik, induksi, kontrak, orientasi, dan penyerahan ke departemen. Kandidat belum menjadi employee tetap dapat dicatat menggunakan nama dan NIK KTP.

Kriteria penerimaan: satu kandidat dapat ditelusuri antar-tahap, termasuk hasil evaluasi dan dokumen pendukung. Bukti surat izin masuk, resume dan verifikasi MCU tersedia sebelum tes praktik sesuai checklist yang disetujui.

### REC-04 | Onboarding, kontrak, dan notifikasi

Status: Terbuka - D11, D12, D14 | Sumber: S2 / Recruitment, HR GA New Hire.

Sistem harus mendukung approval kontrak, transisi kandidat menjadi employee, dan penyampaian status proses. Template notifikasi disediakan GPE. Pengiriman WhatsApp masih manual sesuai pembahasan; otomasi tidak diasumsikan tersedia.

Kriteria penerimaan: kandidat yang memenuhi tahap konversi menghasilkan employee tanpa kehilangan referensi recruitment; kontrak dan approval dapat ditelusuri; notifikasi memakai template dan kanal yang disetujui tanpa menjanjikan API yang belum ditetapkan.

---

# Requirement fungsional - Attendance, roster, dan cuti

### ATT-01 | Penerimaan dan verifikasi attendance

Status: Tercatat | Sumber: S1 / Flow existing, Code Absensi.

Sistem harus menerima data attendance yang bersumber dari fingerprint export/form dan menghubungkannya ke employee, tanggal, site, serta kode absensi. Format impor dan cara menangani scan hilang/duplikat ditetapkan pada D07/D12.

Kriteria penerimaan: batch contoh dapat direkonsiliasi ke sumber; data tidak dikenal atau tidak lengkap dilaporkan. Impor ulang file yang sama tidak menggandakan hasil payroll, sebagai usulan kontrol integritas.

### ATT-02 | Roster, shift, dan kalender hari libur

Status: Terbuka - D07 | Sumber: S1 / Payroll Roster, Shift.

Sistem harus mendukung roster 13:1 dan 6:1, shift sesuai kebutuhan site, serta kalender libur nasional tanpa otomatis menyamakan cuti bersama. Jadwal HO dan aturan shift final disediakan GPE.

Kriteria penerimaan: roster menghasilkan jadwal dan hari istirahat sesuai pola yang disetujui; perubahan shift/hari libur menghasilkan klasifikasi attendance yang benar untuk periode uji tanpa mengubah histori yang telah dikunci.

### ATT-03 | SPL dan kondisi kerja khusus

Status: Terbuka - D07 | Sumber: S1 / Payroll, Shift.

Sistem harus mencatat SPL yang dibuat pengawas dan diinput HR, jam kerja/OT, serta kondisi dipulangkan, kembali bekerja, atau alat rusak. Kasus D6, D7 dan hari libur harus dapat dibedakan. SPL HO merupakan kebutuhan lanjutan yang fasenya belum ditetapkan.

Kriteria penerimaan: jam/rate hasil uji untuk hari reguler, D6, D7, libur, dan alat rusak sesuai matriks GPE; jejak alasan serta check-in/out tersedia. Sistem tidak menerapkan satu formula OT untuk semua site/employee.

### LEV-01 | Annual leave dan saldo

Status: Terbuka - D08 | Sumber: S3 / Annual Leave.

Sistem harus mendukung hak cuti 12 hari setelah satu tahun bergabung, carryover dengan batas enam bulan, dan saldo kedaluwarsa. Cuti bersama HO diperhitungkan sesuai kebijakan. Perlakuan saldo saat resign/PHK/pensiun memerlukan persetujuan aturan final.

Kriteria penerimaan: uji sebelum dan setelah ulang tahun kerja, penggunaan saldo, carryover, dan kedaluwarsa menunjukkan saldo yang sesuai kebijakan bertanggal efektif. Tidak ada penggantian uang atas cuti hangus tanpa aturan yang disetujui.

### LEV-02 | Pengajuan dan bukti cuti

Status: Terbuka - D08, D12 | Sumber: S3 / Annual Leave.

Sistem harus mendukung pencatatan cuti dengan lampiran hardcopy yang telah disetujui dan input oleh admin departemen. Rencana portal harus dijelaskan posisinya terhadap proses manual agar tidak timbul dua pengajuan untuk satu cuti.

Kriteria penerimaan: pencatatan cuti menyimpan employee, jenis, tanggal, durasi, bukti persetujuan, dan penginput; pengajuan portal/manual untuk kejadian yang sama tidak menduplikasi pengurangan saldo.

### LEV-03 | Perubahan cuti roster

Status: Terbuka - D08 | Sumber: S3 / Site Leave.

Sistem harus menyediakan form perubahan roster/cuti, alasan, berita acara, tanggal sebelumnya dan usulan tanggal baru. Approval dilakukan HR Site. Eligibility jabatan mengikuti daftar GPE, termasuk ketentuan foreman ke bawah yang tercatat.

Kriteria penerimaan: perubahan belum memengaruhi roster aktif sebelum approved; setelah approved, plan baru dan histori plan sebelumnya dapat ditelusuri serta diteruskan ke proses terkait.

---

# Requirement fungsional - Payroll dan employee loan

### PAY-01 | Struktur gaji per site dan employee

Status: Terbuka - D05, D06, D07 | Sumber: S1 / Payroll.

Sistem harus mendukung all-in/OT dan struktur gaji yang berbeda per site, kontrak, dan employee. Komponen meliputi gaji pokok, tunjangan, OT, HM, productivity, kompensasi hari libur, safety captain, BPJS, loan, dan potongan lain yang disetujui.

Kriteria penerimaan: dua employee pada jabatan sama dapat memiliki komponen/nominal berbeda; perhitungan memakai kontrak dan tanggal efektif yang benar. Formula dan pembulatan diuji menggunakan daftar komponen final GPE.

### PAY-02 | Input insentif dan komponen variabel

Status: Terbuka - D04, D06 | Sumber: S1 / Payroll Roster.

Sistem harus menerima HM dari MCC, productivity dari Engineering, safety captain yang terkait attendance, serta tunjangan lain-lain manual. Rate HM dapat terkait unit/tipe unit; dampak perubahan fungsi unit perlu dikonfirmasi. Uang makan diproses sebagai payslip dengan pembayaran terpisah.

Kriteria penerimaan: nilai variabel dapat ditelusuri ke sumber/form dan periode; rate HM sesuai konfigurasi yang disetujui; komponen uang makan tidak dibayarkan kembali dalam pembayaran gaji reguler.

### PAY-03 | Prorata dan penyesuaian payroll

Status: Terbuka - D05, D07, D09 | Sumber: S1, S3 / Payroll Roster, Mutasi, Promosi.

Sistem harus mendukung prorata gaji/tunjangan saat promosi di tengah periode, pemotongan kehadiran sesuai site, dan perubahan payroll saat mutasi. Pembagi, cut-off, pembulatan, acting allowance, serta dampak pajak lintas site harus disetujui GPE.

Kriteria penerimaan: contoh promosi tengah bulan dan mutasi AKP-GAM sesuai hitungan pembanding yang disetujui; hasil menampilkan komponen sebelum/sesudah dan tidak mengganti histori payslip final.

### PAY-04 | Slip bayangan, koreksi, approval, dan lock

Status: Terbuka - D07, D14 | Sumber: S1 / Flow existing, Payroll Roster.

Sistem harus mendukung kalkulasi awal, slip bayangan, pencatatan koreksi sebelum tenggat, rekap payroll, approval, dan finalisasi. Stage 1 untuk validasi; revisi pada stage 2-3. Setelah approval Direktur Operational dan lock, revisi biasa dilarang.

Kriteria penerimaan: koreksi pada tahap yang diizinkan tercatat dan menghitung ulang hasil; koreksi setelah lock ditolak. Perubahan nilai membatalkan persetujuan terkait sebagai usulan kontrol yang perlu disetujui; mekanisme koreksi pasca-lock ditentukan pada D07.

### PAY-05 | Payslip final dan output Finance

Status: Terbuka - D05, D06 | Sumber: S1, S6 / Payroll, Payroll Roster.

Sistem harus menghasilkan rekap payroll dan payslip final untuk distribusi sesuai kewenangan. Tampilan HL, komponen pajak/tunjangan pajak, periode, serta rincian penghasilan/potongan mengikuti template GPE. Output untuk Finance harus dibedakan dari status pembayaran aktual.

Kriteria penerimaan: total per employee pada slip sama dengan rekap; total rekap dapat direkonsiliasi ke output Finance; employee hanya menerima slip miliknya. Uang makan dan pembayaran terpisah dikenali dengan jelas.

### LON-01 | Pengajuan dan approval employee loan

Status: Terbuka - D02 | Sumber: S1, S6 / Payroll Roster.

Sistem harus mencatat pengajuan loan, sisa pinjaman, verifikasi Finance/management, approval bertingkat, dan alasan reject wajib. Input loan site dilakukan HR HO dari form manual; loan HO Jakarta/Samarinda diinput Finance sesuai MOM.

Kriteria penerimaan: saldo outstanding terlihat saat pengajuan; loan tidak berstatus approved sebelum seluruh tahap selesai; reject tanpa alasan ditolak. Jumlah tahap dan urutan approver mengikuti keputusan D02.

### LON-02 | Cicilan dan rekonsiliasi loan

Status: Terbuka - D02 | Sumber: S1, S6 / Payroll, Payroll Roster.

Sistem harus menghubungkan jadwal cicilan yang disetujui ke potongan payroll bulanan dan saldo outstanding. Perlakuan pembatalan payroll, pelunasan dipercepat, gaji tidak mencukupi, serta saldo saat exit clearance perlu ditetapkan.

Kriteria penerimaan: cicilan final mengurangi outstanding tepat satu kali; payroll draft tidak dianggap pelunasan; pembatalan/koreksi resmi tidak menyebabkan saldo negatif atau potongan ganda.

---

# Requirement fungsional - Karier, kepatuhan internal, dan offboarding

### CAR-01 | Mutasi, rotasi, dan demosi

Status: Terbuka - D09, D14 | Sumber: S3 / Mutasi.

Sistem harus mencatat evaluasi, pengajuan, approval, tanggal efektif dan histori perubahan organisasi/jabatan. Perpindahan AKP-GAM mempertahankan NIK employee serta meneruskan perubahan yang relevan ke payroll dan hak akses.

Kriteria penerimaan: perubahan belum berlaku sebelum persetujuan dan tanggal efektif; histori asal-tujuan tersedia; hasil payroll dan akses site setelah mutasi mengikuti matriks yang disetujui.

### CAR-02 | Acting period, appraisal, dan promosi

Status: Terbuka - D09, D14 | Sumber: S3 / Promosi.

Sistem harus mendukung pengajuan acting period, salary acting manual, hasil evaluasi, keputusan lulus/tidak lulus, dan SK pengangkatan. Parameter appraisal mencakup attendance, kinerja, riwayat SP, dan pelanggaran HSE.

Kriteria penerimaan: evaluasi terhubung ke employee dan periode; keputusan gagal mempertahankan fungsi lama; keputusan lulus yang disetujui menghasilkan perubahan jabatan/payroll pada tanggal efektif tanpa menimpa riwayat.

### DIS-01 | Coaching dan surat peringatan

Status: Terbuka - D09 | Sumber: S3 / SP.

Sistem harus mencatat coaching, pelanggaran, tingkat SP, masa berlaku, dan dokumen. MOM mencatat SP1 tiga bulan dan SP2 enam bulan. Dampak dirumahkan atau tetap bekerja terhadap gaji harus ditetapkan melalui aturan payroll yang disetujui.

Kriteria penerimaan: masa berlaku dan histori SP terlihat serta dapat digunakan pada appraisal; perubahan kondisi kerja tidak otomatis memotong payroll tanpa klasifikasi dan otorisasi yang ditetapkan.

### DOC-01 | Dokumen karyawan dan reminder

Status: Terbuka - D09, D13 | Sumber: S3 / Dokumen karyawan digital.

Sistem harus mencatat masa berlaku SIMPER, K3, POP, mine permit, MCU, SIM, dan kontrak. Reminder dokumen dimulai satu bulan sebelum habis dengan pengulangan mingguan; kontrak PKWT memiliki jadwal bertahap sesuai MOM, yang perlu diterjemahkan menjadi jumlah hari pasti.

Kriteria penerimaan: data uji sebelum, pada, dan setelah ambang reminder menghasilkan pemberitahuan ke penerima yang benar; dokumen kedaluwarsa tetap terlihat. Rumus expired SIMPER dan daftar penerima mengikuti D13.

### OFF-01 | Resign, PHK, pensiun, dan eligibility rehire

Status: Terbuka - D09 | Sumber: S3 / Resign.

Sistem harus mencatat jenis/sebab keluar, tanggal efektif, dokumen, status ikatan dinas, serta flag blacklist/banned berdasarkan NIK KTP. Durasi dan pemicu mengikuti kebijakan yang disetujui; blacklist permanen dibedakan dari banned sementara.

Kriteria penerimaan: lamaran dengan NIK KTP yang sama menampilkan pembatasan yang masih aktif kepada petugas berwenang; kasus banned kedaluwarsa dan blacklist permanen dibedakan. Data sensitif tidak ditampilkan pada pengguna umum.

### OFF-02 | Exit clearance dan final settlement

Status: Terbuka - D05, D09, D10 | Sumber: S3, S5-S6 / Exit Clearance, Resign, Payroll Roster.

Sistem harus mengonsolidasikan status pengembalian barang per departemen, loan/CA yang relevan, kewajiban ikatan dinas, serta hak/potongan akhir yang disetujui. APD menggunakan konsep form mirroring scrap sesuai MOM, bukan otomatis equipment handover standar.

Kriteria penerimaan: checklist menunjukkan clearance dan kewajiban per departemen; perhitungan akhir menampilkan dasar serta otorisasi setiap komponen. Penyelesaian barang tidak boleh menggandakan potongan atau pengakuan biaya.

---

# Requirement fungsional - Layanan GA

### GA-01 | Permintaan dan pelaksanaan travel

Status: Terbuka - D03, D12 | Sumber: S4 / Travel, HR GA New Hire.

Sistem harus mencatat perjalanan new hire, cuti/kembali cuti, dinas dan MCU, penumpang, asal-tujuan, tanggal, vendor, biaya, dan analytic distribution. Employee terdaftar menggunakan referensi employee; new hire menggunakan nama/NIK KTP tanpa wajib memiliki employee master.

Kriteria penerimaan: permintaan dapat dibuat untuk kandidat dan employee; perjalanan berangkat/pulang dapat menggunakan vendor berbeda; relasi cuti tersedia bila relevan tanpa mewajibkan form cuti bagi new hire.

### GA-02 | Tagihan travel dan reimbursement

Status: Terbuka - D03 | Sumber: S4 / Travel.

Sistem harus mendukung pencatatan invoice travel bulk, rincian biaya/tol, dan alokasi biaya. Reimbursement perjalanan GAM dan lumpsum AKP mengikuti eligibility. Alur direct invoice versus PR-PO belum diputuskan dan tidak boleh keduanya diposting untuk tagihan yang sama.

Kriteria penerimaan: satu invoice dapat mencakup beberapa penumpang; total rincian sesuai invoice; transaksi tidak eligible ditolak/ditandai sesuai kebijakan; satu layanan tidak menciptakan dua kewajiban vendor.

### GA-03 | Pengelolaan mess

Status: Tercatat | Sumber: S4 / Mess Management.

Sistem harus mencatat mess, kapasitas, penghuni, tamu, status RFU/NA, dan status onsite/cuti/kosong. Penghuni tamu perlu dibedakan agar rekap occupancy dan dasar perencanaan meals dapat dijelaskan.

Kriteria penerimaan: daftar penghuni per tanggal dapat ditelusuri; kapasitas dan ketersediaan terlihat; total onsite, cuti, tamu dan tempat kosong dapat direkonsiliasi tanpa menghitung orang yang sama dua kali.

### GA-04 | Pencatatan dan rekonsiliasi laundry

Status: Terbuka - D04 | Sumber: S4 / Laundry Management.

Sistem harus mendukung pendaftaran pengguna, pencatatan laundry employee/mess, kuantitas sesuai satuan yang disetujui, dan monitoring untuk pembandingan tagihan vendor. MOM mencatat batas tagihan tanggal 5 tiap bulan; metode alokasi biaya penghuni masih perlu dibahas.

Kriteria penerimaan: volume dan nilai invoice dapat dibandingkan dengan rekap periode/mess; selisih terlihat; alokasi biaya hanya mengikuti metode D04, bukan dibagi rata tanpa persetujuan.

### GA-05 | Plan, actual, dan rekonsiliasi meals

Status: Terbuka - D04 | Sumber: S4 / Meals Management.

Sistem harus mencatat plan order dan actual meals per kategori, penghuni/POB serta cuti, voucher tamu, dan deviasi. Attendance kantin harus terpisah dari attendance payroll. Rekap dilakukan GA dan direkonsiliasi site sebelum invoice dikirim HO.

Kriteria penerimaan: plan melampaui batas manpower/kapasitas ditangani sesuai kontrol yang disetujui; deviasi sama dengan plan dikurangi actual; data makan tidak menambah jam kerja payroll; eligibility meals dan uang makan tidak bertentangan.

### GA-06 | Survey dan tindak lanjut temuan

Status: Terbuka - D12 | Sumber: S4 / GA Survey.

Sistem harus mendukung survey berbasis web, keterkaitan employee/mess, rekap hasil, penugasan PIC temuan, dan status tindak lanjut. Temuan yang membutuhkan vendor diteruskan ke proses pengadaan jasa.

Kriteria penerimaan: satu hasil survey dapat ditelusuri sampai penanganan internal atau pengadaan jasa; data responden ditampilkan sesuai hak akses; kebutuhan API/portal mengikuti keputusan integrasi.

---

# Requirement fungsional - Asset, pengadaan, dan biaya GA

### AST-01 | Custody dan serah terima barang

Status: Terbuka - D10 | Sumber: S5 / Custody.

Sistem harus mencatat permintaan barang, departemen pemilik, employee penerima, lokasi, serial number untuk barang relevan, serta berita acara serah terima. Bila stok tidak tersedia, proses SPB mengikuti kewenangan departemen dan GA.

Kriteria penerimaan: barang berserial dapat ditelusuri ke penerima/lokasi; permintaan saat stok kosong tidak menghasilkan serah terima fiktif; pengembalian memperbarui custody tanpa menghapus histori.

### AST-02 | APD, penggantian, dan kehilangan

Status: Terbuka - D10 | Sumber: S5 / Exit Clearance.

Sistem harus mencatat masa pakai APD sesuai departemen/jenis, penggantian, kerusakan/kehilangan, berita acara, dan keputusan ganti rugi HO. Konsumsi inventory, write-off dan potongan employee merupakan transaksi berbeda yang harus direkonsiliasi.

Kriteria penerimaan: satu kejadian kehilangan memiliki referensi keputusan dan nilai yang disetujui; treatment probation/non-probation sesuai matriks final; biaya/potongan tidak diposting dua kali oleh form clearance dan inventory.

### PRO-01 | SPB, MOL, penerimaan, dan pengeluaran

Status: Terbuka - D10, D14 | Sumber: S5 / Custody, GA Survey.

Sistem harus mendukung SPB dan MOL sesuai fungsi, penomoran per departemen/site yang reset tahunan, serta pembeda GA-Logistik. Goods receipt mengikuti gudang tujuan dan approver; goods issue memiliki nomor departemen.

Kriteria penerimaan: nomor unik pada tahun yang sama dan reset sesuai aturan; penerimaan ditangani peran yang sesuai gudang; barang keluar/masuk dapat ditelusuri ke permintaan dan persetujuan yang diwajibkan.

### PRO-02 | Minimum stock consumable

Status: Terbuka - D10 | Sumber: S5 / Pengadaan Barang Consumable HO.

Sistem harus menyimpan daftar consumable dan minimum stock, lalu memberi notifikasi kepada departemen terkait jika stok di bawah ambang. Otomatisasi pembelian tidak diasumsikan termasuk tanpa persetujuan terpisah.

Kriteria penerimaan: item di atas dan di bawah minimum menghasilkan status yang berbeda; notifikasi menampilkan item, lokasi dan kekurangan; penerima mengikuti daftar GPE.

### GA-07 | Pengadaan jasa dan reminder kewajiban

Status: Terbuka - D10, D13 | Sumber: S5 / Pengadaan Jasa.

Sistem harus mendukung referensi memo/SPB, uang muka jasa bila relevan, dan reminder tagihan/perizinan. Jadwal yang tercatat mencakup internet/Starlink satu minggu, STNK satu bulan, serta KIR satu minggu sebelum jatuh tempo; applicability per kendaraan harus dipastikan.

Kriteria penerimaan: reminder muncul pada ambang yang disetujui dan hanya untuk objek yang relevan; permintaan dapat ditelusuri ke vendor bill/pembayaran tanpa dianggap otomatis lunas setelah diajukan.

### GA-08 | Monitoring real cost, kendaraan, dan fuel

Status: Tercatat | Sumber: S5 / Pengadaan Jasa, Report Monitoring.

Sistem harus mendukung monitoring biaya meals, laundry, travel, ticket, hotel, air minum, listrik, serta bus/LV. Kendaraan dicatat berdasarkan nomor lambung/vendor dan data operasional terkait. Fuel menghubungkan pembacaan KM pada pengisian sebelumnya dan berikutnya.

Kriteria penerimaan: biaya bulanan dapat ditelusuri ke sumber transaksi; selisih KM terhitung dari dua pembacaan berurutan; pembacaan turun/kosong ditandai, bukan menghasilkan konsumsi valid tanpa pemeriksaan.

---

# Requirement fungsional - Accounting dan cash advance

### FIN-01 | Payroll accrued dan realisasi

Status: Terbuka - D15 | Sumber: S6 / Accounting.

Sistem harus mendukung pengakuan biaya/potongan pada akhir bulan, pencatatan accrued maksimal tanggal 3, reversal tanggal 1 periode berikutnya, dan jurnal realisasi yang menurut MOM terkait tanggal 10/aktual pembayaran. Urutan tanggal dokumen, posting, dan pembayaran harus dikonfirmasi.

Kriteria penerimaan: satu periode uji menghasilkan jurnal balanced, reversal yang mereferensikan accrued, dan realisasi tanpa biaya ganda; jurnal sesuai company, periode dan kebijakan lock-date yang disetujui Finance.

### FIN-02 | Mapping komponen dan analytic distribution

Status: Terbuka - D01, D15 | Sumber: S6 / Payroll Roster.

Sistem harus memisahkan biaya payroll per komponen dan mendukung dimensi operating unit, lokasi/pit, departemen, serta unit opsional. Mapping akun, kewajiban analytic, dan alokasi lintas lokasi/site harus disetujui sebelum posting.

Kriteria penerimaan: total jurnal sama dengan rekap yang menjadi sumber; setiap komponen masuk akun yang ditentukan; persentase distribusi lengkap dan tidak mengalihkan transaksi ke company yang salah.

### FIN-03 | Vendor bill dan accrued GA

Status: Terbuka - D03, D04, D15 | Sumber: S4-S6 / Meals, Laundry, Travel, Pengadaan Jasa.

Sistem harus menghubungkan pemakaian/rekonsiliasi layanan GA ke tagihan dan accrued sesuai proses final. Penghilangan memo pada meals/laundry harus ditetapkan bersama jalur approval dan bukti pendukung yang menggantikannya.

Kriteria penerimaan: total bill/accrued sesuai layanan yang diverifikasi dan alokasi biayanya; satu invoice vendor tidak dicatat berulang; selisih aktual terhadap accrued dapat dijelaskan pada laporan.

### FIN-04 | Pengajuan dan pencairan cash advance

Status: Terbuka - D15 | Sumber: S6 / Cash Advance.

Sistem harus mendukung CA untuk employee maupun DP vendor, pencairan petty cash/bank, approval, dan tautan PO bila relevan. Pengakuan advance mengikuti uang yang benar-benar dikeluarkan. CA bukan potongan payroll reguler kecuali penyelesaian exit clearance yang disetujui.

Kriteria penerimaan: pengajuan belum cair tidak dicatat sebagai pengeluaran aktual; pencairan terhubung ke penerima dan referensi pembayaran; CA tidak otomatis masuk potongan gaji bulanan.

### FIN-05 | Pertanggungjawaban dan outstanding CA

Status: Usulan - D15 | Dasar: kelengkapan kontrol untuk FIN-04.

Sistem perlu menyimpan pertanggungjawaban, pengembalian sisa, dan outstanding CA secara terpisah dari employee loan. Detail bukti, selisih lebih/kurang, serta approval penyelesaian memerlukan keputusan Finance.

Kriteria penerimaan: nilai cair dikurangi pertanggungjawaban/pengembalian menghasilkan outstanding yang dapat direkonsiliasi; status selesai tidak dapat diberikan jika selisih belum ditangani sesuai kebijakan.

---

# Integrasi dan kebutuhan data

## Titik integrasi

Mekanisme berikut merupakan batas kebutuhan, bukan konfirmasi ketersediaan API atau penetapan solusi teknis. Versi Odoo, format, owner interface dan frekuensi final mengikuti D12/D16.

| ID | Pertukaran data | Batas dan kontrol |
| --- | --- | --- |
| INT-01 | Fingerprint/form → attendance → payroll | Awal berbasis export/impor; identitas employee, periode, error dan duplikasi divalidasi |
| INT-02 | MCC/Engineering → komponen payroll | HM, unit, productivity dan periode; sumber serta persetujuan dapat ditelusuri |
| INT-03 | Job portal ↔ recruitment | Excel/posting dan histori sesuai MOM; API real-time belum disepakati |
| INT-04 | Employee/cuti ↔ GA | Identitas, travel, occupancy, eligibility; akses data dibatasi |
| INT-05 | Payroll/GA → Accounting | Rekap, komponen, akun, analytic, accrued/reversal; tidak posting ganda |
| INT-06 | Custody/exit ↔ Inventory/Payroll/Finance | Referensi barang dan kewajiban; pemilik pencatatan biaya/potongan ditentukan |
| INT-07 | Status/reminder → email/portal/WA | Template dan penerima disetujui; WA manual sampai ada scope otomasi |

Kriteria penerimaan bersama (usulan): jumlah record dan total nilai sebelum-sesudah pertukaran sama; record gagal ditampilkan beserta sebabnya; percobaan ulang tidak menggandakan transaksi; pengguna hanya mengakses data yang diizinkan. Pengujian kegagalan dan retry harus masuk spesifikasi interface.

## Master data minimum

- Organisasi: company/legal entity bila digunakan, operating unit, site, lokasi/pit, departemen, jabatan, dan unit.
- Employee: NIK employee, NIK KTP, status kontrak, tanggal masuk, penempatan, lokal/nonlokal, serta data payroll yang disetujui.
- Waktu kerja: kode absensi, shift, roster, kalender hari libur, cut-off dan jenis cuti.
- Payroll: struktur komponen, formula/rate, eligibility, pembulatan, tanggal efektif, dan mapping akun/analytic.
- GA: mess/kapasitas, vendor/layanan, kategori meals, barang/APD, serial, gudang, kendaraan, minimum stock, dan satuan.
- Kontrol: pengguna/peran/site yang diizinkan, approver per proses, template, dan daftar penerima reminder.

## Data awal dan migrasi

Usulan: cakupan awal meliputi employee aktif, kontrak, saldo cuti, outstanding loan/CA, penghuni mess, custody aktif, masa berlaku dokumen, serta nilai pembuka yang disepakati. Histori payroll dan transaksi lama hanya dimigrasikan setelah volume, periode, dan kebutuhan audit disetujui.

Kriteria penerimaan usulan: sumber asli tidak diubah; data dimuat di lingkungan uji dahulu; jumlah employee, saldo cuti/loan/CA, dan nilai pembuka direkonsiliasi; data reject dicatat; pemilik data menyetujui hasil sebelum produksi. Backup database dan filestore diperlukan sebelum migrasi yang berisiko mengubah data existing.

---

# Reporting dan non-functional requirement

## Keluaran laporan

Filter site/company hanya tersedia sesuai akses. Format akhir serta granularitas report menunggu contoh GPE pada D13. Daftar berikut adalah katalog kebutuhan; bukan janji seluruhnya berupa dashboard terpisah.

| ID | Keluaran | Rujukan requirement |
| --- | --- | --- |
| RPT-01 | Slip bayangan/final, rekap komponen dan potongan | PAY-01 sampai PAY-05 |
| RPT-02 | Rekap attendance, roster, SPL dan exception | ATT-01 sampai ATT-03 |
| RPT-03 | Status MPP/PTK, kandidat dan recruitment | REC-01 sampai REC-04 |
| RPT-04 | Saldo cuti, histori jabatan/site, SP dan expiry | EMP-01, LEV-01, CAR-01, DIS-01, DOC-01 |
| RPT-05 | Travel, occupancy, laundry, meals dan deviasi | GA-01 sampai GA-05 |
| RPT-06 | Custody/APD, exit clearance dan minimum stock | AST-01, AST-02, OFF-02, PRO-02 |
| RPT-07 | Loan, CA, accrued/realisasi dan real cost GA | LON-02, FIN-01 sampai FIN-05, GA-08 |
| RPT-08 | Biaya per dimensi organisasi dan unit | FIN-02 |

Kriteria penerimaan usulan: setiap total dapat ditelusuri ke transaksi asal; filter periode/site memberikan hasil konsisten; ekspor tidak melewati hak akses; format slip sensitif hanya tersedia untuk pengguna berwenang.

## Kontrol non-fungsional yang diusulkan

### NFR-01 | Privasi dan least privilege

Status: Usulan | Terkait: SEC-01, EMP-01, REC-03, DOC-01.

Payroll, NIK KTP, data MCU dan dokumen pribadi harus dibatasi berdasarkan kebutuhan kerja. Portal, attachment, pencarian dan ekspor harus mengikuti pembatasan yang sama dengan layar utama. Retensi data dan penerima data ditentukan pada D16.

Kriteria penerimaan: negative test untuk pengguna site lain, kandidat dan employee lain menolak akses record/lampiran sensitif; tidak ada pembocoran melalui report atau tautan langsung.

### NFR-02 | Audit trail dan histori efektif

Status: Usulan | Terkait: SEC-02, PAY-01 sampai PAY-04, CAR-01, FIN-01.

Perubahan data kritis harus merekam aktor, waktu, nilai lama-baru, dan alasan bila diwajibkan. Perubahan kontrak/rate/penempatan memakai tanggal efektif; transaksi final tidak diam-diam berubah ketika master data diperbarui.

Kriteria penerimaan: sampel perubahan dapat direkonstruksi; hitungan ulang periode baru memakai versi tepat; hasil periode final tetap identik kecuali melalui prosedur koreksi resmi.

### NFR-03 | Integritas transaksi dan pemisahan tugas

Status: Usulan | Terkait: payroll, loan, CA, inventory dan accounting.

Sistem perlu mencegah transaksi ganda, approval tidak sah dan nilai total yang tidak konsisten. Posting lintas proses harus selesai konsisten atau meninggalkan error yang dapat dipulihkan; tidak menghasilkan jurnal/potongan sebagian tanpa penanda.

Kriteria penerimaan: submit/retry simultan dan simulasi kegagalan tidak menggandakan payslip, cicilan, atau bill; journal balanced; pemohon dan approver mengikuti matriks pemisahan tugas final.

### NFR-04 | Kinerja, backup, dan operasional

Status: Usulan - D16.

Jumlah employee, concurrent user, volume impor, target durasi payroll/report, jam operasional, backup, RPO/RTO dan retensi perlu ditetapkan sebelum desain teknis. Pengujian dilakukan pada kapasitas yang disepakati, dengan pemisahan local/staging/production.

Kriteria penerimaan: pengujian beban memenuhi angka yang telah disetujui pada D16; restore database dan filestore berhasil diuji; tidak ada data produksi yang dipakai sembarangan pada lingkungan uji.

---

# Rencana validasi dan UAT

## Prasyarat uji

Setiap skenario memiliki data input, hasil yang diharapkan, bukti aktual, status pass/fail, dan reviewer bisnis. Expected result payroll harus disiapkan/ditandatangani HR-Finance GPE; angka yang belum diputuskan tidak dapat dinyatakan lulus. Ambang selisih hanya boleh digunakan jika disetujui tertulis.

## Skenario lintas fungsi minimum - usulan

| ID | Skenario dan hasil yang dibuktikan | Requirement terkait |
| --- | --- | --- |
| UAT-01 | Isolasi payroll AKP/GAM dan akses HR HO; termasuk URL/ekspor/lampiran | SEC-01, NFR-01 |
| UAT-02 | Attendance normal, D6/D7/libur, scan hilang, alat rusak dan impor ulang | ATT-01 sampai ATT-03, PAY-01 |
| UAT-03 | All-in/OT, insentif, promosi tengah bulan, uang makan terpisah dan mutasi | PAY-01 sampai PAY-03, CAR-01 |
| UAT-04 | Slip bayangan dikoreksi, approval, lock, lalu percobaan perubahan ditolak | PAY-04, PAY-05, SEC-02 |
| UAT-05 | Loan diajukan/reject/approved, cicilan, outstanding, dan pembatalan resmi | LON-01, LON-02 |
| UAT-06 | PTK reject dan pengganti; kandidat lolos sampai kontrak/employee | REC-01 sampai REC-04, EMP-01 |
| UAT-07 | Saldo anniversary, carryover/expiry, cuti manual/portal, perubahan roster | LEV-01 sampai LEV-03 |
| UAT-08 | Travel kandidat/employee, vendor berbeda, bill bulk dan eligibility biaya | GA-01, GA-02, FIN-03 |
| UAT-09 | Occupancy/cuti/tamu, laundry dan meals, deviasi serta bill | GA-03 sampai GA-05, FIN-03 |
| UAT-10 | Barang berserial, kehilangan APD, exit clearance dan settlement | AST-01, AST-02, OFF-01, OFF-02 |
| UAT-11 | Accrued akhir bulan, reversal, realisasi dan analytic tanpa biaya ganda | FIN-01 sampai FIN-03 |
| UAT-12 | CA belum cair/cair/settle dan saldo tersisa; tanpa potongan rutin payroll | FIN-04, FIN-05 |
| UAT-13 | Reminder expiry, stok minimum dan kewajiban GA pada ambang waktu | DOC-01, PRO-02, GA-07 |
| UAT-14 | Approval karier/SP, survey temuan, receipt/issue, biaya kendaraan dan report | CAR-02, DIS-01, GA-06, PRO-01, GA-08, RPT-01 sampai RPT-08 |

## Kriteria persetujuan baseline dan kesiapan rilis

Persetujuan requirement dilakukan setelah pemilik proses memvalidasi ruang lingkup dan keputusan yang memengaruhi desain. Requirement terbuka dapat ditunda dengan batas scope yang eksplisit; tidak boleh dianggap otomatis disetujui karena dokumen ditandatangani.

Usulan gate rilis: seluruh skenario kritis payroll, akses, posting dan saldo lulus; tidak ada defect kritis terkait kebocoran data atau salah bayar; data awal direkonsiliasi; matriks approval dan prosedur koreksi final tersedia; backup/restore serta pelatihan PIC selesai. Klasifikasi severity dan otorisasi go-live ditetapkan GPE.

---

# Daftar keputusan terbuka

Semua item berstatus OPEN pada versi 0.1. Owner di bawah adalah fungsi yang disarankan untuk memberi keputusan, bukan penugasan personal yang sudah dikonfirmasi. Target tanggal diisi saat workshop review. Keputusan harus mencatat jawaban, approver, tanggal efektif, bukti, dan requirement terdampak.

### D01 | Struktur organisasi dan akses lintas site

Keputusan: petakan AKP/GAM/HO ke legal company, operating unit, site, lokasi, dan departemen; tentukan batas akses historis setelah mutasi serta kewenangan HR HO.

Owner usulan: HR HO, Finance, IT. Dampak: EMP-01, SEC-01, CAR-01, FIN-02. Gate: sebelum desain akses dan migrasi master.

### D02 | Approval dan penyelesaian employee loan

Keputusan: MOM menulis tiga level tetapi mencantumkan empat pihak untuk site. Konfirmasi urutan, verifikator versus approver, jalur HO, pencairan, cicilan, gaji kurang, pelunasan dan exit.

Owner usulan: HR HO, Finance, Management. Dampak: LON-01, LON-02, SEC-02. Gate: sebelum konfigurasi loan.

### D03 | Travel dan reimbursement

Keputusan: pilih/mapping direct invoice versus PR-PO; definisikan relasi request-penumpang-bill, eligibility GAM/AKP, batas reimbursement/lumpsum, dan perlakuan tol.

Owner usulan: GA, Finance, Procurement. Dampak: GA-01, GA-02, FIN-03. Gate: sebelum desain travel-to-bill.

### D04 | Meals, uang makan, dan laundry

Keputusan: selesaikan ketidakkonsistenan lokal/nonlokal pada MOM; tetapkan eligibility uang makan/fasilitas makan, sumber POB/P5M, pengecualian tamu, satuan laundry, rate serta alokasi biaya per penghuni/mess.

Owner usulan: GA, HR, Finance. Dampak: PAY-02, GA-04, GA-05, FIN-03. Gate: sebelum perhitungan dan rekonsiliasi GA.

### D05 | Aturan pajak, BPJS, dan hak akhir

Keputusan: validasi gross-up dan tampilannya, rate/dasar BPJS, pajak mutasi, hak cuti saat keluar, kompensasi PKWT/PKWTT, pensiun dan pesangon; sepakati sumber legal, tanggal efektif dan pembulatan. Rumus MOM tidak otomatis menjadi aturan produksi.

Owner usulan: HR, Finance/Tax, Legal GPE. Dampak: PAY-01, PAY-03, PAY-05, OFF-02. Gate: sebelum kalkulasi payroll/settlement dinyatakan final.

### D06 | Komponen, insentif, dan template payroll

Keputusan: finalisasi daftar/rate/formula per employee/site, rate HM saat unit berubah fungsi, input productivity, safety captain, tunjangan manual, pembayaran uang makan, dan template slip/rekap.

Owner usulan: HR HO/Site, MCC/Engineering, Finance. Dampak: PAY-01, PAY-02, PAY-05. Gate: sebelum konfigurasi salary rules.

### D07 | Kalender, OT, cut-off, dan payroll lock

Keputusan: finalisasi shift/roster, D6/D7/libur, istirahat, alat rusak/dipulangkan, pembagi potongan, cut-off, batas koreksi slip bayangan, dampak approval ulang, serta prosedur koreksi setelah lock.

Owner usulan: HR HO/Site, Operations, Finance. Dampak: ATT-01 sampai ATT-03, PAY-01, PAY-03, PAY-04. Gate: sebelum UAT payroll.

### D08 | Cuti dan perubahan roster

Keputusan: jenis cuti, perhitungan hak/carryover/expiry, cuti bersama HO, eligibility jabatan, hardcopy versus portal, approval dan relasi travel.

Owner usulan: HR HO/Site, GA. Dampak: LEV-01 sampai LEV-03, GA-01. Gate: sebelum konfigurasi leave/portal.

### D09 | Karier, disiplin, dan offboarding

Keputusan: acting salary, evaluasi dan SK, dampak SP pada payroll, eligibility blacklist/banned dan expiry, ikatan dinas, final settlement serta penerima informasi sensitif.

Owner usulan: HR, Management, Legal. Dampak: CAR-01, CAR-02, DIS-01, DOC-01, OFF-01, OFF-02. Gate: sebelum aktivasi employee lifecycle.

### D10 | APD, custody, dan pengadaan

Keputusan: tetapkan lifecycle barang, probation/masa kerja, ganti rugi, write-off/consume, batas form clearance versus inventory, minimum stock, dan approval GR/GI. Hindari dua sumber pengakuan biaya.

Owner usulan: GA, HSE/IT, Logistics, Finance. Dampak: AST-01, AST-02, PRO-01, PRO-02, GA-07, OFF-02. Gate: sebelum desain inventory dan clearance.

### D11 | Nomor employee dan konversi kandidat

Keputusan: tentukan apakah NIK employee terbentuk saat pengajuan induksi atau orientasi, pola nomor, cut-off, penanganan existing employee dan rehire. NIK KTP harus tetap dipisahkan dari nomor employee.

Owner usulan: HR HO/Site. Dampak: EMP-01, REC-04. Gate: sebelum migrasi employee/recruitment.

### D12 | Kanal portal dan interface

Keputusan: versi/edisi Odoo, spesifikasi fingerprint export, kanal job portal, format transfer, portal cuti/travel/survey, template notifikasi dan batas WA manual. Identifikasi API yang benar-benar tersedia.

Owner usulan: HR, GA, IT, tim implementasi. Dampak: REC-04, ATT-01, LEV-02, GA-01, GA-06, INT-01 sampai INT-07. Gate: sebelum desain integrasi.

### D13 | Report, reminder, dan dokumen

Keputusan: format report/slip, penerima dan kanal reminder, tanggal efektif, rumus expired SIMPER, ambang kontrak dalam hari, dan kewajiban kendaraan yang berlaku.

Owner usulan: HR, GA, Finance. Dampak: DOC-01, GA-07, RPT-01 sampai RPT-08. Gate: sebelum pengujian report/reminder.

### D14 | Matriks approval dan kewenangan

Keputusan: perjelas semua tahap payroll, PTK, MPP, kontrak/evaluasi, karier dan pengadaan; pisahkan validator dan approver; tentukan delegasi, reject/resubmit, self-approval, serta perilaku saat budget MPP terlampaui.

Owner usulan: HR, GA, Finance, Management. Dampak: SEC-02, REC-01, REC-02, REC-04, PAY-04, CAR-01, CAR-02, PRO-01. Gate: sebelum workflow diaktifkan.

### D15 | Accounting, accrued, dan CA

Keputusan: tetapkan COA, analytic wajib/opsional, tanggal accrued/reversal/realisasi versus tanggal pembayaran, proses close/reopen, serta settlement CA dan bukti. Bedakan pengajuan, posting dan pembayaran.

Owner usulan: Finance/Accounting, HR, GA. Dampak: FIN-01 sampai FIN-05, GA-08. Gate: sebelum posting accounting/UAT rekonsiliasi.

### D16 | Delivery, migrasi, dan operasional

Keputusan: fase/prioritas scope, kebutuhan custom versus standard, volume employee/user/data, histori migrasi, hosting, SLA, retention, backup/RPO/RTO, support, dan owner sign-off. Jadwal dan biaya ditetapkan terpisah.

Owner usulan: Project Owner GPE, IT, tim implementasi. Dampak: seluruh scope, NFR-01, NFR-04 dan migrasi. Gate: sebelum baseline delivery dan deployment.

---

# Paket data GPE dan persetujuan baseline

## Checklist bahan workshop

- Struktur organisasi, site/company, jabatan, daftar employee dan work schedule HO; terkait D01/D07/D11.
- Matriks komponen/rate payroll AKP-GAM-HO, eligibility, insentif HM/productivity, sampel hitungan dan slip; terkait D04-D07.
- Jenis cuti, kebijakan carryover, roster tahunan, perubahan roster dan contoh form; terkait D07/D08.
- Matriks approval seluruh transaksi beserta validator, approver, delegasi dan batas nominal; terkait D02/D14.
- Form PTK/MPP, pipeline recruitment, kontrak, evaluasi, SK, SP, offboarding dan template notifikasi; terkait D09/D11-D14.
- Master mess/vendor/layanan, daftar harga travel/laundry/meals, occupancy dan contoh invoice bulk; terkait D03/D04.
- Daftar barang/APD, masa pakai, minimum stock, gudang, kendaraan serta contoh SPB/MOL/GR/GI; terkait D10/D13.
- COA dan analytic, contoh jurnal accrued/reversal/realisasi, saldo loan/CA dan aturan settlement; terkait D02/D15.
- Contoh report existing, daftar dokumen/reminder, spesifikasi file/interface serta jumlah data/user; terkait D12/D13/D16.

## Proses review yang diusulkan

Review kebutuhan per fungsi terlebih dahulu, lalu selesaikan keputusan lintas fungsi HR-GA-Finance. Tim implementasi melakukan fit-gap terhadap versi Odoo yang disepakati dan menyusun desain serta estimasi terpisah. Baseline ditetapkan setelah perubahan dokumen dan daftar pengecualian disetujui pemilik proses.

Setelah baseline, perubahan kebutuhan dicatat dengan ID requirement terdampak, alasan, dampak biaya/jadwal/risiko, dan keputusan persetujuan. Dokumen ini tidak memberikan otorisasi untuk mengubah sistem produksi.

## Lembar review dan persetujuan

| Fungsi reviewer | Nama | Status / tanggal |
| --- | --- | --- |
| HR HO / HR Site | Diisi GPE | Belum direview |
| GA / Operations | Diisi GPE | Belum direview |
| Finance / Accounting / Tax | Diisi GPE | Belum direview |
| IT / Security | Diisi GPE | Belum direview |
| Project Owner / Management | Diisi GPE | Belum disetujui |
| Tim implementasi | Diisi saat review | Belum direview |

Pernyataan baseline: ruang lingkup yang diterima, requirement yang ditunda, keputusan OPEN yang dikecualikan, dan lampiran aturan final harus dicantumkan pada saat persetujuan. Kolom review yang masih kosong bukan bentuk persetujuan.

## Riwayat versi

v0.1 | 2 September 2026 | Draft awal berdasarkan summary MOM dan topik sumber; penambahan ID requirement, kriteria penerimaan usulan, integrasi, UAT, serta daftar keputusan terbuka. Belum dilakukan validasi regulasi atau sign-off GPE.
