"""
check_and_send.py — pulls the iroh repo and sends today's digest if one exists.
Scheduled via launchd to run at 7:30am daily. Safe to run multiple times —
skips silently if today's digest has already been sent.
"""

import sys
import subprocess
from datetime import date
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
DIGESTS_DIR = REPO_DIR / "digests"


def main():
    # Pull latest from GitHub so we get any digest the remote agent pushed
    result = subprocess.run(
        ["git", "pull", "--ff-only"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"git pull failed:\n{result.stderr}")
        sys.exit(1)
    print(result.stdout.strip() or "Already up to date.")

    today = date.today()
    date_str = today.strftime("%Y-%m-%d")
    digest_file = DIGESTS_DIR / f"{date_str}.html"
    sent_marker = DIGESTS_DIR / f"{date_str}.sent"

    if not digest_file.exists():
        print(f"No digest found for {date_str} — agent may not have run yet.")
        return

    if sent_marker.exists():
        print(f"Digest for {date_str} already sent, skipping.")
        return

    # Import send() from send_digest.py in the same scripts/ folder
    sys.path.insert(0, str(REPO_DIR / "scripts"))
    from send_digest import send, load_env

    env = load_env(REPO_DIR / ".env")
    subject = f"UX Hiring Signals — {today.strftime('%A, %B %-d')}"
    html_body = digest_file.read_text(encoding="utf-8")

    send(subject, html_body, env)

    # Mark as sent so re-runs don't double-send
    sent_marker.touch()
    print(f"Done — digest for {date_str} sent to {env['EMAIL_TO']}")


if __name__ == "__main__":
    main()
