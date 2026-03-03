# /db-check
**Intent**: Memeriksa data terbaru di tabel notes dan action_items untuk verifikasi fungsionalitas.
**Steps**:
1. Jalankan perintah: `sqlite3 data/dev.db "SELECT * FROM notes ORDER BY id DESC LIMIT 3;"`
2. Jalankan perintah: `sqlite3 data/dev.db "SELECT * FROM action_items ORDER BY id DESC LIMIT 3;"`
3. Berikan ringkasan data yang ditemukan kepada pengguna.