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

<div class="summary">
  <strong>Today at a glance</strong>
  <ul>
    <li>🔴 <strong>Urgent: Anthropic</strong> — investors gave the company $65 billion yesterday (<a href="https://www.bloomberg.com/news/articles/2026-05-28/anthropic-raises-at-965-billion-valuation-eclipsing-openai">Bloomberg</a>); 9 product design roles currently open across different teams</li>
    <li>🔴 <strong>Lyra Health</strong> — 5 active design roles open right now, spanning mid-level through Director</li>
    <li>🔵 <strong>Figma</strong> — AI design agent launched May 20 (<a href="https://www.fastcompany.com/91545179/figma-ai-agent-tool">Fast Company</a>); new AI-focused teams forming, roles likely coming</li>
    <li style="color:#555;">Companies with active UX postings today: <strong>Anthropic</strong>, <strong>Lyra Health</strong>, <strong>Figma</strong></li>
  </ul>
</div>

<!-- CURRENTLY HIRING -->
<h3><span class="tag tag-hiring">🔴 Currently Hiring</span></h3>

<p class="company-header">Anthropic</p>
<p class="meta">AI &nbsp;·&nbsp; San Francisco, hybrid (Seattle office available) &nbsp;·&nbsp; <a href="https://www.anthropic.com">anthropic.com</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/company/anthropicresearch">LinkedIn</a></p>
<ul>
  <li><strong>What they do:</strong> Anthropic builds Claude — the AI assistant you're using right now. One of the most valuable private companies in the world.</li>
  <li><strong>Why it's worth your attention:</strong>
    <ul>
      <li>Yesterday, investors gave Anthropic $65 billion to grow — the largest single fundraising round in AI history (<a href="https://www.bloomberg.com/news/articles/2026-05-28/anthropic-raises-at-965-billion-valuation-eclipsing-openai">Bloomberg</a>, <a href="https://www.axios.com/2026/05/28/anthropic-ai-fundraising-openai">Axios</a>). The company is now valued at nearly $1 trillion. Raises at this scale tend to unlock a burst of hiring within weeks.</li>
      <li>On April 17, Anthropic launched Claude Design — a product built for visual work: designs, prototypes, slides, one-pagers (<a href="https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/">TechCrunch</a>, <a href="https://www.anthropic.com/news/claude-design-anthropic-labs">Anthropic</a>).</li>
      <li>Workforce data shows 2 UX designers currently on staff — a very small team for a company at this scale.</li>
    </ul>
  </li>
</ul>
<div class="roles">
  <strong>Open role — confirmed Seattle or remote:</strong>
  <ul>
    <li><a href="https://job-boards.greenhouse.io/anthropic/jobs/5055448008">Product Designer, Claude Developer Platform</a> — San Francisco, New York, or Seattle (hybrid)</li>
  </ul>
  <strong>9 total product design roles are open.</strong> Location varies by role — only the above has been confirmed for Seattle. To see all of them:<br>
  &nbsp;→ <a href="https://www.glassdoor.com/Job/seattle-anthropic-jobs-SRCH_IL.0,7_IC1150505_KO8,17.htm">Glassdoor: Anthropic jobs in Seattle</a><br>
  &nbsp;→ <a href="https://job-boards.greenhouse.io/anthropic">Full Greenhouse board</a>
</div>
<p class="caveat">Most current postings are senior-level (8+ years). Mid-level roles are likely to follow — check the careers board weekly.</p>

<br>

<p class="company-header">Lyra Health</p>
<p class="meta">Healthcare / Mental Health &nbsp;·&nbsp; Remote &nbsp;·&nbsp; <a href="https://www.lyrahealth.com">lyrahealth.com</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/company/lyra-health">LinkedIn</a></p>
<ul>
  <li><strong>What they do:</strong> Lyra connects employees at large companies to mental health support — therapists, coaches, and self-guided tools. Their clients are employers; the product serves the people who use it.</li>
  <li><strong>Why it's worth your attention:</strong>
    <ul>
      <li>Five active design roles spanning every level at once — mid through Director — typically signals a team growing significantly, not just replacing one person.</li>
      <li>On January 27, 2026, Lyra launched an integrated care solution with Carrum Health, expanding into specialty care. New product surface often brings new design hires.</li>
    </ul>
  </li>
</ul>
<div class="roles">
  <strong>Open roles</strong> — verify current status on <a href="https://www.lyrahealth.com/careers/">Lyra's careers page</a> before applying:
  <ul>
    <li><a href="https://www.linkedin.com/jobs/view/product-designer-at-lyra-health-2352085135">Product Designer</a> — mid-level</li>
    <li><a href="https://jobs.lever.co/lyrahealth/1a7c1162-851d-4db6-aced-bf5292695b03">Senior Product Designer</a> — $133K–$183K</li>
    <li><a href="https://jobs.lever.co/lyrahealth/d15846a2-ca4c-483c-9c84-dce7f3a13591">Lead Product Designer</a> — $149K–$205K</li>
    <li><a href="https://jobs.lever.co/lyrahealth/402fd4f2-cd15-46e2-8b35-8da324c6952c">Staff UX Content Designer</a> — $134K–$205K</li>
    <li><a href="https://jobs.lever.co/lyrahealth/504eb97a-68ea-43f6-bc14-7657d231e52e">Director of Product Design</a> — $186K–$256K</li>
  </ul>
</div>
<p class="caveat">These links came from search results. The mid-level Product Designer link in particular may be an older posting — confirm it's still open before spending time on it.</p>

<!-- TEAM-LEVEL WATCH -->
<h3><span class="tag tag-team">🔵 Team-Level Watch</span></h3>

<p class="company-header">Figma — AI Products team</p>
<p class="meta">Design Tools &nbsp;·&nbsp; San Francisco, remote-friendly &nbsp;·&nbsp; <a href="https://www.figma.com">figma.com</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/company/figma">LinkedIn</a></p>
<ul>
  <li><strong>What they do:</strong> Figma is the design tool most professional designers use every day. They went public earlier this year, meaning the company now trades on the stock market.</li>
  <li><strong>Signal:</strong>
    <ul>
      <li>On May 20, Figma launched a native AI design agent — embedded in the canvas, it generates and edits designs using natural language prompts (<a href="https://www.fastcompany.com/91545179/figma-ai-agent-tool">Fast Company</a>). A new product requiring dedicated design support.</li>
      <li>On May 21, Figma announced partnerships with Anthropic and OpenAI to integrate AI tools including Claude Code into the platform (<a href="https://dataconomy.com/2026/05/21/figma-ai-design-agent-openai-anthropic-integrations/">Dataconomy</a>). Partnership work at this scale often expands team scope and headcount.</li>
    </ul>
  </li>
  <li><strong>The gap:</strong> Figma has 54 UX designers across many product teams. The AI agent is new enough that a dedicated design team for it may not be fully staffed yet.</li>
  <li><strong>Active postings</strong> (not specifically for AI product teams yet): <a href="https://job-boards.greenhouse.io/figma/jobs/5652044004">Product Designer</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/jobs/view/early-career-product-designer-2026-at-figma-4297189972">Early Career Product Designer</a></li>
  <li><strong>Likelihood: Moderate.</strong> The AI launches are real and very recent. Watch <a href="https://boards.greenhouse.io/figma">Figma's careers page</a> for postings that name the AI agent or Make product specifically.</li>
</ul>
<p class="caveat">Figma is now a public company — hiring decisions are tied to quarterly financial results. No departure signals were identified on these specific teams today.</p>

<!-- CLOSING -->
<div class="closing">
  Anthropic's nine open design roles is the most actionable thing in today's digest — worth going through the full list to find which team's work fits what you actually want to be doing. Lyra Health is worth acting on directly given the volume and the mission alignment. Tomorrow, running signals on the Seattle mid-size and mental health lists will give a fuller picture.
</div>

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
