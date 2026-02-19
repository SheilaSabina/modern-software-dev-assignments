from __future__ import annotations

import json
import re
from typing import List

from dotenv import load_dotenv
from ollama import chat

load_dotenv()

# --- LOGIKA LAMA (REGEX & HEURISTIC) ---
BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    """
    Ekstraksi menggunakan pola regex dan kata kunci (Cara Lama).
    """
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters

# --- TODO 1: Implementasi LLM-powered extraction menggunakan Ollama ---
# Bagian ini dibuat untuk mendeteksi action items secara cerdas dan fleksibel terhadap bahasa input.
def extract_action_items_llm(text: str) -> List[str]:
    """
    Ekstraksi action items menggunakan LLM (Ollama).
    Diperbaiki untuk menangkap tugas dari berbagai perspektif kalimat.
    """

    # Perbaikan pada System Prompt agar lebih mendetail
    system_prompt = """
    You are an expert secretary assistant. Your task is to identify and extract ALL action items, 
    tasks, or commitments mentioned in the meeting notes.
    
    Guidelines:
    1. Extract tasks assigned to others, personal commitments, and general todos.
    2. ALWAYS respond in BAHASA INDONESIA. Do not translate the tasks to English.
    3. Keep the descriptions concise but clear.
    
    Output Format:
    - You MUST return a valid JSON object.
    - Key: "action_items"
    - Value: A list of strings.
    - Example: {"action_items": ["beli camilan", "email klien"]}
    """

    try:
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract action items from these notes:\n\n{text}"},
            ],
            # Menggunakan temperature sedikit lebih tinggi (0.3) agar AI lebih fleksibel
            # memahami bahasa manusia, namun tetap terkontrol.
            options={"temperature": 0.3},
            format="json",
        )

        content = response.message.content
        data = json.loads(content)

        return data.get("action_items", [])

    except Exception as e:
        print(f"Error calling LLM: {e}")
        return []
