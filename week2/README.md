# Week 2 – Action Item Extractor

Aplikasi FastAPI + SQLite yang mengubah catatan rapat atau teks bebas menjadi daftar action items (tugas). Mendukung ekstraksi dengan **regex/heuristik** dan **LLM (Ollama)**.

## Overview Proyek

- **Backend:** FastAPI dengan SQLite (`app/data/app.db`), inisialisasi DB lewat lifespan.
- **Fitur utama:**
  - CRUD catatan (notes): buat, list, ambil satu, hapus.
  - Ekstraksi action items dengan **regex** (pola bullet, keyword, checkbox).
  - Ekstraksi action items dengan **AI** via Ollama (model `llama3.1:8b`), output JSON.
- **Frontend:** Satu halaman HTML di `/` dengan tema biru, modal hapus, dan toast notifikasi.

Struktur singkat:

```
week2/
├── app/
│   ├── main.py          # FastAPI app, lifespan, mount static
│   ├── schemas.py       # Pydantic: Note, NoteCreate, ActionItem
│   ├── routers/
│   │   ├── notes.py     # GET/POST/DELETE notes
│   │   └── action_items.py  # POST extract & extract-llm
│   ├── services/
│   │   ├── db.py        # SQLite: init, notes, action_items
│   │   └── extract.py   # Regex + LLM extraction
│   └── data/            # app.db (dibuat otomatis)
├── frontend/
│   └── index.html
├── tests/
│   └── test_extract.py  # Unit test regex & LLM extract
└── README.md
```

---

## Instalasi

Proyek ini memakai dependensi dari **root repo** (`pyproject.toml` di atas folder `week2`). Jalankan perintah di **root repository** (parent dari `week2`).

### Opsi 1: Conda + Poetry

1. Buat/aktifkan environment Conda (Python ≥3.10):

   ```bash
   conda create -n cs146s python=3.10 -y
   conda activate cs146s
   ```

2. Dari **root repo**, pasang dependensi dengan Poetry:

   ```bash
   cd path/ke/modern-software-dev-assignments
   poetry install
   ```

3. (Opsional) Jika ingin pakai Conda saja tanpa Poetry, ekspor lalu pasang:

   ```bash
   poetry export -f requirements.txt --without-hashes -o requirements.txt
   pip install -r requirements.txt
   ```

### Opsi 2: Poetry saja

1. Pastikan Python 3.10+ terpasang.
2. Dari **root repo**:

   ```bash
   cd path/ke/modern-software-dev-assignments
   poetry install
   ```

---

## Menjalankan Server (Uvicorn)

Dari **root repository** (bukan dari dalam folder `week2`):

```bash
# Jika pakai Poetry
poetry run uvicorn week2.app.main:app --reload

# Jika pakai Conda + Poetry (setelah poetry install)
conda activate cs146s
poetry run uvicorn week2.app.main:app --reload
```

- **URL aplikasi:** http://127.0.0.1:8000/
- **Docs API:** http://127.0.0.1:8000/docs

`--reload` dipakai agar server me-reload saat kode berubah.

---

## Menjalankan Ollama (untuk Ekstraksi LLM)

Endpoint **Extract LLM** memanggil Ollama dengan model `llama3.1:8b`. Ollama harus berjalan di mesin yang sama.

1. **Instal Ollama**  
   https://ollama.com/download

2. **Jalankan Ollama** (biasanya otomatis sebagai service; kalau manual):

   ```bash
   ollama serve
   ```

3. **Pull dan siapkan model** (sekali saja):

   ```bash
   ollama pull llama3.1:8b
   ollama run llama3.1:8b
   ```

   Untuk cek model terpasang: `ollama list`.

4. Pastikan backend bisa mengakses `http://localhost:11434`. Jika Ollama tidak jalan, ekstraksi LLM akan gagal (service mengembalikan list kosong).

---

## Daftar API Endpoints

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| `GET`  | `/` | Halaman utama (HTML). |
| `GET`  | `/notes` | Daftar semua catatan. Response: `List[Note]`. |
| `POST` | `/notes` | Buat catatan baru. Body: `{"content": "..."}`. Response: `Note`. |
| `GET`  | `/notes/{note_id}` | Ambil satu catatan. Response: `Note`. 404 jika tidak ada. |
| `DELETE` | `/notes/{note_id}` | Hapus catatan dan action items terkait. Response: `{"status": "success"}`. |
| `POST` | `/notes/{note_id}/extract` | Ekstraksi action items dengan **regex**. Response: `List[ActionItem]`. |
| `POST` | `/notes/{note_id}/extract-llm` | Ekstraksi action items dengan **Ollama LLM**. Response: `List[ActionItem]`. |

**Schema singkat:**

- **Note:** `id`, `content`, `created_at`, (opsional) `action_items`.
- **NoteCreate:** `content`.
- **ActionItem:** `description`.

---

## Menjalankan Unit Tests

Tests ada di `week2/tests/test_extract.py` (regex + LLM). Jalankan dari **root repository** agar import `week2` berhasil:

```bash
# Dari root repo
poetry run pytest week2/tests/ -v

# Hanya test extract
poetry run pytest week2/tests/test_extract.py -v

# Dengan output print (untuk debug LLM)
poetry run pytest week2/tests/test_extract.py -v -s
```

- **Test regex:** `test_extract_bullets_and_checkboxes` (tidak butuh Ollama).
- **Test LLM:** `test_extract_llm_simple` membutuhkan **Ollama berjalan** dan model `llama3.1:8b`; jika Ollama mati atau model belum di-pull, tes ini bisa gagal atau mengembalikan list kosong.

---

## Ringkasan Cepat

| Yang dilakukan | Perintah (dari root repo) |
|----------------|----------------------------|
| Instal (Conda + Poetry) | `conda activate cs146s` → `poetry install` |
| Instal (Poetry saja) | `poetry install` |
| Jalankan server | `poetry run uvicorn week2.app.main:app --reload` |
| Jalankan Ollama | `ollama serve` lalu `ollama pull llama3.1:8b` |
| Jalankan tests | `poetry run pytest week2/tests/ -v` |
