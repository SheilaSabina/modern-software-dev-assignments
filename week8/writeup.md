# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Sheila Sabina** \
SUNet ID: **2310817220028** \
Citations: **Used Cursor (Composer + Agentic Mode) and built-in Gemini/Ollama assistants for code generation, refactoring, and debugging across all three app versions.**

This assignment took me about **8–10** hours to do. 


## App Concept 
```
Developer Control Center is a small productivity dashboard for developers to manage **Notes** and **Tasks** in one place.
The app lets me quickly jot down meeting notes, decisions, or ideas, and then track concrete tasks derived from those notes.
Across all three versions (Next.js, Django, Flask), the core flows are the same: create notes, create tasks, and see them together in a clean, dark‑mode UI.
```


## Version #1 Description
```
APP DETAILS:
===============
Folder name: week8/bolt-app
AI app generation platform: Cursor Composer (Next.js template / bolt‑style generation)
Tech Stack: Next.js + TypeScript + Tailwind CSS (dark mode)
Persistence: In‑memory / client-side state (no database)
Frameworks/Libraries Used: Next.js, React, Tailwind CSS
(Optional but recommended) Screenshots of core flows: Not included in repo, but main screen shows a two‑column layout with Notes on the left and Tasks on the right, all styled with a dark blue theme.

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - Saat pertama kali menjalankan app, aku kena **Vite / tooling error** terkait dependency yang belum lengkap.
   - Error ini muncul ketika menjalankan dev server, dan build gagal karena beberapa paket belum ter‑install.
   - Solusinya cukup straightforward: aku menjalankan `npm install` di folder proyek Next.js untuk menginstall semua dependency yang dibutuhkan, lalu dev server bisa jalan normal.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel):
   - Di Composer, aku memandu AI dengan prompt yang cukup spesifik: layout dua kolom (Notes dan Tasks), dark mode, dan gaya “developer dashboard”.
   - Untuk styling, aku minta Tailwind utility classes yang clean tanpa terlalu banyak animasi, supaya konsisten dengan feel “productivity tool”.
   - Hal yang kurang bekerja dengan baik adalah ketika aku meminta terlalu banyak fitur sekaligus (filtering, drag‑and‑drop), Composer cenderung membuat kode yang gemuk dan agak sulit diikuti, jadi aku pecah permintaan menjadi langkah-langkah kecil (UI dulu, lalu interaksi dasar).

c. Approximate time-to-first-run and time-to-feature metrics:
   - Time‑to‑first‑run: ~30–40 menit (setup Next.js, menyelesaikan error dependency, dan menjalankan dev server pertama kali).
   - Time‑to‑feature (Notes + Tasks basic CRUD di UI dengan layout dark mode): ~1,5–2 jam termasuk iterasi desain Tailwind dan penyesuaian kecil di komponen.
```

## Version #2 Description
```
APP DETAILS:
===============
Folder name: week8/django-app
AI app generation platform: Cursor Composer + inline agents (Chat) untuk modifikasi bertahap
Tech Stack: Django + SQLite + HTML templates (Tailwind CSS via CDN)
Persistence: SQLite database (db.sqlite3) dengan model Note dan Task
Frameworks/Libraries Used: Django, Django ORM, Tailwind CSS (CDN)
(Optional but recommended) Screenshots of core flows: Tidak disertakan, tetapi tampilan utama adalah dashboard dark mode dengan dua panel (Notes dan Tasks) yang sangat mirip dengan konsep di versi Next.js.

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - Issue utama: **folder `flask-app` sempat “nyasar” ke dalam `django-app`** sehingga environment bercampur dan menimbulkan error **EBUSY (file locked)** saat mencoba memodifikasi / menghapus beberapa file.
   - Error EBUSY terjadi karena file database dan environment sedang terbuka/terpakai oleh terminal dan proses lain, sehingga Windows menolak operasi file tertentu.
   - Solusi: aku menutup seluruh terminal dan proses yang masih memakai folder tersebut, lalu memindahkan folder `flask-app` keluar secara manual ke lokasi yang benar di dalam `week8`. Setelah struktur folder rapi, error EBUSY hilang dan Django bisa dijalankan normal.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel):
   - Aku menggunakan Composer untuk membuat skeleton Django project (settings, urls, app `core`), lalu memakai Chat/Agent untuk langkah-langkah spesifik seperti menambahkan `INSTALLED_APPS`, membuat model, view `dashboard`, dan routing.
   - Hal yang sangat membantu adalah meminta Composer/agent untuk **“sinkronisasi” antar file**: misalnya, ketika aku bilang ingin `dashboard` dan form Notes/Tasks, ia otomatis mengupdate `core/views.py`, `core/urls.py`, dan `core/templates/dashboard.html` dengan struktur yang konsisten.
   - Yang kurang bekerja baik adalah ketika aku memberikan instruksi yang terlalu abstrak (mis. “bikinin dashboard lengkap kaya Notion”); hasilnya terlalu kompleks. Setelah aku mempersempit prompt ke alur yang jelas (input note, input task, list data), hasilnya jauh lebih usable.

c. Approximate time-to-first-run and time-to-feature metrics:
   - Time‑to‑first‑run: ~45–60 menit (setup Django, install dependency, konfigurasi settings, dan runserver pertama kali).
   - Time‑to‑feature (dashboard Notes + Tasks dengan Tailwind dark mode dan tersambung ke SQLite): ~2–3 jam, termasuk debugging error EBUSY dan perbaikan struktur folder.
```

## Version #3 Description
```
APP DETAILS:
===============
Folder name: week8/flask-app
AI app generation platform: Cursor Composer + Chat agents (satu file `app.py` dan `templates/index.html`)
Tech Stack: Flask + Flask-SQLAlchemy + SQLite + Jinja templates (Tailwind CSS via CDN)
Persistence: SQLite database (`dev_control.sqlite3`) dengan model Note dan Task
Frameworks/Libraries Used: Flask, Flask-SQLAlchemy, SQLAlchemy, Jinja2, Tailwind CSS (CDN)
(Optional but recommended) Screenshots of core flows: Tidak ada screenshot di repo, tetapi UI hampir identik dengan versi Django: dark mode, badge status, dua kolom Notes dan Tasks.

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - Masalah utama adalah **`ModuleNotFoundError: No module named 'flask_sqlalchemy'`** ketika menjalankan `app.py`.
   - Penyebabnya simpel: environment global Python belum terinstall paket Flask‑SQLAlchemy (dan bahkan Flask sendiri di environment tertentu).
   - Solusi: menjalankan `pip install flask flask_sqlalchemy` di dalam folder `flask-app` (atau environment yang dipakai), lalu menjalankan `python app.py` lagi. Setelah itu database `dev_control.sqlite3` otomatis dibuat lewat fungsi `init_db()` saat aplikasi start.

b. Prompting (e.g. what required additional guidance; what worked poorly/wel):
   - Di Composer/Chat, aku dengan sengaja membatasi scope: satu file `app.py` yang memuat konfigurasi Flask, model SQLAlchemy, dan semua route, plus satu template `index.html`.
   - Aku juga meminta UI dark mode yang “konsisten dengan versi Django” sehingga agent bisa meniru struktur Tailwind (badge Online, dua section, footer).
   - Yang sedikit tricky adalah menyusun prompt agar database **otomatis terbuat** saat first run; begitu aku menjelaskan bahwa aku ingin fungsi helper `init_db()` yang memanggil `db.create_all()` sebelum `app.run()`, agent bisa menghasilkan pola itu dengan baik.

c. Approximate time-to-first-run and time-to-feature metrics:
   - Time‑to‑first‑run: ~30–40 menit (install Flask/Flask‑SQLAlchemy, wiring route dasar, dan memastikan DB otomatis terbuat).
   - Time‑to‑feature (dashboard lengkap dengan Notes + Tasks, dark mode UI, dan SQLite yang persist): ~1,5–2 jam termasuk beberapa iterasi kecil di struktur template dan penamaan field.
```

