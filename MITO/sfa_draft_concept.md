# SFA Phase 2

_Deskripsi singkat tentang apa dokumen ini._

---

## Gambaran Umum

Tujuan

Kelanjutan dari platform Sales Force Phase 1  yang melayani kebutuhan tim internal dan partner eksternal. Partner dapat melakukan registrasi mandiri, mengelola profil, mendaftarkan IMEI, meminta penawaran, dan mengklaim reward, sementara seluruh proses tetap berada dalam kontrol approval perusahaan.

Target Pengguna
- Internal: Super Admin, Admin, Sales, Sales Manager, Marketing.
- Eksternal: Dealer Owner, Dealer Staff, Distributor, Retail Partner.

## Scope

- Penambahan External User (Dealer, toko, retailer, partner, end customer)
- Imei Registration
- Quotation Request
- Reward Claim
- Odoo Integration

## ROADMAP
| Phase       | Modul                                                                                | Prioritas |
| ----------- | ------------------------------------------------------------------------------------ | --------- |
| **Phase 1** | Registrasi External User, Login, Approval Admin, Role & Permission                   | ⭐⭐⭐⭐⭐     |
| **Phase 2** | Dealer Management, Profile, Dokumen Legal (KTP, NIB, NPWP, SIUP), Dashboard External | ⭐⭐⭐⭐⭐     |
| **Phase 3** | Odoo Integration, IMEI Registration, Validasi IMEI, Approval, Riwayat                                  | ⭐⭐⭐⭐⭐     |
| **Phase 4** | Quotation Request → Konversi menjadi Quotation oleh Sales, Workflow Approval         | ⭐⭐⭐⭐      |
| **Phase 5** | Reward Point, Reward Catalog, Reward Claim, Approval & Pengiriman                    | ⭐⭐⭐⭐      |
| **Phase 6** | Notifikasi (Email, WhatsApp, Push), Audit Log, API Publik, Mobile Ready              | ⭐⭐⭐       |



## CORE FEATURE
1. Self Registration & Approval
 - Registrasi online.
 - Upload dokumen pendukung.
 - Workflow approve/reject.
 - Aktivasi akun setelah disetujui.
2. Dealer Portal
 - Dashboard ringkasan aktivitas.
 - Kelola profil dan dokumen.
 - Riwayat transaksi dan notifikasi.
3. IMEI Registration
 - Input IMEI dan dokumen pembelian.
 - Validasi duplikasi.
 - Approval admin.
 - Integrasi dengan sistem poin.
4. Quotation Request
 - Pengajuan kebutuhan produk.
 - Konversi menjadi quotation oleh sales.
 - Pelacakan status.
5. Reward Management
 - Akumulasi poin.
 - Katalog hadiah.
 - Pengajuan klaim.
 - Approval dan penyelesaian klaim.
6. Workflow Pendukung
 - Approval generik lintas modul.
 - Notifikasi multi-channel.
 - Audit log.
 - API untuk aplikasi mobile.



## High Level Concept

```mermaid
flowchart TB

    APP[Sales Force Application]

    APP --> INTERNAL[Internal Portal]
    APP --> EXTERNAL[External Portal]

    INTERNAL --> SALES[Sales]
    INTERNAL --> MANAGER[Manager]
    INTERNAL --> ADMIN[Admin]
    INTERNAL --> MARKETING[Marketing]

    EXTERNAL --> DEALER[Dealer]
    EXTERNAL --> STORE[Retail Store]
    EXTERNAL --> DISTRIBUTOR[Distributor]
    EXTERNAL --> CUSTOMER[Customer]

    INTERNAL --> DB[(Database)]
    EXTERNAL --> DB
```

## User Registration Flow 

```mermaid
flowchart TD

A[Register]
-->B[Fill Form]
-->C[Upload Document]
-->D[Submit]

D-->E[Pending Approval]

E-->F{Admin Review}

F--Approve-->G[Account Active]

F--Reject-->H[Rejected]

H-->B
```


## IMEI REGIS
```mermaid
flowchart TD

A[Login]
-->B[Input IMEI]

B-->C[Upload Invoice]

C-->D[Submit]

D-->E[Validation]

E-->F{Valid?}

F--No-->G[Reject]

F--Yes-->H[Admin Approval]

H-->I{Approved?}

I--Yes-->J[Reward Point]

I--No-->K[Rejected]
```

## QUOTATION REQUEST
```mermaid
flowchart TD

A[Dealer]
-->B[Create Request]

B-->C[Sales Review]

C-->D[Create Quotation]

D-->E[Manager Approval]

E-->F{Approved?}

F--Yes-->G[Send Quotation]

F--No-->H[Rejected]
```

## REWARD CLAIM
```mermaid
flowchart TD

A[Reward Point]

-->B[Select Reward]

-->C[Submit Claim]

-->D[Admin Verification]

D-->E{Approved?}

E--Yes-->F[Reward Sent]

E--No-->G[Rejected]
```

## OVERALL PROCESS ***Tidak perlu
```mermaid
flowchart TD

A[Reward Point]

-->B[Select Reward]

-->C[Submit Claim]

-->D[Admin Verification]

D-->E{Approved?}

E--Yes-->F[Reward Sent]

E--No-->G[Rejected]
```


## SIMPLE ERD
```mermaid
erDiagram

    USERS {
        bigint id
        bigint dealer_id
        string name
        string email
        string status
    }

    DEALERS {
        bigint id
        string name
    }

    IMEI_REGISTRATIONS {
        bigint id
        bigint dealer_id
        bigint user_id
    }

    QUOTATION_REQUESTS {
        bigint id
        bigint dealer_id
        bigint user_id
    }

    REWARD_CLAIMS {
        bigint id
        bigint dealer_id
        bigint user_id
    }

    APPROVALS {
        bigint id
        string module
        bigint reference_id
    }

    USERS ||--o{ IMEI_REGISTRATIONS : creates
    USERS ||--o{ QUOTATION_REQUESTS : creates
    USERS ||--o{ REWARD_CLAIMS : creates

    DEALERS ||--o{ USERS : has

    APPROVALS ||--o{ IMEI_REGISTRATIONS : approves
    APPROVALS ||--o{ QUOTATION_REQUESTS : approves
    APPROVALS ||--o{ REWARD_CLAIMS : approves
```


 



_Terakhir diperbarui: YYYY-MM-DD_