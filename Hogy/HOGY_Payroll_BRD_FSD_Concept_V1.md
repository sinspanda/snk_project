# Konsep BRD dan FSD Payroll PT Hogy Indonesia

Tanggal: 7 Oktober 2026  
Sistem: Microsoft Dynamics 365 Finance and Operations  
Baseline: Blueprint NSI HOGY Payroll System V1.5 tanggal 7 Oktober 2026  
Tujuan: menyediakan konsep proses dan requirement yang dapat dikembangkan menjadi BRD, FSD, backlog development, dan skenario UAT.

Dokumen ini memetakan kebutuhan pada blueprint menjadi spesifikasi yang dapat ditelusuri oleh konsultan dan tim teknikal. Fokus utama adalah kesinambungan identitas karyawan, ketepatan sumber payroll, riwayat tanggal efektif, kontrol perubahan, dan rekonsiliasi hasil. Formula serta keputusan bisnis yang belum lengkap harus dikonfirmasi sebelum bagian terkait dinyatakan siap dikembangkan.

## 1 Cara menggunakan dokumen

**B** berarti kebutuhan dinyatakan pada blueprint. **D** berarti usulan desain atau kontrol tambahan untuk memenuhi kebutuhan tersebut. **K** berarti keputusan bisnis atau teknis yang belum ditentukan. Label B tidak berarti requirement telah ditandatangani; status persetujuan baseline tetap mengikuti pengendalian dokumen proyek.

Setiap requirement menggunakan kode `HG-AREA-NNN`. Referensi `HG.EMP.01` dan sejenisnya adalah Activity ID pada blueprint. Nama entitas dan form dalam dokumen ini merupakan konsep logis, bukan nama tabel, class, atau menu D365FO yang sudah diverifikasi. Tim teknikal harus melakukan fit-gap pada environment target sebelum menetapkan objek standard, extension, atau custom.

BRD menjelaskan kebutuhan, pemilik proses, aturan bisnis, scope, dan keberhasilan yang diharapkan. FSD menjelaskan bagaimana kebutuhan tersebut diwujudkan melalui form, field, status, validasi, perhitungan, interface, output, dan hak akses. TDD selanjutnya menetapkan objek D365FO, extension, batch, transaction boundary, deployment, dan penanganan concurrency.

## 2 Hasil analisis blueprint

Blueprint sudah mencakup master data, komponen payroll, tarif pajak, jadwal shift, cuti, lembur, contoh laporan, dan aktivitas end to end. Area yang paling siap diturunkan adalah pendaftaran, kontrak, mutasi, serta urutan payroll. Area yang masih perlu spesifikasi rinci adalah formula komponen, accrual cuti, pairing fingerprint, realisasi lembur, mapping output, dan penanganan perubahan setelah finalisasi.

| ID gap | Referensi sumber | Temuan | Dampak dan tindak lanjut |
|---|---|---|---|
| GAP-01 | Document History 1.1; 4.3; 4.4 | Pengajuan cuti dan lembur dilakukan di luar D365, tetapi narasi masih menyebut Submit, sistem memvalidasi, dan workflow | Pisahkan aktivitas eksternal dari input HR di D365. Jangan mengembangkan employee self service dari narasi tersebut tanpa perubahan scope |
| GAP-02 | 4.1.1; 4.1.2 | NPK berubah mengikuti employment type atau kontrak aktif | Gunakan identitas internal yang tetap dan alias NPK berdasarkan tanggal efektif. Semua histori harus tetap milik orang yang sama |
| GAP-03 | 4.1.2 | Istilah kontrak terakhir atau terupdate berpotensi berbeda dari kontrak yang efektif | Kontrak future-dated tidak boleh langsung mengganti NPK, kompensasi, atau organisasi hari ini |
| GAP-04 | 4.1.1; 2.4 | Join date terkait status kepegawaian; tabel upah memakai masa kerja | Pisahkan first join, awal hubungan kerja, permanent date, dan service date untuk benefit; tentukan tanggal acuan tiap formula |
| GAP-05 | 2.9; 2.10 | Position masih berupa contoh terbatas; beberapa job level code berulang | Bedakan position, job, grade, dan role. Satu grade dapat dipakai banyak jabatan; jangan menjadikan kode grade sebagai unique key jabatan |
| GAP-06 | 2.6 | Deskripsi Site mengulang kelompok department, sedangkan kode adalah HOGY 1, HOGY 2, HI Jakarta | Tetapkan hierarki legal entity, lokasi, department, section, posisi, dan financial dimension |
| GAP-07 | 2.2; 2.4 | Formula banyak ditulis sesuai ketentuan; tabel upah tersedia sebagai gambar | Susun katalog formula dan minta tabel upah terstruktur. Jangan mentranskripsikan seluruh nominal dari gambar sebagai master produksi |
| GAP-08 | 2.2; 2.13 | OT eligibility berbeda: Operator–Spv, Operator–Leader/Staff, Foreman/Chief, Spv/Asst Manager | Buat matriks level × day type × cash OT × transport/benefit dan sign-off satu kebijakan |
| GAP-09 | 2.13; HG.ATT.07 | Potongan terlambat menggunakan tarif per jam dikali late minutes | Satuan belum konsisten. Jika durasi menit, diperlukan konversi /60. Konfirmasi juga perlakuan toleransi 2 menit |
| GAP-10 | 2.11 | Shift memiliki jumlah break, tetapi waktu dan durasi break belum lengkap | Jam kerja bersih dan OT tidak dapat dihitung hanya dari jumlah break; perlu interval serta paid/unpaid break |
| GAP-11 | 2.12; 4.3 | Half day ada sebagai jenis cuti tersendiri sekaligus durasi annual leave | Tentukan apakah half day hanya unit durasi atau policy terpisah agar saldo tidak dipotong dua kali |
| GAP-12 | 2.12 | Prorata, cuti ganti hari, cuti masa kerja, cuti menyusul belum memiliki formula dan lifecycle lengkap | Lengkapi basis prorata, expiry, pembulatan, sumber entitlement, reversal, dan pengaruh payroll |
| GAP-13 | 2.12 | Maternity dan miscarriage berupa policy draft | HR perlu memvalidasi terhadap peraturan serta kebijakan yang berlaku sebelum dibuat konfigurasi final |
| GAP-14 | 2.2 | Bonus Direksi muncul bersama istilah Deviden, lalu muncul kembali sebagai baris terpisah | Klarifikasi apakah duplikasi, tantiem/bonus kerja, atau dividen. Jangan otomatis menerapkan satu tax treatment |
| GAP-15 | 3.1.6 | XML BPMP, A1, dan BP21 berupa contoh; judul BP21 menyebut pegawai tetap | Tentukan jenis bukti potong dan kode objek per transaksi. Sample bukan pengganti schema dan mapping resmi |
| GAP-16 | 3.1.6 | Sample A1 memiliki NumberOfMonths 0 dan flag gross-up; sample BPMP memakai DTP | Verifikasi semantik field dan eligibility. Nilai sample tidak boleh menjadi default untuk semua karyawan |
| GAP-17 | 3.2.2; Document History 1.1 | Slip hanya dibuka/diunduh karyawan terkait; pengajuan mandiri dikeluarkan dari scope; slip juga dikirim email berpassword | Tentukan kanal distribusi: email, portal, atau keduanya. Akses HR/payroll berwenang tetap perlu dirumuskan |
| GAP-18 | 4.5; 4.1.4 | Regular, adjustment, termination, simulation belum memiliki aturan hubungan antarrun | Cegah pembayaran, potongan, dan akumulasi pajak ganda; simulation tidak mengubah ledger maupun YTD |
| GAP-19 | 4.5 | Reopen disebut tanpa batasan setelah bank transfer atau posting GL | Bedakan recalculate draft, reopen sebelum pembayaran, dan koreksi setelah paid/posted menggunakan adjustment/reversal |
| GAP-20 | 3.1; 3.2 | Laporan sebagian besar berupa screenshot | Buat katalog field, grain, filter, total, grouping, format, dan sumber data per report |
| GAP-21 | 2.1 | Jumlah karyawan tidak dibatasi | Tetap perlu angka volume UAT dan SLA; tidak dibatasi secara fungsi bukan berarti kapasitas atau waktu proses tanpa batas |
| GAP-22 | 4.5; scope | Migrasi data awal belum merinci YTD pajak/payroll dan saldo cuti | Go-live di tengah tahun memerlukan opening YTD serta rekonsiliasi, bukan hanya employee master |

## 3 Pembagian paket dokumentasi

| Paket | Isi BRD | Isi FSD | Dependensi |
|---|---|---|---|
| FSD-01 Employee and Organization | Identitas, struktur organisasi, keluarga, payroll readiness | Field mapping, alias NPK, employment/service date, keamanan | Master organisasi |
| FSD-02 Contract and Compensation | Kontrak, tabel upah, eligibility benefit | Effective dating, komponen assignment, validasi overlap | FSD-01 |
| FSD-03 Mutation | Mutasi, promosi/demosi, penugasan sementara | Workflow, tanggal efektif, perubahan atomik, amendment | FSD-01/02 |
| FSD-04 Schedule and Attendance | Shift, kalender, import dan koreksi kehadiran | Parser, pairing, rules, exception, source freeze | FSD-01 |
| FSD-05 Leave | Hak, penggunaan, cuti menyusul, cuti ganti hari | Ledger saldo, accrual, reversal, integrasi attendance | FSD-01/04 |
| FSD-06 Overtime | SPL eksternal dan realisasi payable | Header/line SPL, rekonsiliasi, eligibility dan tier | FSD-02/04 |
| FSD-07 Payroll Engine | Penghasilan, potongan, BPJS, ASKOM, pajak, FX | Formula catalog, input, calculation trace, tax YTD | FSD-01/02/04/05/06 |
| FSD-08 Payroll Control | Periode, approval, finalisasi, adjustment, closing | State machine, snapshot, concurrency, koreksi | FSD-07 |
| FSD-09 Termination | Final settlement dan termination payroll | External component import, overlap regular, final tax | FSD-07/08 |
| FSD-10 Payment and Accounting | Transfer Mandiri dan posting GL | File contract, bank reconciliation, mapping akun | FSD-08 |
| FSD-11 Reports and Statutory Output | Laporan, slip, paklaring, Coretax | Dataset mapping, template, keamanan distribusi | Seluruh paket terkait |
| FSD-12 Migration and Operations | Migrasi, akses, operasional, notifikasi | Load order, YTD opening, reconciliation, batch, SLA | Seluruh paket terkait |

## 4 Alur utama yang diusulkan

Master organisasi dan policy → data karyawan → kontrak dan payroll assignment → working schedule → fingerprint staging → attendance tervalidasi → input cuti dan SPL yang disetujui eksternal → rekonsiliasi attendance/cuti/OT → payroll input → perhitungan → review → approval → snapshot final → output → pembayaran dan posting jurnal → rekonsiliasi → closing.

Perubahan efektif kontrak atau mutasi menjadi input pada proses yang sesuai tanggal bisnisnya. Termination dan adjustment memakai engine yang sama dengan cakupan dan kontrol khusus. Setiap output payroll harus menunjuk versi hasil yang telah difinalisasi.

## 5 Konsep tiap proses dan requirement

### 5.1 Master organisasi dan policy

**Dasar blueprint:** 2.4–2.13. **Tujuan bisnis:** menyediakan referensi yang konsisten untuk penempatan, kompensasi, jadwal, benefit, approval, pelaporan, dan biaya. **PIC:** HR Admin, HR Manager, Finance untuk financial dimension.

**Alur:** siapkan master → validasi struktur dan kode → tentukan tanggal efektif → assign kepada karyawan/kontrak → uji dampak payroll → aktifkan konfigurasi.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-MST-001 | B | Menyediakan employment type, site, department, section, position, job level, tabel upah, work profile, leave policy, dan payroll policy |
| HG-MST-002 | D | Memisahkan legal entity dari site; validasi relasi section–department dan penempatan posisi agar kombinasi tidak sah ditolak |
| HG-MST-003 | D | Master yang memengaruhi nilai perhitungan memiliki effective from/to dan versi; perubahan tidak menimpa hasil final periode lama |
| HG-MST-004 | D | Job grade dan nama jabatan dipisahkan; grade 1A dapat dipakai Operator dan Reception tanpa duplikasi key grade |
| HG-MST-005 | B+D | Tabel upah mendukung tahun/versi, masa kerja, level/kategori, employment type, gaji pokok, TMK dan tanggal berlaku; tabel sumber menyatakan masa kerja di atas 30 tahun memakai baris 30 tahun |
| HG-MST-006 | K | Konfirmasi arti Level A/B/C pada tabel upah terhadap job level 1A–4C, masa kerja acuan, annual increase, serta auto update atau update dengan approval |

**Konsep data:** OrganizationReference, PositionReference, JobGrade, WageTableHeader/Line, PolicyVersion. Field kode berupa teks; nominal berupa decimal; tanggal efektif berupa date. Nilai total tabel upah merupakan kontrol penjumlahan, bukan komponen tambahan yang dibayarkan di samping komponen penyusunnya.

**Validasi dan exception:** kode duplikat; relasi organisasi invalid; periode versi overlap; wage lookup tidak menemukan baris; nilai negatif; konfigurasi expired. Setup tanpa formula yang disetujui tidak boleh diam-diam menghasilkan nol.

**Output:** master tervalidasi, workbook konfigurasi, daftar mapping dimensi. **UAT:** satu grade dipakai dua jabatan; masa kerja 31 tahun memilih baris 30 sesuai policy; gaji Januari tidak berubah saat tabel baru efektif Juli.

### 5.2 Pendaftaran dan pemeliharaan karyawan

**Dasar blueprint:** 2.1; HG.EMP.01–04. **Tujuan:** satu identitas karyawan digunakan lintas kontrak, absensi, cuti, payroll, dan pajak. **PIC:** HR Admin.

**Alur:** terima dokumen yang telah disetujui → input personal/statutory/organisasi → verifikasi → simpan → cek readiness payroll → lanjutkan kontrak.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-EMP-001 | B | Menyimpan identitas, hubungan kerja, organisasi, posisi, keluarga, NIK/NPWP, PTKP, BPJS, rekening dan data pendukung dari sistem lama yang disepakati |
| HG-EMP-002 | B+D | Perubahan status atau promosi tidak membuat employee baru. Gunakan WorkerKey yang tetap serta histori NPK bertanggal efektif |
| HG-EMP-003 | D | Attendance ID, legacy employee number, NPK, dan WorkerKey memiliki mapping terpisah; pencarian alias memakai tanggal event |
| HG-EMP-004 | B+D | Memisahkan first join date, employment start, permanent date, service date, dan termination date; formula memilih tanggal acuan yang disetujui |
| HG-EMP-005 | D | Menyediakan payroll readiness checklist untuk kontrak, rekening, statutory, komponen dan schedule; field wajib dapat bergantung pada kategori karyawan |
| HG-EMP-006 | B | Tidak menerapkan batas jumlah record karyawan berdasarkan jumlah saat sign-off; benchmark kapasitas mengikuti requirement operasional |

**Konsep form:** Employee detail dengan kelompok Personal, Employment, Organization, Statutory, Bank, Family, Identifier History, Payroll Readiness. Screenshot sumber adalah referensi field; field wajib final harus dibuat dalam mapping workbook.

**Konsep data keluarga:** relasi, nama, gender bila dibutuhkan, tempat/tanggal lahir, alamat, kontak, status bekerja, status hidup, tanggungan, emergency contact, identitas, BPJS/asuransi, effective date. Pisahkan flag tanggungan benefit dari tanggungan pajak; perubahan anggota keluarga tidak langsung mengubah PTKP tahun berjalan tanpa aturan dan verifikasi.

**Validasi:** NIK dan nomor rekening disimpan sebagai teks, leading zero dipertahankan; deteksi identitas duplikat; tanggal lahir tidak melewati tanggal bisnis; alias aktif tidak tumpang tindih untuk identitas fingerprint yang sama; perubahan rekening/statutory memiliki audit trail dan kewenangan khusus.

**Output:** employee master, riwayat identitas, readiness exceptions. **UAT:** kontrak menjadi permanent menghasilkan NPK baru tetapi histori pajak dan attendance tetap satu orang; fingerprint tanggal lama memakai alias lama; data tidak lengkap tertahan sebelum payroll.

**K:** format dan sequence NPK per employment type; aturan rehire dan masa kerja berkelanjutan; scope field lama; siapa berwenang melihat gaji serta data keluarga.

### 5.3 Kontrak dan assignment kompensasi

**Dasar blueprint:** HG.CON.01–05; 2.2; 2.4. **PIC:** HR Admin. **Alur:** terima kontrak terkonfirmasi → input periode/penempatan/komponen → verifikasi → simpan versi efektif → cetak.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-CON-001 | B | Menyimpan nomor/jenis kontrak, tanggal mulai/akhir, posisi, organisasi, employment type, ketentuan kompensasi dan lampiran |
| HG-CON-002 | B | Komponen tetap dan berulang ditautkan ke kontrak atau payroll assignment; riwayat tidak ditimpa |
| HG-CON-003 | D | Kontrak future-dated tidak langsung mengaktifkan NPK atau gaji. Selection didasarkan pada tanggal efektif, bukan tanggal terakhir diedit |
| HG-CON-004 | D | Cegah overlap pada kontrak/assignment utama; amendment memiliki referensi ke versi sebelumnya dan tanggal efektif |
| HG-CON-005 | B+D | Komponen default ditentukan eligibility; penyimpanan ulang tidak menggandakan assignment. Override harus memiliki alasan dan otorisasi |
| HG-CON-006 | B+K | Menghasilkan dokumen kontrak dari data tersimpan; layout, penandatangan, numbering dan bahasa perlu dikonfirmasi |

**Data:** ContractHeader, CompensationAssignment, ContractAttachment, IdentifierAssignment. Komponen memiliki currency, amount/formula reference, effective from/to, recurring flag dan eligibility reference.

**UAT:** kontrak Juli disimpan Juni tidak mengganti gaji Juni; dua periode overlapping ditolak; promosi tanggal 15 menghasilkan pemilihan kompensasi sesuai kebijakan split yang disetujui; cetak ulang kontrak lama memakai data versi lama.

**K:** aturan prorata perubahan gaji tengah bulan; kontrak primary/secondary; approval kontrak; pembatasan probation sesuai jenis hubungan kerja; urutan prioritas nilai kontrak terhadap tabel upah.

### 5.4 Mutasi promosi demosi dan penugasan sementara

**Dasar blueprint:** HG.MUT.01–07. **PIC:** Requesting Manager, HR Manager, HR Admin. **Alur:** Draft → submit → review → Approved/Refused → menunggu efektif → Process Mutation → amendment bila perlu → Done.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-MUT-001 | B | Form menyimpan kondisi asal/tujuan, jenis, alasan, tanggal efektif dan pengusul |
| HG-MUT-002 | B | Workflow menyediakan submit, approve, refuse, cancel sesuai peran dan kondisi |
| HG-MUT-003 | B | Mutasi disetujui baru diproses pada tanggal efektif melalui Process Mutation oleh HR Admin |
| HG-MUT-004 | B+D | Penugasan sementara tidak mengganti kontrak utama; simpan tanggal berakhir dan assignment sementara serta mekanisme kembali |
| HG-MUT-005 | B+D | Promosi/demosi mengaitkan perubahan grade, posisi, kompensasi dan eligibility dengan kontrak/amendment baru |
| HG-MUT-006 | D | Pembaruan organisasi dan amendment terkait dilakukan konsisten; jangan menandai Done jika kontrak wajib belum berhasil |
| HG-MUT-007 | D | Approved adalah hasil persetujuan; Pending effective date dapat menjadi indikator kesiapan. Hindari dua status yang maknanya saling tumpang tindih |

**Data:** MutationRequest, BeforeAfterSnapshot, WorkflowHistory, EffectiveAssignment. **Validasi:** tanggal efektif, tujuan valid, konflik mutasi, sumber data berubah setelah approval, periode payroll terkunci, kontrak belum siap.

**UAT:** approved hari ini efektif bulan depan tetap mempertahankan posisi lama; klik Process dua kali tidak menghasilkan dua kontrak; kegagalan amendment tidak meninggalkan posisi baru dengan gaji lama; temporary assignment kembali sesuai tanggal.

**K:** scope akses manager; perubahan kompensasi dalam mutasi permanen selain promosi; mutasi backdated; approval ulang jika data tujuan berubah.

### 5.5 Pemberhentian dan termination payroll

**Dasar blueprint:** HG.TER.01–09. **PIC:** HR Admin, HR Manager/Finance, Payroll Officer.

**Alur:** terima dokumen pemberhentian eksternal → catat termination → hitung dan setujui komponen khusus di luar D365 → buka termination run → engine menghitung komponen otomatis → input komponen khusus → rekonsiliasi → finalisasi → output dan pembayaran.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-TER-001 | B | Menyimpan alasan, tanggal kerja terakhir dan referensi dokumen; approval pemberhentian tetap di luar D365 |
| HG-TER-002 | B | Termination engine menghitung komponen otomatis yang telah dikonfigurasi, termasuk prorata, potongan, attendance, BPJS, ASKOM, pajak akhir dan FX |
| HG-TER-003 | B+D | External settlement hanya memasok komponen khusus yang belum dihitung sistem; simpan kategori dan referensi sumber untuk mencegah duplikasi |
| HG-TER-004 | D | Regular dan termination run memiliki coverage date serta settlement reference agar gaji/benefit satu rentang tidak dibayar dua kali |
| HG-TER-005 | B | Rekonsiliasi draft termination payslip terhadap settlement eksternal sebelum finalisasi |
| HG-TER-006 | B+K | Menghasilkan final payslip, paklaring, laporan settlement dan output pajak sesuai klasifikasi transaksi yang dikonfirmasi |

**Data:** TerminationCase, ExternalSettlementLine, SettlementReconciliation, PayrollRun link. Simpan amount otomatis, amount eksternal, expected total, variance, alasan koreksi dan reviewer.

**UAT:** gaji regular telah dibayar sebagian dan termination hanya menyelesaikan hak tersisa; pesangon eksternal tidak muncul dua kali; variance bukan nol menghambat finalisasi sampai diselesaikan/diterima berwenang; karyawan nonaktif tetap dapat dipilih untuk settlement yang sah.

**K:** gaji terakhir dibayar regular atau termination; unused leave payout; outstanding loan; jenis dan tax treatment pesangon/kompensasi/pensiun; workflow final payroll mengikuti approval regular atau khusus. Jangan menyimpulkan seluruh formula pesangon otomatis dari daftar komponen karena flow sumber menetapkan perhitungan khusus eksternal.

### 5.6 Working schedule

**Dasar blueprint:** 2.11; HG.WS.01–05. **PIC:** HR Admin.

**Alur:** pilih periode/cakupan → tampilkan default profile → ubah tanggal tertentu → simpan exception calendar → verifikasi jadwal efektif.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-WS-001 | B | Jadwal efektif merupakan default employee/group profile ditambah perubahan pada profile calendar |
| HG-WS-002 | B | Mendukung 3 shift, long shift, non-shift, driver/bus, security, Jumat, Ramadan, OFF dan kalender libur |
| HG-WS-003 | D | Setiap shift memiliki start/end datetime, day offset untuk lintas tengah malam, interval break, paid/unpaid flag dan day classification |
| HG-WS-004 | B+D | Laporan jadwal dapat ditelusuri ke employee, work date, profile dan sumber override; jadwal periode yang dibekukan tidak berubah diam-diam |
| HG-WS-005 | K | Urutan konflik antara public holiday, group schedule, employee override, temporary assignment dan Ramadan harus ditetapkan |

**Form/data:** Work Planner, Profile Calendar, EffectiveSchedule, ShiftBreak. Konsep memanfaatkan fitur yang dinyatakan standard pada blueprint; ketersediaan modul, lisensi, extension dan entity di environment target masih harus diverifikasi.

**UAT:** 23.00–07.00 menghasilkan work date awal shift dengan checkout hari berikutnya; OFF profile yang memiliki rentang jam tidak otomatis menjadi hari kerja berbayar; override satu hari tidak mengubah hari lain; break tidak dihitung ganda.

### 5.7 Import fingerprint dan pemrosesan attendance

**Dasar blueprint:** HG.ATT.01–08; contoh file fingerprint. **PIC:** Attendance Operator/IT untuk rantai eksternal; HR Admin untuk D365.

**Batas sistem:** penarikan 24 mesin Amano → TA → proses Copy Finger Server 11/10 → Daikintai/TA → export tetap mengikuti proses eksternal. Batas custom D365 dimulai pada import file ke Attendance Staging; direct connection ke mesin/server tidak otomatis termasuk scope.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-ATT-001 | B | Mengimpor file output existing ke staging tanpa mengganti sumber asli |
| HG-ATT-002 | D | Menyimpan batch ID, nama/hash file, raw line, row number, source, waktu import, uploader, parse status dan alasan error |
| HG-ATT-003 | B+D | Validasi employee alias, tanggal/timestamp, machine/source, duplikasi dan jadwal efektif; exact duplicate tidak menjadi punch baru |
| HG-ATT-004 | D | Bentuk attendance dari event tervalidasi dengan aturan pairing, overnight window, missing punch dan multiple punch yang disetujui |
| HG-ATT-005 | B | Satu form Employee Attendance digunakan untuk review jam masuk/pulang, late, early leave, absent, actual hours serta rekonsiliasi cuti/OT/koreksi |
| HG-ATT-006 | B+K | Toleransi masuk terlambat dan pulang cepat 2 menit; batas inclusive, pembulatan, durasi setelah toleransi dan label status perlu dipastikan |
| HG-ATT-007 | D | Koreksi memakai correction record dengan alasan/reviewer; raw punch tetap utuh dan histori derivasi tersimpan |
| HG-ATT-008 | D | Reprocess batch tidak menggandakan attendance; jika sumber payroll final, proses menampilkan dampak dan mengikuti koreksi periode yang berwenang |

**Kontrak file wajib FSD:** format fixed width/delimited; encoding; posisi start/length setiap field; date/time format; timezone; machine code; direction; employee identifier; record length; blank/header/trailer; checksum/control count; filename/version; file malformed. Gambar berupa deretan angka belum memberikan definisi offset; minta sample file asli dan spesifikasi export dari IT Hogy.

**Usulan klasifikasi:** Imported → Parsed → Validated → Processed atau Rejected; attendance memiliki valid/exception/reconciled/frozen. Absence sebaiknya ditetapkan setelah jadwal, leave dan correction diperiksa, bukan setiap missing punch langsung unpaid absence.

**UAT:** upload file identik dua kali; unknown alias; satu punch saja; dua checkout; lintas mesin; shift malam; checkout tengah malam; terlambat 1/2/3 menit; pulang awal; cuti setengah hari; file rusak parsial. FSD menentukan atomic per batch atau per row dan apakah baris valid dapat diproses saat baris lain error.

### 5.8 Pengelolaan cuti

**Dasar blueprint:** 2.12; HG.LEV.01–07; revisi 1.1. **PIC:** Employee dan atasan di luar D365; HR Admin di D365.

**Alur:** pengajuan dan persetujuan eksternal → HR cek policy/saldo/dokumen → input transaksi disetujui di D365 → validasi sistem → posting leave ledger → perbarui attendance → kontrol payroll.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-LEV-001 | B | HR menginput cuti yang telah disetujui di luar sistem, mencatat referensi approval dan lampiran |
| HG-LEV-002 | B | Mendukung annual leave, special leave, maternity, miscarriage, tenure leave, cuti ganti hari dan half day sesuai policy final |
| HG-LEV-003 | B+D | Annual leave 12 hari kerja/tahun pada draft; entitlement prorata, expiry, cuti bersama dan saldo migrasi diproses sebagai transaksi ledger |
| HG-LEV-004 | B+K | Durasi 0,5 hari diperbolehkan untuk policy yang sesuai; definisi first/second half serta split attendance disepakati |
| HG-LEV-005 | D | Validate balance, eligibility, overlap, working day dan attachment ketika HR memposting; cuti eksternal yang disetujui belum tentu lolos validasi data |
| HG-LEV-006 | B+K | Cuti menyusul dapat mengubah klasifikasi absence menjadi annual leave; mekanisme koreksi potongan yang sudah dibayar mengikuti adjustment |
| HG-LEV-007 | D | Cancellation/reversal mengembalikan saldo tepat sekali serta membatalkan dampak attendance; simpan histori referensi |
| HG-LEV-008 | K | Cuti ganti hari perlu definisi event pemberi hak, nilai konversi, expiry, approval dan apakah menggantikan cash OT |

**Data:** LeavePolicy, LeaveEntitlement, LeaveTransaction, LeaveBalanceLedger, ExternalApprovalReference. Balance = opening + earned + adjustment − used + reversal − expired. Daftar keluarga tidak boleh menjadi satu-satunya bukti eligibility tanpa policy pendukung.

**UAT:** annual leave 0,5 hari memotong 0,5; special leave tidak memotong annual bila policy demikian; OFF day tidak mengurangi saldo bila dihitung working day; pembatalan dua kali tidak mengembalikan dua kali; cuti bersama tidak dipotong ulang pada leave request; backdated setelah payroll menghasilkan koreksi yang terlacak.

**K:** entitlement grant saat join/anniversary/awal tahun; prorata berdasarkan bulan atau hari; rounding 0,5; carry forward; nilai hak 10/20 tahun; apakah cuti setengah hari adalah type atau duration; sick/permit/status lain yang ada di sample report; paid/unpaid effect per type.

### 5.9 Pengelolaan SPL dan realisasi lembur

**Dasar blueprint:** 2.13; HG.OT.01–06. **PIC:** requester, Department Head, PGA Manager, Factory Director di luar D365; HR Admin untuk input.

**Alur:** rencana dan approval eksternal → HR input SPL approved → cocokkan dengan effective schedule dan actual fingerprint → tentukan actual eligible duration → review exception → freeze payable OT → payroll.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-OT-001 | B | Form HR mencatat SPL untuk satu/banyak karyawan, tanggal, waktu rencana, alasan dan referensi approval eksternal |
| HG-OT-002 | B+D | Menyimpan planned, actual, approved dan payable duration terpisah agar dasar pembayaran dapat ditelusuri |
| HG-OT-003 | B+K | Eligibility berdasarkan grade/role dan day type; aturan Supervisor/Assistant Manager serta Foreman/Chief wajib disatukan |
| HG-OT-004 | B+K | Cash OT menggunakan eligible wage /173 × durasi jam × multiplier per tier; wage basis dan seluruh tier harus disetujui |
| HG-OT-005 | D | Missing punch, actual di luar SPL, overlap shift/leave, OT lintas hari dan absence menghasilkan exception; tidak otomatis bayar |
| HG-OT-006 | D | Input/reprocess idempotent terhadap SPL reference, employee dan tanggal/waktu; perubahan setelah final mengikuti adjustment |
| HG-OT-007 | K | Tetapkan apakah payable = irisan waktu SPL approved dan actual, serta apakah perlu klaim/review tambahan setelah realisasi |

**Data:** OvertimeHeader/Line, Realization, EligibilityMatrix, MultiplierTier, PayableOT. Benefit transport atau holiday untuk level tertentu menggunakan komponen terpisah dari cash OT.

**UAT:** actual melebihi SPL; SPL ada tetapi punch tidak ada; Foreman weekday dibanding holiday; hari libur 5-day/6-day calendar; overlapping SPL; crossing midnight; input ulang; penugasan sementara yang mengubah schedule.

**K:** aturan rounding menit, minimum durasi, break, maksimum/exception, workday/holiday tier, meal entitlement, dan wage component basis. Tier 2,0 pada draft tidak cukup sebagai definisi seluruh holiday OT.

### 5.10 Katalog komponen dan input payroll

**Dasar blueprint:** 2.2; HG.PAY.04–05. **PIC:** HR/payroll consultant, Payroll Officer; Finance untuk treatment akuntansi.

**Konsep:** master komponen mendefinisikan sifat dan formula; assignment menentukan eligibility karyawan; input transaction memasok nilai variabel; calculation line menyimpan hasil dan asalnya. Pisahkan komponen grouping seperti Tunjangan/Transport/Pesangon dari komponen yang benar-benar dibayarkan.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-CMP-001 | B | Mendukung seluruh komponen blueprint yang telah dinormalisasi, termasuk bonus direksi dan potongan lainnya |
| HG-CMP-002 | D | Setiap komponen memiliki stable code, earning/deduction/employer cost/noncash, currency, sumber nilai, formula, eligibility, effective date dan rounding |
| HG-CMP-003 | D | Mendefinisikan inclusion dalam cash THP, taxable gross, BPJS wage basis, OT wage basis, THR basis, report category dan GL mapping secara terpisah |
| HG-CMP-004 | B+D | Input/upload komponen variabel memuat employee, period, component, quantity/rate/amount, currency, source reference dan approved reference |
| HG-CMP-005 | D | Import memvalidasi duplicate reference, inactive employee eligibility, component valid, currency/rate, nominal dan period state; tampilkan control total serta error rows |
| HG-CMP-006 | D | Tetapkan precedence assignment/default/manual override agar source yang sama tidak dibayarkan dua kali |
| HG-CMP-007 | B+K | Bonus, THR, leave paid, koperasi, serikat, compensation dan lainnya pada tabel memiliki sumber upload; konfirmasi mana nominal final eksternal dan mana dihitung sistem |

**Worksheet formula yang wajib dibuat:** ComponentCode, SourceRow, Name, Category, EffectiveDate, Eligibility, InputSource, Formula, Dependency, Unit, Currency, Proration, TaxTreatment, BPJSBasis, THRBasis, OTBasis, CashFlag, GL, PayslipOrder, Approval, WorkedExample, UAT ID, DecisionStatus.

**UAT:** upload valid 10 line dengan total cocok; duplicate file/reference ditolak atau di-skip sesuai kontrak; employer cost muncul pada laporan/jurnal tetapi tidak menambah cash THP; manual override tidak ditambah lagi oleh formula default.

**K:** eligibility dan tarif haid/kehadiran, transport motor, shift allowance, penanggung jawab shift, family/child, ASKOM, THR, bonus, Tax Natura, other bank, incentive tax/DTP, Bonus Direksi versus dividen. Kolom UPAH pada sumber tidak otomatis menjelaskan seluruh basis statutory atau accounting.

### 5.11 Payroll engine BPJS pajak dan valuta

**Dasar blueprint:** 2.2; 2.3; HG.PAY.05–06. **PIC:** Payroll Officer; pemilik aturan HR/Tax/Finance.

**Urutan konsep:** pilih effective contract/assignment → snapshot source → hitung fixed/prorata → attendance benefit/deduction → OT → variable/nonregular → employer/employee benefit → taxable base dan tax gross-up → deductions → THP → control total. Urutan final harus mengikuti dependency graph tiap formula, bukan urutan tampilan komponen.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-ENG-001 | B+D | Menghasilkan calculation line per employee/component/run beserta quantity, rate, basis, amount, rule version, rounding dan source reference |
| HG-ENG-002 | B+K | Prorata memakai eligibility date dan denominator yang disetujui per komponen; jangan otomatis memakai attendance untuk semua fixed salary |
| HG-ENG-003 | B+K | Potongan late dan unpaid absence mengikuti policy final, mencegah overlap pemotongan untuk waktu yang sama |
| HG-ENG-004 | B+D | BPJS dan ASKOM dipisah antara bagian employer/employee, wage basis, rate, ceiling/floor, active enrollment serta effective date |
| HG-ENG-005 | B | Pajak memilih TER/progresif/metode lain sesuai penerima dan masa pajak pada konfigurasi yang tervalidasi |
| HG-ENG-006 | B+D | Gross-up memakai metode yang teruji, precision/tolerance, max iteration serta exception jika tidak konvergen; simpan calculation trace |
| HG-ENG-007 | B+D | Annual/last-period tax memakai YTD finalized, opening balance migrasi, adjustment dan previous withholding sesuai policy, tanpa simulation |
| HG-ENG-008 | B+D | Komponen USD menyimpan original amount, rate type/date/source, IDR amount dan currency pembayaran; kurs efektif dibekukan pada hasil final |
| HG-ENG-009 | D | Hitung ulang draft mengganti hasil versi draft secara terkendali; input/version sama menghasilkan total sama; final lama tetap tersimpan |
| HG-ENG-010 | D | Missing policy, missing FX, formula cycle, invalid tax category, negative THP dan extreme variance menjadi exception dengan blocking severity |
| HG-ENG-011 | K | Expatriate classification SPDN/SPLN, pembayaran USD, natura dan kebutuhan PPh 26 diputuskan eksplisit; label expatriate saja tidak menentukan pajak |

**Contoh koreksi satuan untuk dibahas:** jika tarif hourly = Basic Salary /30 /8 dan durasi = late minutes, nilai monetary harus memakai durasi jam yaitu late minutes /60. Untuk basic salary Rp6.000.000 dan 30 menit, hasil sebelum policy toleransi adalah Rp12.500. Ini contoh usulan konsistensi satuan, bukan pengesahan formula potongan Hogy.

**THP concept:** cash earnings − cash deductions, setelah treatment pajak dan kontribusi ditentukan. Employer cost dan noncash taxable benefit memiliki flag tersendiri agar tidak dianggap uang transfer. Untuk USD gunakan rekonsiliasi per currency sebelum konversi control total.

**UAT:** karyawan penuh bulan; join/exit tengah bulan; salary change tengah bulan; THR/bonus bersama gaji; gross-up di batas TER; tax terakhir lebih potong; opening YTD; BPJS ceiling; USD rate kosong; employer cost; negative THP; formula loop; ulang calculate tanpa perubahan.

**K:** rate/basis BPJS termasuk klasifikasi JKK, ceiling JP per effective year, ASKOM basis, TER applicability, treatment natura/dividen, rounding setiap tahap, refund pajak, kurs dan tanggal acuan. Dokumen ini belum merupakan audit seluruh tarif hukum pada blueprint.

### 5.12 Payroll period approval finalisasi dan closing

**Dasar blueprint:** HG.PAY.01–12. **PIC:** Payroll Officer, HR Admin, HR Manager, Treasury, Accounting.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-PAY-001 | B | Periode menyimpan legal entity, payroll group, type, month, coverage dates, cut-off, payment date dan notes |
| HG-PAY-002 | B | Mendukung Regular, Gantungan/Adjustment, Termination dan Simulation |
| HG-PAY-003 | B+D | Employee generation memakai eligibility date, status, assignment, group dan statutory; daftar inclusion/exclusion beralasan dapat ditinjau |
| HG-PAY-004 | B+D | Attendance/leave/OT final dibekukan untuk run; engine mencatat sumber dan versi yang digunakan |
| HG-PAY-005 | B+D | Submit approval hanya saat calculation terkini dan blocking exceptions selesai; perubahan sumber/hasil setelah submit mengharuskan review/approval ulang |
| HG-PAY-006 | B | Finalisasi setelah approval menyimpan snapshot hasil dan mengunci source/result terkait |
| HG-PAY-007 | D | Status lifecycle terpisah dari payment state dan journal state; pembayaran parsial tidak dipaksakan menjadi satu Paid flag |
| HG-PAY-008 | B+D | Closing hanya jika pembayaran dan posting sesuai kondisi yang disepakati, rekonsiliasi lengkap dan tidak ada exception yang belum diterima berwenang |
| HG-PAY-009 | D | Menolak calculate/finalize bersamaan pada run yang sama; mencatat batch job, lock, completion/error dan opsi retry yang tidak menggandakan hasil |
| HG-PAY-010 | B+D | Reopen dibatasi kewenangan dan kondisi; paid/posted run tidak ditimpa atau dihapus. Koreksi finansial melalui adjustment/reversal terhubung |

**State machine usulan:** Draft → Prepared → Calculated → Under Review → Submitted → Approved → Finalized → Closed. Rejected/Returned kembali ke review; perubahan calculation setelah approved mencabut readiness finalization. Payment: Not Generated/Prepared/Submitted/Partial/Completed/Failed. Journal: Not Generated/Draft/Validated/Posted/Reversed.

**Data:** PayrollPeriod, PayrollRun, RunEmployee, SourceSnapshot, CalculationVersion, ApprovalHistory, PaymentBatch, JournalLink, ClosureChecklist. Cut-off attendance dan payroll coverage boleh berbeda; keduanya harus disimpan eksplisit.

**UAT:** dua user calculate bersamaan; run gagal sebagian lalu retry; approval draft usang; finalisasi tanpa approval; simulation menghasilkan preview tetapi tidak dapat bayar/posting; closing ketika transfer gagal; perubahan master setelah final tidak mengubah payslip final.

### 5.13 Adjustment retroactive dan simulation

**Dasar blueprint:** daftar komponen, deliverable, HG.PAY.01/04–06/08. **Tujuan:** menyelesaikan koreksi tanpa kehilangan histori atau akumulasi ganda.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-ADJ-001 | B+D | Adjustment mereferensikan employee, periode sumber, komponen, alasan, approved reference dan settlement period |
| HG-ADJ-002 | D | Simpan original amount, recalculated amount dan delta; delta yang telah diselesaikan tidak diselesaikan lagi |
| HG-ADJ-003 | K | Gantungan dibedakan antara pembayaran tertunda, koreksi nilai dan retroactive recalculation; tiap tipe memiliki treatment tax/accounting |
| HG-ADJ-004 | D | Simulation membaca snapshot/setup terpilih dan menghasilkan preview terisolasi, tanpa update salary assignment, YTD, leave ledger, bank atau GL |
| HG-ADJ-005 | D | Koreksi masa pajak dan pembayaran lintas bulan/tahun menghasilkan exception untuk review Tax sesuai treatment yang disetujui |

**UAT:** salary retro dua bulan menghasilkan delta saja; dua adjustment terhadap source sama memiliki settlement history; simulation tidak mengubah register final; cuti menyusul setelah paid regular mengoreksi deduction melalui run terkait.

### 5.14 Transfer Mandiri dan rekonsiliasi pembayaran

**Dasar blueprint:** 3.1.7; Summary and List Bank Transfer; HG.PAY.09–10. **PIC:** Payroll Officer untuk output; Treasury untuk bank.

**Alur:** final payroll → build payment batch → validasi rekening/control total → generate file sesuai format Mandiri yang disetujui → Treasury upload/authorize eksternal → catat hasil → reconcile success/failed → retry hanya saldo yang belum dibayar.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-BNK-001 | B | File/list transfer berasal dari payroll finalized; menyimpan run/version dan rekening yang digunakan pada snapshot |
| HG-BNK-002 | D | Interface contract menentukan channel/product Mandiri, encoding, delimiter/width, header/trailer, debit account, currency, value date dan control total |
| HG-BNK-003 | D | Simpan payment reference per beneficiary, generated version, amount, status, timestamp dan bank result reference |
| HG-BNK-004 | D | Regenerate file tidak dianggap transaksi baru; cegah resubmission penerima yang sudah sukses dibayar |
| HG-BNK-005 | B+D | Summary/list transfer dapat direkonsiliasi terhadap employee THP dan pembayaran agregat bila disetujui |
| HG-BNK-006 | K | Sample summary mencakup claim, serikat dan koperasi; konfirmasi apakah transfer agregat ini output D365 atau hanya lampiran kontrol eksternal |

**UAT:** rekening berawalan nol; bank lain; rekening invalid; success sebagian; retry satu employee; file regenerate; source payroll version berubah; sum detail = batch total. File upload tidak sama dengan pembayaran sukses.

**K:** exact template bank, IDR/USD, fee other bank, claim tambahan, beneficiary koperasi/serikat, upload result manual atau file import; direct API banking tidak terdefinisi pada baseline.

### 5.15 Posting jurnal payroll

**Dasar blueprint:** HG.PAY.11–12; Payroll Payment and Finance Integration. **PIC:** Finance/Accounting.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-GL-001 | B | Generate jurnal dari hasil final berdasarkan komponen, account mapping, dimension dan legal entity |
| HG-GL-002 | D | Mapping effective-dated mencakup earning, deduction, employer expense, payable dan clearing; dimensi memakai assignment periode sumber |
| HG-GL-003 | D | Validasi akun aktif, kombinasi dimensi, posting date, open ledger period, currency dan debit-credit balance sebelum posting |
| HG-GL-004 | B+D | Simpan journal/voucher reference per run/version dan cegah duplicate generation/posting |
| HG-GL-005 | D | Reversal/adjustment mempunyai link ke voucher asal; hasil payroll posted tidak ditimpa |
| HG-GL-006 | K | Konfirmasi detail per employee atau agregasi per component/dimension, confidentiality description serta mekanisme payment clearing |

**UAT:** mutasi tengah periode dengan aturan cost allocation; akun belum dipetakan; periode GL closed; debit-credit tidak seimbang; klik generate dua kali; posting sukses lalu correction; company isolation.

### 5.16 Laporan dokumen dan statutory export

**Dasar blueprint:** 3.1; 3.2; HG.PAY.09; HG.TER.09. **PIC:** Payroll, HR, Tax, Finance sesuai output.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-RPT-001 | B+D | Setiap report memiliki katalog dataset, grain, parameter, grouping, sort, kolom, formula total, currency, output format dan access role |
| HG-RPT-002 | B+D | Report payroll final membaca snapshot final. Preview draft memiliki penanda dan tidak digunakan untuk payment/statutory final |
| HG-RPT-003 | B | Slip mendukung employee info, earning/deduction, attendance, sisa annual leave dan variasi local/expatriate/koperasi/serikat |
| HG-RPT-004 | B+D | Email slip berpassword mengikuti kanal yang disepakati; recipient mapping, attachment per employee dan distribution log mencegah salah kirim |
| HG-RPT-005 | B+D | Employee hanya memperoleh dokumen miliknya; HR/payroll memiliki akses berbasis tugas yang disetujui; export massal diaudit |
| HG-RPT-006 | B | Mendukung paklaring, dokumen mutasi, kontrak, laporan absensi, korporat, payroll kategori, BPJS dan pajak pada baseline |
| HG-RPT-007 | B+D | Coretax exporter memisahkan BPMP, BPA1/A1 dan BP21 berdasarkan mapping jenis transaksi; memilih schema/version yang disetujui |
| HG-RPT-008 | D | XML divalidasi required field, enumerations, number/date format, legal entity TIN/NITKU, tax period, nil rules dan control total sebelum export |
| HG-RPT-009 | D | Sampel identitas dan nominal tidak di-hardcode; DTP, Resident, GrossUpOpt, NumberOfMonths dan tax object berasal dari keputusan/mapping tervalidasi |
| HG-RPT-010 | D | Simpan export batch, schema version, payroll result version, file hash dan upload outcome bila direkam; file generated belum berarti bupot resmi terbit |
| HG-RPT-011 | K | Konfirmasi printout 1721-A1 versus BPA1 dan proses mengambil bukti potong resmi dari Coretax; PPh26/SPLN adalah kebutuhan yang harus diputuskan |

**Katalog output awal:**

| ID output | Output | Grain dan sumber konsep | Requirement detail yang belum final |
|---|---|---|---|
| OUT-01 | Working Schedule | Employee × work date; effective schedule | Day type, override origin, break dan total hours |
| OUT-02 | Laporan Absensi Karyawan | Employee × work date; reconciled attendance | Planned/actual, fingerprint, late/early, OT, status dan remarks |
| OUT-03 | Rekap Absensi Karyawan | Employee × selected period; attendance/leave/OT | Definisi setiap status contoh dan unit day/hour/minute; status mutually exclusive atau bisa overlap |
| OUT-04 | Corporate Actual Hours | Section × period; source frozen | Definisi MP, actual hours, absence, index OT dan denominator |
| OUT-05 | Rekap Allowance dan Deduction | Section atau employee × component × period | Kategori, subtotal, currency dan employer cost inclusion |
| OUT-06 | Uang Pisah dan Kompensasi | Employee × settlement | Reason, service dates, component dan tax classification |
| OUT-07 | Rekap Gaji berdasarkan Kategori | Employee × category × period | Normalisasi seluruh kolom screenshot dan total formula |
| OUT-08 | eSPT atau 1721-I Excel | Employee × tax period/year | Apakah compatibility report atau proses pelaporan aktif; format final |
| OUT-09 | BPJS TK Active dan Employee Out | Member × contribution period | NIK, KPJ, wage/rapel, enrollment/end dates dan reason; layout SIPP |
| OUT-10 | PPh21 Bulanan Tahunan Kompensasi | Taxpayer × tax period/object | YTD, object, PTKP, gross/tax, fasilitas, withholding reference |
| OUT-11 | Bank Detail Summary dan List | Beneficiary × payment batch | Beneficiary agregat koperasi/serikat/claim dan template Mandiri |
| OUT-12 | Payslip | Employee × finalized run | Local/expat, zero suppression, USD display, annual leave as-of date, password |
| OUT-13 | Paklaring | Employee × termination case | Last position, service date, signature, numbering dan language |
| OUT-14 | Mutation Document | Mutation request | Before/after snapshot, approvals, effective date |
| OUT-15 | Contract Document | Contract version | Layout, signature dan numbering |
| OUT-16 | BPMP XML | Taxpayer × withholding month | Schema, object, DTP eligibility, field mapping |
| OUT-17 | BPA1 XML dan annual print | Taxpayer × last tax period/year | Annual/partial year logic, prior withholding, official issuance |
| OUT-18 | BP21 XML | Transaction × object/withholding date | Final/nonfinal object classification dan recipient treatment |

**UAT:** totals report match run; export filter company tidak bocor; annual report tidak menggandakan adjustment; payslip A tidak terkirim ke B; zero component hidden tanpa mengubah total; special character escape XML; missing TIN; NumberOfMonths disesuaikan rules; rejected upload dicatat dan diperbaiki pada source/mapping; template XML lolos uji upload pada proses yang diotorisasi.

### 5.17 Workflow notifikasi keamanan dan audit

**Dasar blueprint:** Workflow and Notification; HG.MUT; HG.PAY. **PIC:** HR Manager, system administrator dan process owners.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-SEC-001 | B+D | Scope akses legal entity, department bila relevan, employee dan payroll group; kontrol data berlaku di form, export, report serta interface |
| HG-SEC-002 | D | Pisahkan data preparation, payroll approval, payment authorization, GL posting dan system administration sesuai matriks kewenangan |
| HG-SEC-003 | B | Workflow dalam D365 untuk mutasi dan payroll sesuai baseline; approval cuti/lembur eksternal dicatat sebagai evidence |
| HG-SEC-004 | B+D | Contract expiry, pending mutation, payroll exception dan approval notification menggunakan configurable recipients serta event reference |
| HG-SEC-005 | D | Audit merekam actor, time, old/new, reason, company, record/run reference dan approval; notifikasi tidak memuat nominal sensitif tanpa kebutuhan |
| HG-SEC-006 | D | Attachment password/slip tidak ditulis pada log umum; recipient error mempunyai retry terkendali dan tidak mengirim batch ke penerima lain |
| HG-SEC-007 | K | Delegation, approval threshold, pengganti approver, salary visibility per grade, retention dan kanal notifikasi perlu disetujui |

**UAT:** manager hanya melihat scope yang sah; employee tidak bisa membuka payslip orang lain lewat link; user tanpa role tidak dapat export salary; approve oleh pembuat sendiri mengikuti policy; retry notifikasi tidak menggandakan event bisnis.

### 5.18 Migrasi dan kesiapan operasional

**Dasar blueprint:** Project Scope Data/User Adoption; dokumentasi implementasi. **PIC:** HR/Payroll/IT, consultant, Finance.

| Requirement | Jenis | Spesifikasi konsep |
|---|---|---|
| HG-MIG-001 | B+D | Migrasi master organisasi, employee/family/identifier, employment/contract, compensation, statutory, bank, schedule dan opening balances sesuai scope |
| HG-MIG-002 | D | Go-live tengah tahun memuat opening payroll/tax YTD per employee/component/masa, kontribusi, withholding references dan saldo leave |
| HG-MIG-003 | D | Menentukan apakah histori transaksi dimigrasi lengkap atau opening saja; raw sumber dipertahankan dan mapping legacy ID tersedia |
| HG-MIG-004 | D | Dry run dan final load memiliki count/control total reconciliation, error resolution, approved cut-off dan sign-off owner |
| HG-OPS-001 | D | Batch processing, logging, retry, monitoring dan retention mendukung volume aktual; benchmark tidak memakai batas jumlah employee fungsional |
| HG-OPS-002 | K | SLA import, calculation, report, concurrent users, jumlah employee/line, deployment window dan support period ditetapkan sebelum acceptance |
| HG-OPS-003 | D | Sebelum load final atau perubahan destruktif, siapkan backup/recovery yang sesuai environment dan prosedur rollback yang teruji |

**Load order:** master/policy → employee/alias/family → employment/contract/assignment → statutory/bank → schedule → opening leave → YTD payroll/tax → transaksi sumber yang disepakati → control totals. Data reconciliation harus selesai sebelum payroll pertama difinalisasi.

**UAT:** one employee with two historical NPK maps to one identity; YTD sebelum go-live + run pertama sesuai control total lama; load ulang tidak menggandakan saldo; restore/dry run sesuai prosedur pada staging.

## 6 Model data logis dan ownership

| Entitas konsep | Key dan relasi | Pemilik | Prinsip |
|---|---|---|---|
| Worker | Stable WorkerKey | HR | Tidak berubah saat status/NPK berubah |
| Employment | WorkerKey + legal entity + employment interval | HR | Mendukung eligibility date dan rehire policy |
| IdentifierHistory | WorkerKey + identifier type/value + interval | HR/IT | NPK/attendance alias tidak menjadi foreign key histori payroll |
| FamilyMember | WorkerKey + relation ID | HR | Benefit/tax dependent flags dipisah |
| Contract | EmploymentKey + contract version | HR | Effective date; tidak overwrite |
| CompensationAssignment | Contract/EmploymentKey + component + interval | HR/Payroll | Eligibility, amount/formula, currency |
| MutationRequest | RequestID + WorkerKey | HR | Before/after, approval, effective execution |
| EffectiveSchedule | EmploymentKey + work date + version | HR | Default + override + day classification |
| RawPunch | ImportBatchID + row/event identity | Attendance/IT | Raw immutable, alias resolve as-of event |
| Attendance | EmploymentKey + work date + calculation version | HR | Derivation/correction provenance |
| LeaveLedger | EmploymentKey + policy + transaction reference | HR | Opening, earn, usage, expiry, reversal |
| OvertimeRealization | SPL line + schedule/punch reference | HR | Planned/actual/payable terpisah |
| PayrollInput | RunID + WorkerKey + component + source reference | Payroll | Idempotent import dan approval evidence |
| PayrollResult | RunID + employee + component + calculation version | Payroll | Snapshot basis, rule, quantity, amount |
| TaxAccumulation | Taxpayer/employment scope + year + object | Tax/Payroll | Finalized results, YTD opening, no simulation |
| PaymentBatch | Run/version + beneficiary + payment reference | Treasury | Success/failed/retry history |
| JournalLink | Run/version + journal/voucher | Accounting | Balanced mapping dan anti duplicate |
| ExportBatch | Output/schema + run/version + file hash | Tax/Payroll | Traceable statutory/bank output |

Perhitungan harus membaca data pada tanggal efektif yang relevan dan menyimpan version/reference yang digunakan. Perubahan master hari ini tidak boleh mengubah laporan gaji final bulan lalu. Worker dapat lintas legal entity; payroll, akses, banking, statutory dan accounting harus tetap memiliki scope perusahaan eksplisit.

## 7 Keputusan yang harus ditutup sebelum development terkait

| ID keputusan | Pertanyaan konkret | Pemilik | Menghambat |
|---|---|---|---|
| DEC-01 | Bagaimana format NPK, alias historis dan attendance ID; apa yang terjadi saat permanent atau rehire? | HR/IT | EMP/CON/ATT/MIG |
| DEC-02 | Tanggal masa kerja apa yang dipakai untuk upah, THR, leave, pensiun dan paklaring? | HR | MST/ENG/LEV/TER |
| DEC-03 | Bagaimana mapping site–department–section–position–grade–cost center, termasuk Level A/B/C upah? | HR/Finance | MST/CON/GL |
| DEC-04 | Apakah middle-month salary/mutation dibagi per hari; denominator apa per komponen? | HR/Payroll | CON/MUT/ENG |
| DEC-05 | Apa formula final semua komponen dan sumber nilainya; mana employer/noncash/cash? | HR/Tax/Finance | CMP/ENG/RPT |
| DEC-06 | Bagaimana offset field, encoding, timezone, pairing window dan duplikasi fingerprint? | IT/HR | ATT |
| DEC-07 | Apakah 2 menit pertama bebas atau seluruh late dihitung setelah melewati toleransi? Bagaimana early leave dan rounding? | HR | ATT/ENG |
| DEC-08 | Berapa break duration dan paid/unpaid untuk setiap shift? Bagaimana overnight work date? | HR/Operations | WS/ATT/OT |
| DEC-09 | Siapa eligible cash OT per day type; apa seluruh multiplier dan payable duration rule? | HR | OT/ENG |
| DEC-10 | Bagaimana accrual/prorata/expiry/carry forward/tenure/half day/cuti ganti hari/cuti bersama? | HR | LEV |
| DEC-11 | Apakah Bonus Direksi adalah bonus kerja, tantiem atau dividen, dan apakah dua baris sumber duplikat? | Finance/Tax | CMP/ENG/Coretax |
| DEC-12 | Apa scope expatriate SPDN/SPLN, USD payment, natura dan PPh26? | HR/Tax/Finance | ENG/RPT |
| DEC-13 | Apa treatment DTP/incentive tax dan rapel; kapan berlaku dan siapa eligible? | Tax | ENG/Coretax |
| DEC-14 | Apa BPJS wage basis/rate/ceiling termasuk JKK/JP dan ASKOM; tanggal effective perubahan? | HR/Payroll | ENG |
| DEC-15 | Apa schema Coretax/type/object/mapping final; apakah output aplikasi draft atau bupot resmi diambil dari Coretax? | Tax | RPT |
| DEC-16 | Apa kanal slip, password policy dan akses HR versus employee; ada portal dalam scope? | HR/IT | RPT/SEC |
| DEC-17 | Apa perbedaan adjustment/gantungan/retro; bagaimana overlap regular/termination dan YTD tax? | Payroll/Tax/Finance | PAY/ADJ/TER |
| DEC-18 | Apa format Mandiri dan transfer agregat koperasi/serikat/claim; bagaimana recording partial result? | Treasury | BNK |
| DEC-19 | Apa GL mapping, dimensions, posting date, aggregation dan payment clearing? | Accounting | GL |
| DEC-20 | Bagaimana reopen setelah paid/posted, approval ulang, correction dan reversal? | HR/Finance | PAY/ADJ/GL |
| DEC-21 | Field laporan mana wajib dan definisi total/status/OT index/MP apa yang dipakai? | Report owners | RPT |
| DEC-22 | Go-live date, migration depth/YTD, volume benchmark, SLA dan support apa yang disepakati? | PM/HR/IT | MIG/OPS |

Gunakan log keputusan dengan kolom ID, pertanyaan, opsi, keputusan final, owner, tanggal, evidence, impacted requirements, dan sign-off. Status K tidak boleh diubah menjadi B hanya karena teknikal memilih default implementasi.

## 8 Template satu proses untuk BRD dan FSD

### BRD process sheet

- Process ID dan nama proses.
- Business objective dan masalah existing.
- Pemilik proses dan aktor.
- Trigger, input, prasyarat, output dan postcondition.
- Alur existing dan alur proposed; tandai manual/external/D365.
- In scope, out of scope dan dependensi.
- Business rule bernomor, tanggal berlaku dan pemilik kebijakan.
- Requirement ID, prioritas, sumber blueprint, acceptance criteria.
- Asumsi, exception, keputusan terbuka dan approval.

### FSD feature sheet

- FSD ID, version, source BRD dan linked requirement IDs.
- Fit-gap outcome: standard/extension/custom; bukti environment/modul yang diverifikasi.
- Menu/form/workspace dan role pengguna.
- Header/line/group field dengan type, mandatory condition, default, editable state, lookup dan validation.
- Status transition, action/button, precondition, postcondition, role, error message dan rollback behaviour.
- Data model logis, company scope, effective dating dan unique/reference keys.
- Formula/dependency/precision/rounding/unit plus contoh perhitungan yang disetujui.
- Interface/file schema/mapping/version, idempotency, control total, retry dan failure behaviour.
- Workflow, delegation, notifications dan approval invalidation.
- Snapshot/audit/source provenance dan perubahan setelah finalisasi.
- Report/output mapping, filters, access dan sample yang disetujui.
- Migration/opening data dan batch/performance expectations.
- UAT case dengan input, langkah, expected output, reconciliation dan evidence.
- Daftar keputusan terbuka serta readiness gate sebelum development.

### Contoh acceptance criterion yang lengkap

Requirement HG-EMP-002: ketika HR mengaktifkan kontrak Permanent yang sah pada tanggal efektif, sistem menggunakan WorkerKey yang sama dan NPK sesuai aturan employment type. Transaksi fingerprint sebelum tanggal efektif tetap ditelusuri melalui alias lama, transaksi baru melalui alias yang berlaku, dan YTD pajak tidak terpecah menjadi dua karyawan. Payroll final periode sebelumnya tetap menampilkan identitas pada snapshot periode tersebut.

Requirement HG-ATT-006: dengan effective schedule masuk 07.00 dan toleransi 2 menit, punch 07.02 dan 07.03 harus menghasilkan status/durasi sesuai keputusan DEC-07. Expected monetary deduction baru diisi setelah formula, rounding dan treatment grace period ditandatangani. Jangan membuat expected amount sebelum keputusan tersebut selesai.

Requirement HG-PAY-006: setelah HR Manager menyetujui calculation version V3 dan Payroll Officer melakukan finalize, V3 serta sumbernya terkunci. Perubahan contract rate sesudahnya tidak mengubah V3; export bank dan payslip menyimpan referensi V3. Jika sumber berubah sebelum finalize, approval terhadap versi usang tidak dapat dipakai.

## 9 Traceability dan pembagian pekerjaan teknikal

Gunakan satu register requirement sebagai sumber bersama: RequirementID → BlueprintReference → BusinessRuleID → DecisionID → FSDSection → TechnicalObject → UATCase → Status. Prioritas awal P0 untuk integrity payroll/payment/tax dan akses; P1 untuk proses utama serta output mandatory; P2 untuk kemudahan operasional. Prioritas tiap fitur disetujui PM dan process owner, bukan ditentukan dari urutan halaman blueprint.

**Contoh mapping:**

| Requirement | Sumber | FSD | Decision | UAT konsep |
|---|---|---|---|---|
| HG-EMP-002 | HG.EMP.02/HG.CON.02 | FSD-01/02 | DEC-01 | NPK berubah, worker dan YTD tetap |
| HG-ATT-003 | HG.ATT.07 | FSD-04 | DEC-06 | File identik tidak menggandakan punch |
| HG-LEV-004 | 2.12/HG.LEV.01 | FSD-05 | DEC-10 | Annual 0,5 memotong tepat 0,5 |
| HG-OT-004 | 2.13/HG.PAY.05 | FSD-06/07 | DEC-09 | Workday/holiday tier dan wage basis |
| HG-ENG-006 | 2.3/HG.PAY.05 | FSD-07 | DEC-05/13 | Gross-up konvergen di rate boundary |
| HG-PAY-010 | HG.PAY.08/12 | FSD-08 | DEC-20 | Paid/posted correction tanpa overwrite |
| HG-BNK-004 | HG.PAY.09/10 | FSD-10 | DEC-18 | Retry hanya failed beneficiary |
| HG-RPT-007 | 3.1.6 | FSD-11 | DEC-15 | XML sesuai jenis transaksi dan schema |

**Urutan implementasi yang disarankan:**

1. Tutup identity/organization/service date dan buat skeleton akses, master serta kontrak.
2. Lengkapi file contract, shift/break dan attendance reconciliation.
3. Tetapkan leave ledger serta OT eligibility/realization.
4. Selesaikan formula catalog dan statutory/FX mapping; bangun engine serta trace.
5. Tambahkan workbench, approval, snapshot, adjustment dan termination.
6. Integrasikan Mandiri, GL, laporan dan statutory output.
7. Jalankan migration dry run, parallel payroll reconciliation dan end-to-end UAT sampai closing.

Aktivitas dapat berjalan bersamaan bila dependensi sudah stabil. Paket formula, schema, dan mapping yang belum disetujui tidak boleh dianggap selesai hanya karena UI sudah tersedia.

## 10 Contoh skenario integrasi untuk handover

| Skenario | Setup dan input | Expected result |
|---|---|---|
| E2E-01 Local regular | Karyawan permanent, schedule normal, attendance complete, komponen valid | Satu hasil final; report/payslip/bank/GL control total sesuai mapping |
| E2E-02 Change status | Contract → permanent dengan NPK baru pada tengah tahun | Satu worker; histori alias benar; YTD berlanjut; benefit efektif sesuai policy |
| E2E-03 Promotion | Approved mutation efektif tanggal 15 dan kontrak/amendment baru | Tidak ada data setengah terproses; pay split/eligibility sesuai keputusan |
| E2E-04 Overnight | Shift 23.00–07.00, punch lintas tanggal dan dua mesin | Pairing benar, work date konsisten, actual dan OT tidak double count |
| E2E-05 Half day | Annual leave 0,5 ditambah attendance setengah hari | Saldo −0,5; status attendance dan deduction sesuai policy |
| E2E-06 Late tolerance | Punch 1, 2, 3 dan 30 menit setelah schedule | Boundary dan monetary unit sesuai policy final; tanpa potongan ganda |
| E2E-07 Expat USD | Employee resident, USD allowance, FX efektif dan natura | Currency asli/konversi tersimpan; tax dan cash THP terpisah sesuai mapping |
| E2E-08 Termination | Regular coverage telah dibayar; special settlement eksternal disetujui | Settlement tidak menggandakan hak; final tax memakai YTD valid |
| E2E-09 Backdated correction | Cuti menyusul/rapel setelah run paid dan GL posted | Delta melalui adjustment terhubung; final/voucher lama utuh |
| E2E-10 Partial bank failure | Sebagian transfer sukses, sebagian gagal | Status per beneficiary, retry tidak membayar yang sudah sukses; closing terkendali |
| E2E-11 Migration midyear | Opening YTD dan saldo leave telah direkonsiliasi | Annual tax dan saldo berjalan cocok dengan control total baseline |
| E2E-12 Security | HR department A, employee B, payroll approver, Treasury | Akses sesuai scope di form/link/report/export; audit terbentuk |

Expected amounts tiap kasus diisi menggunakan worked example yang disetujui business owner. Parallel payroll harus menjelaskan setiap variance antara sistem lama dan baru: policy correction, source discrepancy, rounding, mapping atau defect; target acceptance tidak cukup hanya total agregat sama.

## 11 Referensi eksternal untuk titik verifikasi

Referensi berikut dipakai untuk menentukan area verifikasi, bukan untuk mengesahkan semua tarif atau menghitung kewajiban pajak pada dokumen ini.

- DJP menyediakan template XML/converter terpisah untuk bukti potong. FSD exporter perlu memakai jenis dan versi yang dipilih serta mapping final: https://www.pajak.go.id/en/node/112031
- Penerbitan BPA1/A2 melalui Coretax dan dokumen yang dihasilkan aplikasi lain perlu dibedakan pada definisi output resmi: https://pajak.go.id/id/pengumuman/imbauan-penerbitan-bukti-potong-pajak-penghasilan-dalam-rangka-pelaporan-spt-tahunan
- Validasi kebijakan maternity terhadap UU 4 Tahun 2024 serta ketentuan yang relevan; jangan membatasi engine pada draft tiga bulan tanpa review HR: https://peraturan.go.id/id/uu-no-4-tahun-2024

## 12 Kriteria siap diberikan untuk development

Satu paket FSD siap dikembangkan jika source requirement dapat ditelusuri, field/form dan workflow lengkap, formula memiliki unit dan contoh hasil, mapping interface/output tersedia, keamanan dan company scope disetujui, exception/rollback/retry jelas, dan keputusan yang memblokir paket telah ditutup. Tim teknikal kemudian melengkapi objek aktual D365FO serta estimasi pekerjaan; BRD/FSD tidak menetapkan objek standard yang belum diverifikasi.

Dokumen sumber tetap dipertahankan. Konsep ini menjadi pendamping baseline, dan usulan D atau perubahan scope harus melalui review serta mekanisme persetujuan proyek yang berlaku.
