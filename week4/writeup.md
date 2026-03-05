# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Sheila Sabina** \
SUNet ID: **2310817220028** \
Citations: **N/A**

This assignment took me about **4** hours to do. 


## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Terinspirasi dari dokumentasi Best Practices Anthropic untuk memberikan panduan konteks proyek agar AI tidak salah memberikan perintah terminal.

b. Design of each automation, including goals, inputs/outputs, steps
> Goal: Memberikan panduan konteks proyek (Windows, PowerShell, dan struktur folder).
Inputs/Outputs: File ini dibaca oleh AI saat sesi dimulai untuk memandu navigasi kode.
Steps: Mendefinisikan perintah make run dan lokasi router.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> File ini bersifat pasif. AI (Claude atau Copilot) membacanya sebagai referensi konteks saat bekerja di dalam repositori ini.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> Before: AI sering memberikan saran perintah Linux yang error di terminal Windows saya.
After: AI memberikan saran yang tepat sesuai perintah make yang tersedia di repositori.

e. How you used the automation to enhance the starter application
> Saya merujuk pada panduan di CLAUDE.md saat meminta Copilot untuk menambahkan fitur Delete Note. Hal ini memastikan Copilot menempatkan kode di router yang benar dan mengikuti gaya penulisan yang sudah ditetapkan.


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Terinspirasi dari fitur Custom Slash Commands untuk otomatisasi tugas verifikasi data yang berulang.

b. Design of each automation, including goals, inputs/outputs, steps
> Goal: Verifikasi instan data di tabel notes dan action_items tanpa query manual.
Inputs: Perintah /db-check pada terminal.
Outputs: Ringkasan baris data terbaru dari database.
Steps: Agen menjalankan query SELECT pada data/app.db menggunakan sqlite3 dan menampilkan hasilnya.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> Karena kendala akses pada Claude Code CLI, perintah ini dijalankan secara manual di terminal menggunakan: sqlite3 data/app.db "SELECT * FROM notes;".

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> Manual: Harus mengingat letak file .db dan query SQL yang benar setiap kali ingin verifikasi.
Automated: Instruksi sudah tersimpan rapi di .claude/commands/db-check.md sebagai dokumentasi perintah siap pakai.

e. How you used the automation to enhance the starter application
> Perintah ini saya gunakan untuk memastikan bahwa data benar-benar terhapus dari database setelah saya menekan tombol "Delete" pada UI yang baru saya buat.