# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Sheila Sabina** \
SUNet ID: **2310817220028** \
Citations: Warp AI (Oz Agent), dokumentasi FastAPI, dokumentasi SQLAlchemy

Pengerjaan tugas ini memakan waktu sekitar **4** jam.


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> Saya membuat workflow Warp Drive bernama **"Pre-commit-Check"** yang merangkai tiga target Make secara berurutan: `make format && make lint && make test`. Tujuannya adalah memastikan kualitas kode sebelum setiap commit. Input-nya adalah working tree saat ini; output-nya berupa status lolos (exit 0) atau gagal langsung disertai pesan error dari langkah yang bermasalah. Langkah-langkahnya: (1) `black` + `ruff --fix` melakukan auto-format pada seluruh kode, (2) `ruff check` memverifikasi tidak ada pelanggaran lint yang tersisa, dan (3) `pytest` menjalankan seluruh test suite untuk mendeteksi regresi.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Sebelum:** Saya harus mengingat dan menjalankan tiga perintah terpisah secara manual (`black .`, `ruff check . --fix`, `pytest backend/tests`) dan terkadang lupa salah satu, yang menyebabkan kegagalan CI setelah push. **Sesudah:** Satu kali invokasi workflow menjalankan ketiganya secara berurutan. Jika formatting mengubah file, linting menangkap apa pun yang tidak diperbaiki `black`, dan test memverifikasi tidak ada yang rusak — semua dalam satu langkah.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> Workflow ini berjalan dengan izin tulis pada direktori backend karena `make format` memodifikasi file secara langsung (Black dan Ruff auto-fix). Saya melakukan supervisi dengan meninjau diff setelah formatting (`git diff`) dan mengonfirmasi hasil test sebelum melakukan commit.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> Tidak berlaku untuk automasi ini — ini adalah pipeline sekuensial tunggal.

e. How you used the automation (what pain point it resolves or accelerates)
> Automasi ini menghilangkan masalah "lupa lint" atau "lupa jalankan test" sepenuhnya. Sebelum setiap commit, saya cukup menjalankan workflow Pre-commit-Check sekali dan mendapatkan hasil lolos/gagal yang definitif. Ini mengurangi rutinitas pre-commit saya dari ~2 menit perintah manual menjadi satu aksi sekali klik.



### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> Saya menggunakan dua tab Warp yang berjalan secara bersamaan, masing-masing dengan agen AI-nya sendiri. **Agen 1 (Tab Kiri — Infrastruktur)** bertanggung jawab atas Task #7: menambahkan validasi Pydantic `Field(min_length=1)` pada schema, mengimplementasikan global exception handler untuk `HTTPException` dan `RequestValidationError`, serta membangun middleware response envelope yang membungkus semua response API 2xx ke dalam format `{"ok": true, "data": ...}`. **Agen 2 (Tab Kanan — Pengembang Fitur)** bertanggung jawab atas Task #8: menambahkan parameter query `page` dan `page_size` pada `GET /notes/` dan `GET /action-items/`, mengembalikan payload `{"items": [...], "total": N}`, serta menulis test untuk batas paginasi. Kedua agen mengambil kode yang sudah ada sebagai input dan menghasilkan file Python yang telah diedit sebagai output.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Sebelum:** Response API berupa JSON mentah tanpa envelope yang konsisten — error mengembalikan format yang tidak seragam, dan endpoint daftar menampilkan semua record tanpa paginasi. Seorang developer harus mengimplementasikan middleware, exception handler, dan paginasi secara berurutan, yang memakan waktu. **Sesudah:** Setiap response API mengikuti envelope yang seragam (`ok` + `data` atau `ok` + `error`), validasi menolak string kosong, dan semua endpoint koleksi mendukung `page`/`page_size` dengan jumlah `total`. Seluruh 14 test berhasil lolos.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> Kedua agen diberikan izin tulis yang dibatasi pada direktori `backend/`. Agen 1 memodifikasi `main.py` dan `schemas.py`; Agen 2 memodifikasi `routers/notes.py` dan `routers/action_items.py`. Saya memilih izin tulis karena kedua tugas memerlukan pengeditan file dan pembaruan test secara langsung. Supervisi dilakukan dengan menjalankan `make test` setelah masing-masing agen menyelesaikan pekerjaannya — ini berfungsi sebagai gerbang integrasi untuk memastikan perubahan dari kedua agen berjalan dengan benar tanpa konflik.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> **Peran:** Agen 1 = Infrastruktur (middleware, error handling, validasi). Agen 2 = Pengembang Fitur (logika paginasi, perubahan router). **Strategi koordinasi:** Pemisahan di level file — Agen 1 mengelola `main.py` dan `schemas.py`, Agen 2 mengelola `routers/*.py`. Hal ini menghindari konflik merge. **Keuntungan konkurensi:** Kedua tugas diselesaikan secara paralel, sehingga waktu pengerjaan berkurang sekitar setengahnya dibandingkan implementasi sekuensial. **Risiko:** Middleware (Agen 1) membungkus response yang berisi payload paginasi (Agen 2), sehingga ketidakcocokan struktur response bisa menyebabkan kegagalan test. **Mitigasi:** Saya menjalankan seluruh test suite setelah kedua agen selesai untuk mendeteksi masalah integrasi. Middleware envelope berhasil membungkus payload paginasi `{"items": ..., "total": ...}` ke dalam `{"ok": true, "data": {"items": ..., "total": ...}}` dengan benar.

e. How you used the automation (what pain point it resolves or accelerates)
> Pendekatan multi-agen mengatasi masalah ketergantungan sekuensial — biasanya, error handling harus diselesaikan terlebih dahulu, baru kemudian membangun paginasi di atasnya. Dengan memisahkan tanggung jawab ke dua agen yang bekerja secara paralel, waktu implementasi berkurang secara signifikan. Insight utamanya adalah bahwa pekerjaan infrastruktur (middleware/validasi) dan pekerjaan fitur (paginasi) menyentuh file yang berbeda, sehingga pengembangan konkuren menjadi aman dan efisien.


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> Tidak ada.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> Tidak ada.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> Tidak ada.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> Tidak ada.

e. How you used the automation (what pain point it resolves or accelerates)
> Tidak ada.

