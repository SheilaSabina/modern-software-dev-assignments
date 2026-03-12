# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Sheila Sabina** \
SUNet ID: **2310817220028** \
Citations: **Semgrep Documentation, FastAPI Security Best Practices.**

This assignment took me about **5** hours to do. 


## Brief findings overview 
> Saya memperbaiki 6 temuan keamanan kritis yang dideteksi Semgrep, termasuk SQL Injection, XSS, dan kebijakan CORS yang tidak aman, hingga mencapai 0 temuan (clean scan).

## Fix #1
a. File and line(s)
> `backend/app/routers/notes.py` (Baris 71‑79)

b. Rule/category Semgrep flagged
> `python.sqlalchemy.security.sqlalchemy-execute-f-string`

c. Brief risk description
> Penggunaan f-string dalam kueri SQL memungkinkan penyerang menyuntikkan perintah database berbahaya.

d. Your change (short code diff or explanation, AI coding tool usage)
> Mengganti f-string dengan bind parameters (parameterized queries) menggunakan kamus data `:val`.
> ```python
> # sebelum
> db.execute(f"SELECT * FROM notes WHERE title LIKE '%{q}%'")
> # sesudah
> stmt = select(Note).where(Note.title.contains(q))
> rows = db.execute(stmt).scalars().all()
> ```
> (atau setara, saya menggunakan ORM select sehingga input tidak disisipkan langsung)

e. Why this mitigates the issue
> Memisahkan kode SQL dari data pengguna sehingga input tidak dieksekusi sebagai perintah, menutup celah injeksi.

## Fix #2
a. File and line(s)
> `frontend/app.js` (Baris 14)

b. Rule/category Semgrep flagged
> `javascript.browser.security.insecure-dom-api.innerHTML`

c. Brief risk description
> Penggunaan `.innerHTML` dapat mengeksekusi skrip berbahaya yang disisipkan penyerang ke dalam halaman web.

d. Your change (short code diff or explanation, AI coding tool usage)
> Mengganti penggunaan `.innerHTML` dengan `.textContent`.
> ```javascript
> // sebelum
> element.innerHTML = userInput;
> // sesudah
> element.textContent = userInput;
> ```

e. Why this mitigates the issue
> `.textContent` memperlakukan semua input sebagai teks biasa, bukan kode HTML/JS, sehingga mencegah eksekusi skrip.

## Fix #3
a. File and line(s)
> `backend/app/main.py` (Baris 24)

b. Rule/category Semgrep flagged
> `python.fastapi.security.cors-allow-origins-wildcard`

c. Brief risk description
> Penggunaan wildcard `["*"]` pada `allow_origins` memungkinkan situs web mana pun untuk mengakses data API kita secara lintas-asal.

d. Your change (short code diff or explanation, AI coding tool usage)
> Membatasi `allow_origins` hanya ke domain spesifik yang dipercaya (seperti `["http://localhost:8000"]`).
> ```python
> app.add_middleware(
>     CORSMiddleware,
>     allow_origins=["http://localhost:8000"],
>     allow_credentials=True,
>     allow_methods=["*"],
>     allow_headers=["*"],
> )
> ```

e. Why this mitigates the issue
> Membatasi akses API hanya untuk sumber yang sah, mengurangi risiko pencurian data melalui serangan lintas situs.