# Week 3 — Build a Custom MCP Server (Game Discovery)

## Deskripsi Proyek
Proyek ini mengimplementasikan Model Context Protocol (MCP) server yang menghubungkan AI dengan **RAWG Video Games API**. Server ini menggunakan transport STDIO untuk mencari data game secara real-time.

## Kapabilitas (Tools)
1. `search_game(name: str)`: Mencari hingga 5 game berdasarkan input nama. Mengembalikan ID, nama, dan rating dalam format JSON string.
2. `get_game_detail(game_id: int)`: Mengambil detail mendalam (tanggal rilis dan rating) menggunakan ID game unik.

## Struktur Folder
- `server/main.py`: Entrypoint utama MCP Server.
- `requirements.txt`: Daftar dependensi.
- `README.md`: Dokumentasi proyek.

## Prasyarat & Instalasi
1. Pastikan Python 3.10+ terinstal.
2. Buka terminal di dalam folder `week3/` dan instal dependensi:
   `pip install -r requirements.txt`

## Konfigurasi Client (Claude Desktop)
Tambahkan konfigurasi berikut ke dalam file `claude_desktop_config.json`:

{
  "mcpServers": {
    "game-server": {
      "command": "C:/path/to/your/python.exe",
      "args": [
        "D:/path/to/your/week3/server/main.py"
      ],
      "env": {
        "RAWG_API_KEY": "ISI_API_KEY_ANDA_DI_SINI"
      }
    }
  }
}

## Implementasi Ketahanan (Resilience)
- **Error Handling**: Menggunakan blok `try-except` untuk menangkap kegagalan HTTP.
- **HTTP Validation**: Memanggil `response.raise_for_status()` untuk mengidentifikasi status error dari API.
- **Empty Results**: Memberikan respons "Game not found" jika pencarian tidak membuahkan hasil, mencegah crash pada klien.

## Contoh Penggunaan (Invocation)
* "Tolong cari game berjudul 'Elden Ring' menggunakan tool saya."
* "Berapa rating dan tanggal rilis untuk game dengan ID 3245?"