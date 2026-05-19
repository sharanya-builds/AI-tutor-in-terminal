import os
import sys
import json
import ollama

CHAT_MODEL   = "llama3.2"
HISTORY_FILE = "history.json"
NAME_FILE    = "user_name.txt"
MAX_MESSAGES = 20

# ── Name helpers ─────────────────────────────────────────────────────────────

def load_name():
    if os.path.exists(NAME_FILE):
        with open(NAME_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def save_name(name):
    with open(NAME_FILE, "w", encoding="utf-8") as f:
        f.write(name)

# ── JSON helpers ──────────────────────────────────────────────────────────────

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
            except json.JSONDecodeError:
                print("   ⚠️  history.json was corrupted — starting fresh.\n")
    return []

def save_history(messages):
    to_save = [m for m in messages if m["role"] != "system"]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(to_save, f, indent=2, ensure_ascii=False)

# ── Get or ask for name ───────────────────────────────────────────────────────

user_name = load_name()
if not user_name:
    user_name = input("Hey! What's your name? ").strip()
    if not user_name:
        user_name = "there"
    save_name(user_name)
    print()

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        f"You are {user_name}'s personal tutor and coding assistant. "
        "Be conversational, warm, and direct — like a smart friend who actually knows this stuff. "
        "When they are debugging, don't give the answer away immediately — ask what they think is wrong first, then guide them. "
        "When they ask a question or want something explained, give a proper, well-structured answer. "
        "Not too short that it's unhelpful, not too long that it's overwhelming. "
        "If it's a simple question, keep it brief. If it's a concept, explain it properly with an example. "
        "If they ask for more detail, go deeper. "
        "Never use meta-commentary about your own teaching style. "
        "IMPORTANT: Never ever use asterisks for any expressions, emotions or actions. No *waves*, no *smiles*, no *excited*, nothing in asterisks at all. Do not use emojis either. You can use ! to show enthusiasm but that is the only exception. This rule cannot be broken under any circumstance. "
        f"If this is the very first message in the conversation, greet {user_name} and ask: "
        "'What are we working on today? Should I explain a concept, clear up some doubts, or jump straight into debugging your code?'"
    ),
}

# ── Load saved history ────────────────────────────────────────────────────────

saved = load_history()
messages = [SYSTEM_MESSAGE] + saved

print("🦆 Rubber Duck ready!")
print("   Ask anything or use /read to load a file.")
print("   (type 'exit' to quit)\n")

if saved:
    print(f"   📂 Loaded {len(saved)} messages from previous session.\n")

# ── Main loop ─────────────────────────────────────────────────────────────────

while True:

    # Check history length
    non_system = [m for m in messages if m["role"] != "system"]
    if len(non_system) >= MAX_MESSAGES:
        print(f"\n⚠️  History is getting too long ({len(non_system)} messages).")
        print("   What do you want to do?\n")
        print("   [1] Keep the last 6 messages and delete the rest")
        print("   [2] Delete everything and start completely fresh")

        while True:
            choice = input("\n   Your choice (1/2): ").strip()
            if choice in ("1", "2"):
                break
            print("   Please enter 1 or 2.")

        if choice == "1":
            last_few = non_system[-6:]
            messages = [SYSTEM_MESSAGE] + last_few
            save_history(messages)
            print("   ✅ Kept last 6 messages. Continuing with trimmed context.\n")
        else:
            messages = [SYSTEM_MESSAGE]
            save_history(messages)
            print("   ✅ History wiped. Fresh start!\n")

    user_input = input("You: ").strip()

    if user_input.lower() in ("exit", "quit"):
        save_history(messages)
        print("🦆 Quack. Good luck!")
        break

    if not user_input:
        continue

    # /read command
    if user_input.startswith("/read "):
        filepath = user_input.split("/read ", 1)[1].strip().strip("'\"& ")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            messages.append({
                "role": "user",
                "content": (
                    f"Here is my EXACT code from {filepath}, do not assume anything outside of this:\n\n"
                    f"```\n{code}\n```\n\n"
                    "Only refer to this exact code. "
                    "Do not invent variables, errors, or keywords that aren't here."
                ),
            })
            save_history(messages)
            print(f"🦆 Duck: Got it, I've read {filepath}. What's the problem?\n")
        else:
            print(f"   ❌ File not found: {filepath}\n")
        continue

    # Normal message
    messages.append({"role": "user", "content": user_input})

    print("🦆 Duck: ", end="", flush=True)
    full_reply = ""

    try:
        stream = ollama.chat(
            model=CHAT_MODEL,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            token = chunk["message"]["content"]
            print(token, end="", flush=True)
            full_reply += token

    except Exception as e:
        print(f"\n❌ Error talking to Ollama: {e}")
        messages.pop()
        continue

    print()
    messages.append({"role": "assistant", "content": full_reply})
    save_history(messages)
