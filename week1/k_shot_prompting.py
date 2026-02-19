import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """
Reverse the word exactly character by character.

Example 1:
Input: h t t p s t a t u s
Output: s u t a t s p t t h
Final: sutatsptth

Example 2:
Input: a b b a c
Output: c a b b a
Final: cabba

Rules:
- Reverse strictly from last character to first.
- Keep all repeated letters.
- Do not drop or duplicate characters.
- The final answer must contain the same number of characters as the input.
- Output only the final reversed word (like the "Final" examples).
"""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""

EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)