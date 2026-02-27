# Week 0: Launch Pad

**Time required:** 30–45 minutes
**Complete before:** Session 1 of the course
**Goal:** Your environment works. You've talked to Claude via code. You've met your cohort.

---

## How the Course Works

Each week has **five sessions** (30–45 minutes each) and a **weekly project**. The sessions build on each other sequentially — Session 3 assumes you've done Sessions 1 and 2 — but you work through them at your own pace within the week.

Binge all five on a Tuesday evening. Spread them out. Do three on Saturday and two on Sunday. Whatever fits around your lectures, labs, assignments, and life.

The one fixed point is the **weekly project deadline (Sunday)**. That's when you share your work on Anseo, and when peer review starts. This is how the cohort stays in sync.

**Time commitment: ~5 hours per week.** Two evenings and a Saturday morning. Or one long Sunday. That's it.

**Miss a week?** It happens — exams, deadlines, life. You can rejoin the following week. The Anseo community posts and peer projects serve as a record of what you missed, so you can catch up on context without falling behind permanently.

---

## What You Need Before You Start

This course assumes you can already write code. You don't need to be an expert, but you should be comfortable with:

- Writing and running Python (functions, loops, dictionaries, basic file I/O)
- Using Git for version control (commit, push, pull, branch)
- Navigating a terminal
- Reading API documentation

If you're unsure whether you're ready, here's a quick test: if you could build a simple web scraper in Python given an afternoon and access to documentation, you're ready. If "web scraper" sounds intimidating, consider doing a Python fundamentals course first — there are excellent free ones — and coming back.

**You do NOT need:**
- Any AI or machine learning experience
- A CS degree
- DevOps knowledge
- A powerful computer (everything runs in the cloud)

---

## Step 1: Create Your Accounts

You need four accounts. That's it.

### GitHub
If you don't already have one: [github.com](https://github.com)

**Important:** Use a professional username. This becomes part of your portfolio. `cool_hacker_69` will haunt you in job applications.

If you're a student, apply for the [GitHub Student Developer Pack](https://education.github.com/pack) — it includes free Codespaces hours and other tools we'll use.

### Anthropic
Go to [console.anthropic.com](https://console.anthropic.com) and create an account.

Once you're in:
1. Navigate to **API Keys**
2. Click **Create Key**
3. Name it `bwai-course`
4. Copy the key immediately — you won't see it again

The key looks like: `sk-ant-api03-xxxxx...`

**Keep this key private.** Never commit it to Git. Never paste it in a public chat. Treat it like a password.

New accounts include free API credits. The entire course will cost a few euros in API usage at most — we use efficient models and small prompts.

### Railway
Go to [railway.app](https://railway.app) and sign up **using your GitHub account**. This links them together and makes deployment seamless later.

You don't need to create any projects yet. Just have the account ready.

### Anseo
Go to [anseo.irish](https://anseo.irish) and create your account. Join the **Building With AI** course community.

This is where you'll share your work, get help, review peers' projects, and find your cohort. It's not a side channel — it's core to how the course works.

---

## Step 2: Open the Course Codespace

We use **GitHub Codespaces** — a full development environment that runs in your browser. No local installation required. It's VS Code, a Linux terminal, Python, and all the tools you need, ready in about 90 seconds.

### Open it:

1. Go to the course repository: `github.com/[COURSE_ORG]/bwai`
2. Click the green **Code** button
3. Select the **Codespaces** tab
4. Click **Create codespace on main**

Wait for it to build. The first time takes 2–3 minutes. Subsequent opens are faster.

When it's ready, you'll see VS Code in your browser with a terminal at the bottom.

### Add your API key:

**Option A — Codespace Secrets (recommended):**

This keeps your key secure and available across all Codespaces.

1. Go to [github.com/settings/codespaces](https://github.com/settings/codespaces)
2. Click **New secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: paste your `sk-ant-...` key
5. Repository access: select the course repo
6. If your Codespace is already running, restart it

**Option B — .env file:**

In the Codespace terminal:

```bash
cp .env.example .env
```

Edit `.env` and paste your key:

```
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

The `.env` file is in `.gitignore` so it won't be committed. But Option A is safer.

### Connect to Anseo:

Once your Anseo account is set up, generate an API token so the course CLI can share your projects to the community automatically.

1. Log in to [anseo.irish](https://anseo.irish)
2. Go to **Settings → API Tokens**
3. Click **Generate Token**, name it `bwai course CLI`
4. Copy the token immediately (you won't see it again)

**Add it to Codespace Secrets** (same process as the Anthropic key):

1. Go to [github.com/settings/codespaces](https://github.com/settings/codespaces)
2. **New secret:** `ANSEO_API_TOKEN` → paste your `anseo_...` token
3. Restart your Codespace if it's running

Or add it to your `.env` file:

```
ANSEO_URL=https://anseo.irish
ANSEO_API_TOKEN=anseo_your_token_here
```

This is optional for Week 0 but you'll want it working by Week 1's weekly project.

---

## Step 3: Run the Verification

In the Codespace terminal:

```bash
python verify.py
```

You should see something like:

```
=========================================================
  Building With AI — Environment Verification
=========================================================

1/4  Checking Python...
     ✅ Python 3.12.x

2/4  Checking packages...
     ✅ anthropic
     ✅ fastapi
     ✅ chromadb
     ✅ rich
     ✅ click
     ✅ pytest

3/4  Testing Anthropic API...
     ✅ Claude responded: {"status": "ok", "message": "Welcome to Building With AI!"}
        Tokens used: 52 in, 23 out

4/4  Checking Git...
     ✅ git version 2.x.x
     ✅ Identity: Your Name <you@example.com>

=========================================================
  ✅ ALL CHECKS PASSED — You're ready for Session 1!
=========================================================
```

**If anything fails:** read the error message. It tells you exactly what to fix. If you're stuck, post the full output on Anseo in the Week 0 help thread. Someone — a peer or a course facilitator — will help you.

---

## Step 4: Try the Course CLI

The course includes a small command-line tool called `bwai` that handles project scaffolding, environment checks, and submission.

It's already installed — the Codespace set it up automatically when it built (from the `tools/` directory in the repo). If you ever need to reinstall it manually, run `pip install -e tools/` from the repo root.

Test it:

```bash
bwai check-env
```

This runs a more detailed version of the verification with colour-coded output.

Then try:

```bash
bwai api-test
```

This sends a prompt to Claude and shows you the response with token counts. You just made your first API call. That's the foundation everything else builds on.

Explore what's available:

```bash
bwai --help
```

---

## Step 5: Scaffold Your First Project

Let's make sure the full workflow works — create, code, commit, push.

```bash
bwai new-project hello-claude --week 1
```

This creates a project structure at `projects/week1-thinking-with-ai/hello-claude/`.

Open `src/main.py` and replace the contents with:

```python
"""My first AI interaction via code."""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


def main():
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": "In one sentence, what's the most important thing for a developer to understand about working with AI?"
        }]
    )

    print(response.content[0].text)


if __name__ == "__main__":
    main()
```

Run it:

```bash
cd projects/week1-thinking-with-ai/hello-claude
python src/main.py
```

Claude should respond with a sentence. You've just written your first AI-powered script.

---

## Step 6: Introduce Yourself on Anseo

Head to the course community on Anseo and post in the **Introductions** thread. Share:

- Your name (or handle — whatever you're comfortable with)
- What you do right now (student, working developer, career switcher)
- One thing you want to be able to build with AI by the end of this course
- Whether your `verify.py` passed (and if not, what's stuck)

Read a few other introductions. Reply to at least one. You'll be reviewing each other's work for the next six weeks — start building those connections now.

---

## What You Don't Need To Do

- **Don't install Python locally.** Codespaces handles it.
- **Don't configure Docker.** Not needed.
- **Don't set up a database.** That comes in Week 4, inside the Codespace.
- **Don't deploy anything yet.** Railway deployment starts in Week 3.
- **Don't read ahead.** Each session is designed to build on the previous one. Skipping ahead breaks the learning model.

---

## If Something Goes Wrong

In order of what to try:

1. **Read the error message.** Most issues are a missing key, a typo, or a package that didn't install.
2. **Run `bwai check-env` again.** It will tell you specifically what's wrong.
3. **Stop and restart the Codespace.** GitHub menu → Codespaces → Stop → Restart. This fixes most mysterious issues.
4. **Delete and recreate the Codespace.** You won't lose any committed code. GitHub menu → Codespaces → Delete → Create new one from the repo.
5. **Post on Anseo.** Include the full error output. Someone will help. This isn't a solo course — asking for help is part of how it works.

---

## Checklist

Before Session 1, confirm you can tick all of these:

- [ ] GitHub account created
- [ ] Anthropic API key generated
- [ ] Railway account created (linked to GitHub)
- [ ] Anseo account created, joined course community
- [ ] Anseo API token generated (optional but recommended)
- [ ] Codespace opens and runs
- [ ] `python verify.py` passes all checks
- [ ] `bwai check-env` shows green
- [ ] `bwai api-test` gets a response from Claude
- [ ] hello-claude project runs and prints a response
- [ ] Posted introduction on Anseo
- [ ] Read and replied to at least one peer's introduction

If all boxes are ticked, you're ready. See you in Session 1.
