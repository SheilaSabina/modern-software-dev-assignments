# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Sheila Sabina** \
SUNet ID: **2310817220028** \
Citations: **GitHub documentation for FastAPI, SQLAlchemy, and ChatGPT/Copilot for debugging WinError 32.**

This assignment took me about **6** hours to do. 


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> https://github.com/mihail911/modern-software-dev-assignments/pull/21

b. PR Description
> Menambahkan endpoint DELETE dengan status code 204 No Content dan validasi min_length=3 pada skema Pydantic untuk title dan description. Memperbaiki conftest.py dengan menambahkan engine.dispose() dan blok try-except untuk menangani file lock SQLite di Windows (PermissionError: [WinError 32]).

c. Graphite Diamond generated code review
> Graphite Diamond tidak memberikan review otomatis karena kendala sinkronisasi tool eksternal pada repositori fork.

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> https://github.com/mihail911/modern-software-dev-assignments/pull/23#pullrequestreview-3938270436

b. PR Description
> Mengotomatisasi ekstraksi 'action items' dari konten catatan dengan memanggil fungsi extract_action_items() setelah catatan disimpan. Menambahkan logika pembersihan data action items lama pada fungsi patch_note untuk mencegah duplikasi di database, serta memastikan penyimpanan data dengan db.flush() dan db.commit().

c. Graphite Diamond generated code review
> Kendala teknis sinkronisasi tool eksternal pada fork repository, sehingga review otomatis tidak tersedia.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> https://github.com/mihail911/modern-software-dev-assignments/pull/26#pullrequestreview-3938396880

b. PR Description
> Membuat model ActionItem dengan hubungan ForeignKey ke tabel Notes untuk mendukung fitur ekstraksi otomatis action items. Model mencakup kolom id (primary key), description (Text, required), completed (Boolean, default False), dan note_id (Foreign Key). Pembaruan schemas.py menggunakan ConfigDict(from_attributes=True) yang kompatibel dengan Pydantic V2.

c. Graphite Diamond generated code review
> Tidak tersedia due to synchronization constraints.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> TODO (belum ada PR link khusus untuk Task 4)

b. PR Description
> Memperbaiki pengujian pada test_notes.py untuk memastikan parameter query q (search), limit (pagination), dan sort (sorting dengan prefix '-' untuk descending) mengembalikan data yang valid dan terurut sesuai ekspektasi.

c. Graphite Diamond generated code review
> TODO

## Brief Reflection 
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> Komentar manual saya fokus pada:
> - **Correctness**: Logika penghapusan duplikat action items sebelum ekstraksi ulang
> - **Security**: Validasi input pada skema Pydantic (min_length, nullable constraints)
> - **Performance**: Penggunaan db.flush() vs db.commit() untuk efisiensi database operations
> - **OS-specific bugs**: Detection masalah PermissionError di Windows pada file lock SQLite dan temporary files cleanup

b. A comparison of **your** comments vs. **Graphite's** AI-generated comments for each PR.
> Komentar manual saya lebih mendalam pada aspek lingkungan pengembangan khususnya masalah Windows-specific issues (PermissionError), sementara Graphite Diamond tidak memberikan input karena kendala teknis sinkronisasi pada fork repository. Jika Graphite berhasil tersinkronisasi, review AI diharapkan dapat menangkap aspek structural code patterns dan best practices general, namun tetap terbatas pada environment-specific issues.

c. When the AI reviews were better/worse than yours (cite specific examples)
> **AI (Copilot) lebih unggul pada:**
> - Penulisan boilerplate code dengan cepat (schema definitions, model classes)
> - Suggestion untuk refactoring ke background tasks (Task 3)
> - Implementation detail untuk exception handling patterns
>
> **Manual review lebih unggul pada:**
> - Detection masalah PermissionError [WinError 32] yang memerlukan pemahaman OS-level
> - Context-aware decision tentang db.flush() vs db.commit() berdasarkan transaction scope
> - Validation strategy decisions untuk API contracts
>
> **Contoh spesifik:** Copilot tidak mendeteksi bahwa temporary SQLite database file masih di-lock setelah test execution di Windows, sehingga os.unlink() akan fail. Manual intervention diperlukan untuk menambahkan try-except dan engine.dispose().

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> **Comfort level: Moderate-High untuk general code patterns, Moderate untuk database/OS-specific concerns**
>
> **Heuristics untuk mengandalkan AI reviews:**
> - ✅ **Andalkan AI untuk**: Boilerplate code, naming conventions, structural patterns, general best practices
> - ⚠️ **Review manual wajib untuk**: Database transaction logic, environment-specific bugs (Windows/Linux differences), security-sensitive operations, deployment/infrastructure code
> - ✅ **AI + Manual hybrid approach**: AI untuk code generation speed, manual untuk critical logic verification dan OS/environment considerations
>
> Kesimpulannya, AI sangat berguna untuk acceleration development cycle, namun expertise manual tetap diperlukan untuk aspek-aspek yang sensitive terhadap deployment environment dan sistem operasi.