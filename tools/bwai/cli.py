"""
Building With AI — Course CLI Tool

Commands:
    bwai check-env      Verify your environment is set up correctly
    bwai new-project    Scaffold a new weekly project
    bwai submit         Push, deploy, and share your project
    bwai token-count    Count tokens in a file or string
    bwai api-test       Quick test of your Anthropic API connection
"""

import os
import subprocess
import shutil
import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def run(cmd: str, capture: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command."""
    return subprocess.run(
        cmd, shell=True, capture_output=capture, text=True, check=check
    )


def check_passed(label: str):
    rprint(f"  [green]✅ {label}[/green]")


def check_failed(label: str, hint: str):
    rprint(f"  [red]❌ {label}[/red]")
    rprint(f"     [grey70]{hint}[/grey70]")


def check_warned(label: str, hint: str):
    rprint(f"  [yellow]⚠️  {label}[/yellow]")
    rprint(f"     [grey70]{hint}[/grey70]")


# ──────────────────────────────────────────────
# CLI Group
# ──────────────────────────────────────────────

@click.group()
def main():
    """Building With AI — Course CLI Tool"""
    pass


# ──────────────────────────────────────────────
# check-env
# ──────────────────────────────────────────────

@main.command("check-env")
def check_env():
    """Verify your development environment is ready."""

    console.print(Panel(
        "[bold]Building With AI — Environment Check[/bold]",
        style="bright_cyan"
    ))

    passed = 0
    failed = 0
    warnings = 0

    # 1. Python version
    console.print("\n[bold]Python[/bold]")
    try:
        result = run("python3 --version")
        version = result.stdout.strip()
        major, minor = version.replace("Python ", "").split(".")[:2]
        if int(minor) >= 11:
            check_passed(f"{version}")
            passed += 1
        else:
            check_failed(f"{version} — need 3.11+", "Update Python or use the Codespace")
            failed += 1
    except Exception:
        check_failed("Python not found", "Are you in the Codespace?")
        failed += 1

    # 2. Git
    console.print("\n[bold]Git[/bold]")
    try:
        result = run("git --version")
        check_passed(result.stdout.strip())
        passed += 1
    except Exception:
        check_failed("Git not found", "Install git or use the Codespace")
        failed += 1

    # Check git identity
    try:
        name = run("git config user.name").stdout.strip()
        email = run("git config user.email").stdout.strip()
        if name and email:
            check_passed(f"Identity: {name} <{email}>")
            passed += 1
        else:
            check_warned(
                "Git identity not set",
                "Run: git config --global user.name 'Your Name' && git config --global user.email 'you@example.com'"
            )
            warnings += 1
    except Exception:
        check_warned("Could not read git config", "Set your git identity before Session 1")
        warnings += 1

    # 3. Anthropic API key
    console.print("\n[bold]Anthropic API[/bold]")
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if not api_key:
        # Also check .env file
        env_file = Path(".env")
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    if not api_key:
        check_failed(
            "ANTHROPIC_API_KEY not set",
            "Add it to Codespace secrets or create a .env file with ANTHROPIC_API_KEY=sk-ant-..."
        )
        failed += 1
    elif not api_key.startswith("sk-ant-"):
        check_warned(
            "ANTHROPIC_API_KEY doesn't look right",
            "Key should start with 'sk-ant-'. Check console.anthropic.com"
        )
        warnings += 1
    else:
        # Actually test the key
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                messages=[{"role": "user", "content": "Reply with exactly: BWAI_OK"}]
            )
            reply = response.content[0].text.strip()
            if "BWAI_OK" in reply:
                check_passed("API key valid — Claude responded")
                passed += 1
            else:
                check_passed(f"API key valid — Claude responded (got: {reply[:30]})")
                passed += 1
        except anthropic.AuthenticationError:
            check_failed("API key rejected", "Check your key at console.anthropic.com")
            failed += 1
        except Exception as e:
            check_warned(f"API call failed: {e}", "Check your internet connection")
            warnings += 1

    # 4. Key packages
    console.print("\n[bold]Packages[/bold]")
    packages = ["anthropic", "fastapi", "chromadb", "rich", "pytest"]
    for pkg in packages:
        try:
            __import__(pkg)
            check_passed(pkg)
            passed += 1
        except ImportError:
            check_failed(pkg, f"Run: pip install {pkg}")
            failed += 1

    # 5. Railway CLI (optional)
    console.print("\n[bold]Deployment[/bold]")
    try:
        result = run("railway --version", check=False)
        if result.returncode == 0:
            check_passed(f"Railway CLI: {result.stdout.strip()}")
            passed += 1
        else:
            check_warned(
                "Railway CLI not installed",
                "Optional. Install with: npm install -g @railway/cli"
            )
            warnings += 1
    except Exception:
        check_warned(
            "Railway CLI not installed",
            "Optional. Install with: npm install -g @railway/cli"
        )
        warnings += 1

    # Summary
    console.print()
    table = Table(title="Results", show_header=False, padding=(0, 2))
    table.add_row("[green]Passed[/green]", str(passed))
    table.add_row("[yellow]Warnings[/yellow]", str(warnings))
    table.add_row("[red]Failed[/red]", str(failed))
    console.print(table)

    if failed == 0:
        console.print(Panel(
            "[bold green]You're ready! 🚀[/bold green]\n\n"
            "Your environment is set up for Building With AI.\n"
            "Head to Anseo and introduce yourself in the course community.",
            style="green"
        ))
    elif failed <= 2:
        console.print(Panel(
            "[bold yellow]Almost there![/bold yellow]\n\n"
            "Fix the issues above and run [bold]bwai check-env[/bold] again.\n"
            "Post on Anseo if you're stuck — someone will help.",
            style="yellow"
        ))
    else:
        console.print(Panel(
            "[bold red]Environment needs setup[/bold red]\n\n"
            "If you're not using GitHub Codespaces, try that first:\n"
            "Open the course repo on GitHub and click 'Create Codespace'.\n\n"
            "If you're already in a Codespace, post the output above on Anseo.",
            style="red"
        ))


# ──────────────────────────────────────────────
# new-project
# ──────────────────────────────────────────────

WEEK_THEMES = {
    1: "thinking-with-ai",
    2: "ai-augmented-coding",
    3: "ai-powered-features",
    4: "rag-and-knowledge",
    5: "agents-and-automation",
    6: "portfolio-and-next",
}

PROJECT_TYPES = {
    "weekly": "Weekly Project",
    "exercise": "Session Exercise",
    "final": "Final Project",
}


@main.command("new-project")
@click.argument("name")
@click.option("--week", "-w", type=int, required=True, help="Week number (1-6)")
@click.option(
    "--type", "-t", "project_type",
    type=click.Choice(["weekly", "exercise", "final"]),
    default="weekly",
    help="Project type"
)
def new_project(name: str, week: int, project_type: str):
    """Scaffold a new project.

    Example: bwai new-project my-rag-app --week 4
    """

    if week not in WEEK_THEMES:
        console.print("[red]Week must be 1-6[/red]")
        return

    theme = WEEK_THEMES[week]
    project_dir = Path(f"projects/week{week}-{theme}/{name}")

    if project_dir.exists():
        console.print(f"[red]Project already exists: {project_dir}[/red]")
        return

    # Create structure
    project_dir.mkdir(parents=True)
    (project_dir / "src").mkdir()
    (project_dir / "tests").mkdir()

    # .env.example
    (project_dir / ".env.example").write_text(
        "# Copy this to .env and fill in your values\n"
        "ANTHROPIC_API_KEY=sk-ant-your-key-here\n"
    )

    # .gitignore
    (project_dir / ".gitignore").write_text(
        ".env\n"
        "__pycache__/\n"
        "*.pyc\n"
        ".pytest_cache/\n"
        "*.egg-info/\n"
        ".chromadb/\n"
        "node_modules/\n"
    )

    # Main entry point
    (project_dir / "src" / "__init__.py").write_text("")
    (project_dir / "src" / "main.py").write_text(
        '"""' + f'\n{PROJECT_TYPES[project_type]} — Week {week}: {theme}\n'
        f'Project: {name}\n'
        '"""\n\n'
        'import os\n'
        'from dotenv import load_dotenv\n\n'
        'load_dotenv()\n\n\n'
        'def main():\n'
        '    """Entry point."""\n'
        '    print("Hello from ' + name + '!")\n\n\n'
        'if __name__ == "__main__":\n'
        '    main()\n'
    )

    # Test stub
    (project_dir / "tests" / "__init__.py").write_text("")
    (project_dir / "tests" / "test_main.py").write_text(
        '"""Tests for ' + name + '."""\n\n\n'
        'def test_placeholder():\n'
        '    """Replace with real tests."""\n'
        '    assert True\n'
    )

    # README
    (project_dir / "README.md").write_text(
        f"# {name}\n\n"
        f"**Building With AI** — Week {week}: {theme.replace('-', ' ').title()}\n\n"
        f"_{PROJECT_TYPES[project_type]}_\n\n"
        "## What This Does\n\n"
        "_Describe your project here._\n\n"
        "## What I Learned\n\n"
        "_Reflect on what you learned building this._\n\n"
        "## How To Run\n\n"
        "```bash\n"
        "cp .env.example .env\n"
        "# Add your API key to .env\n"
        "pip install -r requirements.txt\n"
        f"python src/main.py\n"
        "```\n\n"
        "## Live Demo\n\n"
        "_Add your Railway deployment URL here._\n\n"
        "---\n\n"
        "*Built as part of [Building With AI](https://anseo.irish) — "
        "a free course for software engineers. 6 weeks. Real projects.*\n"
    )

    # Railway config
    (project_dir / "railway.toml").write_text(
        '[build]\n'
        'builder = "nixpacks"\n\n'
        '[deploy]\n'
        'startCommand = "python src/main.py"\n'
        'restartPolicyType = "on_failure"\n'
        'restartPolicyMaxRetries = 3\n'
    )

    # Project requirements
    (project_dir / "requirements.txt").write_text(
        "anthropic>=0.42.0\n"
        "python-dotenv>=1.0.0\n"
        "# Add your project-specific dependencies below\n"
    )

    console.print(Panel(
        f"[bold green]Project created: {project_dir}[/bold green]\n\n"
        f"📁 {project_dir}/\n"
        f"   src/main.py       — Your code goes here\n"
        f"   tests/            — Your tests go here\n"
        f"   .env.example      — Copy to .env, add your API key\n"
        f"   README.md         — Fill this in as you build\n"
        f"   railway.toml      — Deployment config (ready to go)\n\n"
        f"Next steps:\n"
        f"  cd {project_dir}\n"
        f"  cp .env.example .env\n"
        f"  python src/main.py",
        style="green"
    ))


# ──────────────────────────────────────────────
# api-test
# ──────────────────────────────────────────────

@main.command("api-test")
@click.option("--prompt", "-p", default="What's one thing most developers get wrong about AI?", help="Prompt to send")
@click.option("--model", "-m", default="claude-sonnet-4-20250514", help="Model to use")
def api_test(prompt: str, model: str):
    """Quick test of your Anthropic API connection."""

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        console.print("[red]ANTHROPIC_API_KEY not set. Run: bwai check-env[/red]")
        return

    console.print(f"[grey70]Model: {model}[/grey70]")
    console.print(f"[grey70]Prompt: {prompt}[/grey70]\n")

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        with console.status("Thinking..."):
            response = client.messages.create(
                model=model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )

        reply = response.content[0].text
        usage = response.usage

        console.print(Panel(reply, title="Claude", style="bright_cyan"))
        console.print(
            f"\n[grey70]Tokens — input: {usage.input_tokens}, "
            f"output: {usage.output_tokens}[/grey70]"
        )

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("Run [bold]bwai check-env[/bold] to diagnose.")


# ──────────────────────────────────────────────
# token-count
# ──────────────────────────────────────────────

@main.command("token-count")
@click.argument("input_text", required=False)
@click.option("--file", "-f", "filepath", type=click.Path(exists=True), help="Count tokens in a file")
def token_count(input_text: str, filepath: str):
    """Count tokens in a string or file.

    Example: bwai token-count "Hello, Claude!"
    Example: bwai token-count --file prompt.txt
    """

    if filepath:
        text = Path(filepath).read_text()
        source = filepath
    elif input_text:
        text = input_text
        source = "input"
    else:
        console.print("[red]Provide text or --file[/red]")
        return

    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = len(enc.encode(text))
        chars = len(text)
        words = len(text.split())

        table = Table(title=f"Token Count: {source}", show_header=False)
        table.add_row("Characters", f"{chars:,}")
        table.add_row("Words", f"{words:,}")
        table.add_row("Tokens (approx)", f"{tokens:,}")
        table.add_row("Est. cost (Sonnet input)", f"${tokens * 0.000003:.6f}")
        console.print(table)

    except ImportError:
        console.print("[yellow]tiktoken not installed. Run: pip install tiktoken[/yellow]")


# ──────────────────────────────────────────────
# submit
# ──────────────────────────────────────────────

@main.command("submit")
@click.option("--message", "-m", default=None, help="Commit message")
@click.option("--share/--no-share", default=True, help="Share to Anseo community (default: yes)")
@click.option("--description", "-d", default=None, help="What does this project do?")
@click.option("--learnings", "-l", default=None, help="What did you learn?")
def submit(message: str, share: bool, description: str, learnings: str):
    """Push to GitHub and share on Anseo.

    Run this from inside a project directory.
    Pushes your code, then creates a post in the course community.
    """

    # Check we're in a git repo
    try:
        run("git rev-parse --is-inside-work-tree")
    except Exception:
        console.print("[red]Not inside a git repository.[/red]")
        return

    # Check for uncommitted changes
    status = run("git status --porcelain").stdout.strip()

    if status:
        if not message:
            message = click.prompt("Commit message")

        console.print("[grey70]Adding and committing changes...[/grey70]")
        run("git add -A")
        run(f'git commit -m "{message}"')

    # Push
    console.print("[grey70]Pushing to GitHub...[/grey70]")
    try:
        run("git push")
    except Exception:
        console.print("[yellow]Push failed. You may need to set up the remote:[/yellow]")
        console.print("  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git")
        console.print("  git push -u origin main")
        return

    # Get the remote URL
    remote = None
    try:
        remote = run("git remote get-url origin").stdout.strip()
        if remote.startswith("git@"):
            remote = remote.replace("git@github.com:", "https://github.com/").replace(".git", "")
        elif remote.endswith(".git"):
            remote = remote[:-4]
        console.print(f"[green]✅ Pushed to GitHub:[/green] {remote}")
    except Exception:
        console.print("[green]✅ Pushed to GitHub[/green]")

    # ── Share to Anseo ──

    if not share:
        console.print("\n[grey70]Skipped Anseo sharing (--no-share)[/grey70]")
        _print_manual_share_hint(remote)
        return

    anseo_url = os.environ.get("ANSEO_URL", "").rstrip("/")
    anseo_token = os.environ.get("ANSEO_API_TOKEN", "")

    if not anseo_url or not anseo_token:
        # Try .env file
        env_file = Path(".env")
        # Walk up to find .env (might be in project root, not subdir)
        for parent in [Path("."), *Path(".").resolve().parents]:
            candidate = parent / ".env"
            if candidate.exists():
                for line in candidate.read_text().splitlines():
                    line = line.strip()
                    if line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key == "ANSEO_URL" and not anseo_url:
                        anseo_url = val.rstrip("/")
                    elif key == "ANSEO_API_TOKEN" and not anseo_token:
                        anseo_token = val
                break

    if not anseo_url or not anseo_token:
        console.print()
        console.print("[yellow]Anseo sharing not configured.[/yellow]")
        console.print("[grey70]To enable auto-sharing, add to your .env:[/grey70]")
        console.print("[grey70]  ANSEO_URL=https://anseo.irish[/grey70]")
        console.print("[grey70]  ANSEO_API_TOKEN=anseo_your_token_here[/grey70]")
        console.print("[grey70]Generate a token at: Settings → API Tokens on Anseo[/grey70]")
        _print_manual_share_hint(remote)
        return

    # Detect project metadata from directory structure
    # Expected: projects/week{N}-{theme}/{project-name}/
    cwd = Path(".").resolve()
    project_name = cwd.name
    week = None
    project_type = "weekly"

    # Try to parse week from parent directory name
    parent_name = cwd.parent.name if cwd.parent else ""
    if parent_name.startswith("week") and "-" in parent_name:
        try:
            week = int(parent_name.split("-")[0].replace("week", ""))
        except ValueError:
            pass

    # If we couldn't detect, ask
    if week is None:
        week = click.prompt("Which week is this project for?", type=int)

    if not description:
        description = click.prompt("Brief description of what it does (or Enter to skip)", default="", show_default=False)

    if not learnings:
        learnings = click.prompt("What did you learn? (or Enter to skip)", default="", show_default=False)

    # Detect Railway live URL if available
    live_url = ""
    railway_toml = cwd / "railway.toml"
    if railway_toml.exists():
        # Check if RAILWAY_PUBLIC_DOMAIN is set
        live_url = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
        if live_url and not live_url.startswith("http"):
            live_url = f"https://{live_url}"

    # Build the payload
    payload = {
        "project_name": project_name,
        "week": week,
        "project_type": project_type,
        "github_url": remote or "",
    }
    if live_url:
        payload["live_url"] = live_url
    if description:
        payload["description"] = description
    if learnings:
        payload["learnings"] = learnings

    # POST to Anseo
    console.print("\n[grey70]Sharing to Anseo...[/grey70]")

    try:
        import httpx

        resp = httpx.post(
            f"{anseo_url}/api/v1/course/submit/",
            json=payload,
            headers={
                "Authorization": f"Bearer {anseo_token}",
                "Content-Type": "application/json",
            },
            timeout=15.0,
        )

        if resp.status_code == 201:
            data = resp.json()
            post_url = data.get("post_url", "")
            console.print(Panel(
                f"[bold green]Submitted & shared! 🎉[/bold green]\n\n"
                f"GitHub: {remote}\n"
                f"Anseo:  {post_url}\n\n"
                f"Your cohort can see your project now.\n"
                f"Don't forget to update your README with what you learned!",
                style="green"
            ))
        elif resp.status_code == 401:
            console.print("[red]Anseo token rejected.[/red]")
            console.print("[grey70]Check your ANSEO_API_TOKEN or generate a new one at Settings → API Tokens[/grey70]")
        elif resp.status_code == 400:
            data = resp.json()
            fields = data.get("fields", {})
            console.print("[red]Anseo rejected the submission:[/red]")
            for field, msg in fields.items():
                console.print(f"  [red]{field}:[/red] {msg}")
        else:
            console.print(f"[yellow]Anseo returned {resp.status_code}[/yellow]")
            try:
                console.print(f"[grey70]{resp.json().get('message', resp.text[:200])}[/grey70]")
            except Exception:
                console.print(f"[grey70]{resp.text[:200]}[/grey70]")

    except httpx.ConnectError:
        console.print("[yellow]Couldn't reach Anseo. Your code is pushed to GitHub.[/yellow]")
        console.print("[grey70]You can share manually on Anseo later.[/grey70]")
    except Exception as e:
        console.print(f"[yellow]Anseo sharing failed: {e}[/yellow]")
        console.print("[grey70]Your code is pushed to GitHub — share manually on Anseo.[/grey70]")


def _print_manual_share_hint(remote: str | None):
    """Show manual sharing instructions as fallback."""
    console.print(Panel(
        f"[bold green]Pushed to GitHub! 🎉[/bold green]\n\n"
        + (f"GitHub: {remote}\n\n" if remote else "")
        + "Share this link on Anseo in the course community.\n"
        "Don't forget to update your README with what you learned!",
        style="green"
    ))


if __name__ == "__main__":
    main()
