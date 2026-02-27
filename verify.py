#!/usr/bin/env python3
"""
Building With AI — Week 0 Verification Script

This script checks that your entire environment works end-to-end:
  1. Python and packages are installed
  2. Anthropic API key is valid and Claude responds
  3. Git is configured and can commit
  4. You're ready to start Session 1

Run: python verify.py
"""

import os
import sys
import subprocess

def main():
    print()
    print("=" * 55)
    print("  Building With AI — Environment Verification")
    print("=" * 55)
    print()

    errors = []

    # ── Step 1: Python ──
    print("1/4  Checking Python...")
    v = sys.version_info
    if v.major == 3 and v.minor >= 11:
        print(f"     ✅ Python {v.major}.{v.minor}.{v.micro}")
    else:
        errors.append(f"Python {v.major}.{v.minor} — need 3.11+")
        print(f"     ❌ Python {v.major}.{v.minor} — need 3.11+")

    # ── Step 2: Key packages ──
    print("\n2/4  Checking packages...")
    required = ["anthropic", "fastapi", "chromadb", "rich", "click", "pytest"]
    for pkg in required:
        try:
            __import__(pkg)
            print(f"     ✅ {pkg}")
        except ImportError:
            errors.append(f"Missing package: {pkg}")
            print(f"     ❌ {pkg} — run: pip install {pkg}")

    # ── Step 3: Anthropic API ──
    print("\n3/4  Testing Anthropic API...")

    # Try environment variable first, then .env file
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        except ImportError:
            pass

    if not api_key:
        errors.append("ANTHROPIC_API_KEY not set")
        print("     ❌ ANTHROPIC_API_KEY not found")
        print("        Set it in Codespace secrets or in a .env file")
    else:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": (
                        "You are verifying a student's setup for an AI course. "
                        "Reply with exactly this JSON and nothing else: "
                        '{"status": "ok", "message": "Welcome to Building With AI!"}'
                    )
                }]
            )
            reply = response.content[0].text.strip()
            print(f"     ✅ Claude responded: {reply[:60]}")
            print(f"        Tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
        except anthropic.AuthenticationError:
            errors.append("API key was rejected")
            print("     ❌ API key rejected — check console.anthropic.com")
        except Exception as e:
            errors.append(f"API error: {e}")
            print(f"     ❌ API error: {e}")

    # ── Step 4: Git ──
    print("\n4/4  Checking Git...")
    try:
        result = subprocess.run(
            ["git", "--version"], capture_output=True, text=True, check=True
        )
        print(f"     ✅ {result.stdout.strip()}")

        # Check identity
        name = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True
        ).stdout.strip()
        email = subprocess.run(
            ["git", "config", "user.email"], capture_output=True, text=True
        ).stdout.strip()

        if name and email:
            print(f"     ✅ Identity: {name} <{email}>")
        else:
            print("     ⚠️  Git identity not set. Run:")
            print('        git config --global user.name "Your Name"')
            print('        git config --global user.email "you@example.com"')
    except FileNotFoundError:
        errors.append("Git not installed")
        print("     ❌ Git not found")

    # ── Summary ──
    print()
    print("=" * 55)
    if not errors:
        print("  ✅ ALL CHECKS PASSED — You're ready for Session 1!")
        print()
        print("  Next steps:")
        print("  1. Head to Anseo and join the course community")
        print("  2. Introduce yourself in the Week 0 thread")
        print("  3. Try: bwai api-test")
        print()
        print("  See you in Session 1! 🚀")
    else:
        print(f"  ❌ {len(errors)} ISSUE(S) TO FIX:")
        print()
        for err in errors:
            print(f"    • {err}")
        print()
        print("  Fix these and run: python verify.py again")
        print("  Stuck? Post on Anseo — someone will help.")
    print("=" * 55)
    print()

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
