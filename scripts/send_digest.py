"""
send_digest.py — sends the daily UX hiring signal digest email.
Usage: python3 send_digest.py --subject "..." --body-file digest.html
       python3 send_digest.py --test   (sends the test digest)
"""

import smtplib
import sys
import os
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"


def load_env(path):
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                env[key.strip()] = value.strip()
    return env


def send(subject, html_body, env):
    required = ["EMAIL_FROM", "EMAIL_TO", "EMAIL_PASSWORD", "SMTP_HOST", "SMTP_PORT"]
    missing = [k for k in required if not env.get(k)]
    if missing:
        print(f"ERROR: Missing required .env variables: {', '.join(missing)}")
        sys.exit(1)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = env["EMAIL_FROM"]
    msg["To"] = env["EMAIL_TO"]
    msg.attach(MIMEText(html_body, "html"))

    print(f"Connecting to {env['SMTP_HOST']}:{env['SMTP_PORT']}...")
    with smtplib.SMTP(env["SMTP_HOST"], int(env["SMTP_PORT"])) as server:
        server.ehlo()
        server.starttls()
        server.login(env["EMAIL_FROM"], env["EMAIL_PASSWORD"])
        server.sendmail(env["EMAIL_FROM"], env["EMAIL_TO"], msg.as_string())

    print(f"Sent: '{subject}' → {env['EMAIL_TO']}")


TEST_SUBJECT = "UX Hiring Signals — Friday, May 29"

TEST_BODY = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 680px; margin: 0 auto; padding: 24px; color: #1a1a1a; line-height: 1.6; }
  h2 { font-size: 18px; margin-top: 36px; margin-bottom: 4px; }
  h3 { font-size: 15px; font-weight: 600; margin-top: 28px; margin-bottom: 2px; border-top: 1px solid #e5e5e5; padding-top: 20px; }
  .summary { background: #f7f7f7; border-radius: 8px; padding: 16px 20px; margin-bottom: 28px; }
  .summary ul { margin: 8px 0 0 0; padding-left: 18px; }
  .summary li { margin-bottom: 6px; }
  .tag { display: inline-block; font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 4px; margin-right: 6px; }
  .tag-hiring { background: #fee2e2; color: #991b1b; }
  .tag-team { background: #dbeafe; color: #1e40af; }
  .company-header { font-size: 16px; font-weight: 700; }
  .meta { font-size: 13px; color: #555; margin-bottom: 12px; }
  ul { padding-left: 20px; }
  li { margin-bottom: 5px; }
  .roles { background: #f0fdf4; border-radius: 6px; padding: 12px 16px; margin: 10px 0; }
  .roles li { margin-bottom: 4px; }
  .caveat { color: #6b7280; font-size: 14px; font-style: italic; margin-top: 8px; }
  .closing { border-top: 1px solid #e5e5e5; margin-top: 32px; padding-top: 16px; color: #444; font-size: 14px; }
  a { color: #2563eb; }
</style>
</head>
<body>
<p style="font-size:13px;color:#888;margin-bottom:4px;">Friday, May 29 — Daily digest</p>
<h2 style="margin-top:0;">UX Hiring Signals</h2>
<p>This is a test email confirming SMTP delivery is working.</p>
</body>
</html>
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Send the test digest")
    parser.add_argument("--subject", help="Email subject")
    parser.add_argument("--body-file", help="Path to HTML file with email body")
    args = parser.parse_args()

    env = load_env(ENV_PATH)

    if args.test:
        send(TEST_SUBJECT, TEST_BODY, env)
    elif args.subject and args.body_file:
        with open(args.body_file) as f:
            body = f.read()
        send(args.subject, body, env)
    else:
        print("Usage: python3 send_digest.py --test")
        print("       python3 send_digest.py --subject '...' --body-file digest.html")
        sys.exit(1)
