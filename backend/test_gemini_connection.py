"""
Manual connectivity check for GEMINI_API_KEY.

Not a unit test (no mocking) — this makes a real API call and costs quota.
Run it by hand when you need to confirm the key in .env is valid, distinct
from tests/test_scam_detection.py which mocks genai.Client on purpose.

Usage:
    python test_gemini_connection.py
"""
from google import genai
from google.genai import types

from config import Config


def main():
    api_key = Config.GEMINI_API_KEY
    if not api_key:
        print("FAILED: GEMINI_API_KEY is not set in .env / environment.")
        return

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="Reply with exactly the word OK.",
        )
    except Exception as e:
        print(f"FAILED: key rejected or request errored.\n  {type(e).__name__}: {e}")
        return

    text = (response.text or "").strip()
    if not text:
        print("FAILED: key accepted the request but returned an empty response.")
        return

    print("SUCCESS: Gemini API key is valid and reachable.")
    print(f"  Model response: {text!r}")


if __name__ == "__main__":
    main()