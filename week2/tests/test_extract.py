from week2.app.services.extract import extract_action_items, extract_action_items_llm


# --- TES FUNGSI LAMA (REGEX) ---
def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# --- TES FUNGSI BARU (AI / LLM) - TODO 2 ---
def test_extract_llm_simple():
    """
    Tes apakah LLM bisa menangkap tugas dari kalimat narasi biasa
    (yang tidak bisa dilakukan oleh Regex biasa).
    """
    text = """
    Hi team, quick recap.
    We need to buy snacks for the party next week.
    Also, please email the client about the delay.
    Thanks!
    """

    # Panggil fungsi LLM
    items = extract_action_items_llm(text)

    # Debugging: Cetak hasil ke terminal biar kita bisa lihat
    print(f"\n[LLM Output]: {items}")

    # Assertions (Pengecekan)
    # 1. Pastikan hasilnya berupa list
    assert isinstance(items, list)

    # 2. Pastikan minimal ada 2 tugas yang terdeteksi
    assert len(items) >= 2

    # 3. Cek apakah kata kunci penting tertangkap (case insensitive)
    # Kita gabung semua item jadi satu string biar gampang ngeceknya
    combined_text = " ".join(items).lower()

    assert "beli camilan" in combined_text or "camilan" in combined_text
    assert "email" in combined_text or "klien" in combined_text
