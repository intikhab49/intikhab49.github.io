"""Builds intikhab49.github.io: one portfolio page plus the files search engines and AI crawlers read.

Project names, descriptions, topics and stars come from the GitHub API at build time, so the page
says what the repositories say. Only the grouping and the extra links (sites, packages,
Marketplace listings) are written here by hand.

Usage: python build.py            (needs `gh` signed in, or GITHUB_TOKEN for the API)
"""
import datetime as dt
import html
import json
import os
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
USER = "intikhab49"
SITE = f"https://{USER}.github.io/"
NAME = "Intikhab Azam"
URDU = "انتخاب اعظم"
TITLE = "Intikhab Azam · AI/ML Engineer, Researcher & Systems Architect"
DESC = ("AI/ML engineer and systems architect from Pakistan, working remotely with US teams: voice AI agents, "
        "RAG and LLM evaluation, multi-tenant SaaS, and open-source developer tools.")
X = "https://x.com/AzamIntikhab"
GH = f"https://github.com/{USER}"
MKT = "https://github.com/marketplace/actions/"
BING_VERIFY = "8696AEC33B172905558B45B0DB631DAD"

# (repo, extra links). Order inside a group is the order on the page.
GROUPS = [
    ("Developer tools and CI checks", "Catch the problem before it ships.", [
        ("fairfax", [("Website", f"{SITE}fairfax/"), ("PyPI", "https://pypi.org/project/fairfax/"),
                     ("GitHub Action", MKT + "fairfax-gov-cloud-check")]),
        ("blueprint-runtime", [("Website", f"{SITE}blueprint-runtime/"),
                               ("npm", "https://www.npmjs.com/package/blueprint-runtime")]),
        ("pgvector-cpu-check", [("Website", f"{SITE}pgvector-cpu-check/"), ("GitHub Action", MKT + "pgvector-cpu-check")]),
        ("diff-gate", [("GitHub Action", MKT + "diff-gate")]),
        ("lifeboat", [("GitHub Action", MKT + "postgresql-with-pgvector-and-postgis-lifeboat")]),
        ("minio-from-source", [("GitHub Action", MKT + "minio-from-source"),
                               ("Images", f"{GH}/minio-from-source/pkgs/container/minio-from-source")]),
    ]),
    ("AI research and benchmarks", "Measured, with the numbers that went against me left in.", [
        ("open-jev-typed-decision-engine", [("GitHub Action", MKT + "open-jev-typed-decisions")]),
        ("rag-cost-curve", []),
        ("pdf-cpu-bench", []),
        ("whofetched", []),
        ("pushback", [("PyPI", "https://pypi.org/project/pushback/")]),
        ("edgeproof-crypto-trading-backtest", []),
    ]),
    ("AI apps and automation", "Voice agents, RAG assistants, lead pipelines and ML APIs.", [
        ("vapi-voice-agent-crm", []), ("local-business-lead-finder", []), ("npi-healthcare-lead-pipeline", []),
        ("ai-wealth-advisor", []), ("secureface-liveness-detection", []), ("cryptoaion-price-prediction", []),
        ("crypto-price-prediction-api", []),
    ]),
    ("DevOps and full-stack", "Kubernetes, Docker, Flask, React and the tools around them.", [
        ("kubernetes-flask-microservices", []), ("kubernetes-flask-crud", []), ("flask-postgres-crud-dashboard", []),
        ("react-express-drizzle-crud", []), ("devops-agency-website", []), ("ubuntu-dev-tools-installer", []),
        ("libncurses5-libaio1-ubuntu-deb", []), ("git-notes", []), ("cpp-queue-data-structure", []),
    ]),
]

# Public repos left off the page: an older duplicate of edgeproof-crypto-trading-backtest.
SKIP = {USER, "crypto-15m-edge-research"}

# Painted cards from the profile README (assets/cards), shown as a gallery.
CARDS = [("open-jev-typed-decision-engine", "open-jev"), ("pushback", "pushback"), ("diff-gate", "diff-gate"),
         ("rag-cost-curve", "rag-cost-curve"), ("minio-from-source", "minio-from-source"),
         ("vapi-voice-agent-crm", "voice-agent-crm"), ("edgeproof-crypto-trading-backtest", "edgeproof"),
         ("local-business-lead-finder", "lead-finder")]

BUILD = [
    ("AI voice agents", "Vapi and Twilio receptionists and outbound callers, wired into CRMs, payments and SMS."),
    ("RAG and LLM agents", "Knowledge-base chatbots with tool calling and memory, evaluated by cost per correct answer."),
    ("LLM evals and research", "Calibration, benchmarks and backtests that report the losing numbers too."),
    ("Multi-tenant SaaS architecture", "Postgres row-level security, BFF auth, field-level encryption, event-driven jobs."),
    ("Agentic coding", "Claude Code, Codex and DeepSeek working in parallel behind spec files, a claims board and test gates."),
    ("Automation and data pipelines", "n8n, Cloudflare Workers, lead generation, scraping and enrichment."),
    ("Developer tools and CI checks", "CLIs, GitHub Actions and MCP servers on PyPI and npm, for Microsoft gov clouds "
     "(GCC High, Azure Government), Make.com, Postgres images and AI-written code."),
]
ARCH = [
    ("Multi-tenant SaaS", "shared schema with tenant keys, Postgres row-level security and cross-tenant tests in CI"),
    ("BFF authentication", "httpOnly cookie sessions with token refresh owned in one place"),
    ("Field-level encryption", "for sensitive personal data, with key rotation and idempotent backfills"),
    ("Event-driven pipelines", "webhooks, job queues, retries and idempotency keys"),
    ("Edge compute", "Cloudflare Workers for payment links, SMS and API glue between voice agents and Stripe"),
    ("LLM routing", "small models first, frontier models only when needed, prompt caching to cut token spend"),
    ("Delivery", "Docker, Kubernetes + NGINX, Prometheus, and end-to-end tests that run against real data"),
]
HIRE = [
    ("AI voice agents", "receptionists, outbound callers, call-to-CRM and payment flows on Vapi and Twilio"),
    ("RAG chatbots and LLM agents", "knowledge bases, tool calling, memory and evaluation"),
    ("LLM cost and quality", "benchmarks, calibration, prompt caching and model routing"),
    ("System architecture", "multi-tenant SaaS design, auth and data security, scaling and cost reviews"),
    ("Agentic coding setups", "Claude Code skills, MCP servers and CI gates for AI-written code"),
    ("Automation", "n8n workflows, lead generation, scraping, CRM and payment integrations"),
    ("Microsoft gov cloud", "GCC, GCC High and Azure Government feature, endpoint and sign-in checks before you build"),
    ("Make.com and no-code QA", "regression tests for Make scenarios that run offline and in CI"),
]
KNOWS = ["Voice AI agents", "Vapi", "Twilio", "Retrieval-augmented generation", "Agentic RAG", "LLM evaluation",
         "Model calibration", "Claude Code", "Model Context Protocol", "Multi-tenant SaaS", "PostgreSQL row-level security",
         "System architecture", "Machine learning", "PyTorch", "FastAPI", "NestJS", "n8n", "Cloudflare Workers",
         "Microsoft 365 GCC High", "Azure Government", "Make.com", "Docker", "Kubernetes", "GitHub Actions"]


def repos() -> dict:
    token = os.environ.get("GITHUB_TOKEN") or subprocess.run(["gh", "auth", "token"], capture_output=True,
                                                             text=True).stdout.strip()
    req = urllib.request.Request(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner",
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return {d["name"]: d for d in data if not d["fork"] and not d["private"] and not d["archived"]}


def e(s) -> str:
    return html.escape(str(s), quote=True)


def card(repo, extra) -> str:
    stars = f'<span class="stars" title="GitHub stars">★ {repo["stargazers_count"]}</span>' if repo["stargazers_count"] else ""
    links = [("GitHub", repo["html_url"])] + extra
    lang = f'<li class="lang">{e(repo["language"])}</li>' if repo.get("language") else ""
    tags = lang + "".join(f"<li>{e(t)}</li>" for t in repo.get("topics", [])[:6])
    anchors = " · ".join(f'<a href="{e(u)}">{e(t)}</a>' for t, u in links)
    return (f'<article class="proj"><h3><a href="{e(repo["html_url"])}">{e(repo["name"])}</a>{stars}</h3>'
            f'<p>{e(repo["description"] or "")}</p><ul class="tags">{tags}</ul><p class="links">{anchors}</p></article>')


def main():
    data = repos()
    listed = {name for _, _, items in GROUPS for name, _ in items}
    missing = sorted(n for n in data if n not in listed and n not in SKIP)
    if missing:
        raise SystemExit(f"public repos not placed in a group: {', '.join(missing)}")
    groups_html, item_list, llms, full = [], [], [], []
    for title, sub, items in GROUPS:
        cards = [card(data[n], extra) for n, extra in items if n in data]
        groups_html.append(f'<section class="group"><h3 class="gh">{e(title)}</h3><p class="sub">{e(sub)}</p>'
                           f'<div class="grid">{"".join(cards)}</div></section>')
        llms.append(f"\n## {title}\n")
        full.append(f"\n## {title}\n")
        for n, extra in items:
            if n not in data:
                continue
            r = data[n]
            more = (" Links: " + ", ".join(f"{t} {u}" for t, u in extra)) if extra else ""
            llms.append(f"- [{n}]({r['html_url']}): {r['description']}{more}")
            full.append(f"### {n}\n\n{r['description']}\n\n- Repository: {r['html_url']}" +
                        "".join(f"\n- {t}: {u}" for t, u in extra) +
                        (f"\n- Language: {r['language']}" if r.get("language") else "") +
                        (f"\n- Topics: {', '.join(r.get('topics', []))}" if r.get("topics") else "") +
                        (f"\n- Stars: {r['stargazers_count']}" if r["stargazers_count"] else "") + "\n")
            item_list.append({"@type": "SoftwareSourceCode", "name": n, "description": r["description"],
                              "codeRepository": r["html_url"], "url": (extra[0][1] if extra else r["html_url"]),
                              "programmingLanguage": r.get("language") or None, "author": {"@id": SITE + "#person"}})
    for x in item_list:
        if x["programmingLanguage"] is None:
            del x["programmingLanguage"]

    person = {"@type": "Person", "@id": SITE + "#person", "name": NAME, "alternateName": URDU,
              "jobTitle": "AI/ML Engineer, Researcher & Systems Architect", "description": DESC, "url": SITE,
              "image": SITE + "assets/og.png", "homeLocation": {"@type": "Country", "name": "Pakistan"},
              "sameAs": [GH, X], "knowsAbout": KNOWS}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfilePage", "@id": SITE, "url": SITE, "name": TITLE, "description": DESC,
         "inLanguage": "en", "dateModified": dt.date.today().isoformat(), "mainEntity": {"@id": SITE + "#person"}},
        person,
        {"@type": "ItemList", "name": f"Open-source projects by {NAME}",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": x} for i, x in enumerate(item_list)]}]}

    gallery = "".join(f'<a href="{GH}/{repo}"><img src="assets/cards/{art}.svg" width="640" height="400" loading="lazy" '
                      f'alt="{e(data[repo]["name"])}: {e(data[repo]["description"] or "")}"></a>'
                      for repo, art in CARDS if repo in data)
    li = lambda rows: "".join(f"<li><b>{e(a)}</b>: {e(b)}</li>" for a, b in rows)
    tools = sum(1 for _, _, items in GROUPS for n, _ in items if n in data)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<meta name="author" content="{NAME}">
<meta name="msvalidate.01" content="{BING_VERIFY}">
<link rel="canonical" href="{SITE}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="alternate" type="text/markdown" title="llms.txt" href="{SITE}llms.txt">
<meta property="og:type" content="profile">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}assets/og.png">
<meta property="og:image:width" content="1280"><meta property="og:image:height" content="640">
<meta property="profile:first_name" content="Intikhab"><meta property="profile:last_name" content="Azam">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@AzamIntikhab">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Ultra&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
:root{{--night:#0d0b16;--panel:#17132a;--cream:#f6e7c1;--paper:#fbf3dc;--red:#e0262b;--saffron:#ffb400;--gold:#f2c14e;
--green:#1fa34a;--teal:#16b3c4;--pink:#ff3e8a;--blue:#1f4fd8;--muted:#cbbf9f}}
*{{box-sizing:border-box}}
html{{background:var(--night)}}
body{{margin:0;color:var(--cream);font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--night)}}
a{{color:var(--saffron)}} a:hover{{color:var(--pink)}}
.wrap{{max-width:1120px;margin:0 auto;padding:0 16px}}
.hero img{{display:block;width:100%;height:auto}}
.tape{{height:10px;background:repeating-linear-gradient(90deg,var(--red) 0 28px,var(--paper) 28px 56px,var(--green) 56px 84px,var(--saffron) 84px 112px)}}
h1{{font-family:Ultra,Georgia,serif;font-weight:400;font-size:clamp(28px,4.6vw,48px);line-height:1.15;margin:28px 0 6px;color:var(--paper)}}
h1 .urdu{{display:block;font-family:"Noto Nastaliq Urdu","Jameel Noori Nastaleeq",serif;font-size:.6em;color:var(--gold);margin-top:6px}}
.role{{font-size:clamp(17px,2.2vw,21px);color:var(--gold);margin:0 0 14px;font-weight:600}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:0 0 18px;list-style:none}}
.chips li{{border:2px solid var(--saffron);border-radius:999px;padding:3px 12px;font-size:14px;font-weight:600}}
.chips li:nth-child(3n+2){{border-color:var(--pink)}} .chips li:nth-child(3n){{border-color:var(--teal)}}
.cta{{display:inline-block;background:var(--red);color:var(--paper);font-weight:700;padding:10px 18px;border-radius:8px;
text-decoration:none;border:3px solid var(--saffron);margin:4px 8px 4px 0}} .cta.alt{{background:transparent}}
.cta:hover{{color:var(--paper);background:var(--pink)}}
h2{{font-family:Ultra,Georgia,serif;font-weight:400;color:var(--saffron);font-size:clamp(24px,3.4vw,34px);margin:52px 0 12px}}
h2::after{{content:"";display:block;width:120px;height:6px;margin-top:8px;background:linear-gradient(90deg,var(--red),var(--saffron),var(--green),var(--teal))}}
ul.plain{{padding-left:20px}} ul.plain li{{margin:6px 0}} b{{color:var(--paper)}}
.group{{margin:30px 0}} .gh{{font-size:21px;margin:0;color:var(--paper)}} .sub{{margin:2px 0 14px;color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}}
.proj{{background:var(--panel);border:2px solid #2c2550;border-top:5px solid var(--saffron);border-radius:10px;padding:14px 16px;min-width:0}}
.group:nth-of-type(2) .proj{{border-top-color:var(--pink)}} .group:nth-of-type(3) .proj{{border-top-color:var(--teal)}}
.group:nth-of-type(4) .proj{{border-top-color:var(--green)}}
.proj h3{{margin:0 0 6px;font-size:18px;overflow-wrap:anywhere}} .proj h3 a{{color:var(--paper);text-decoration:none}}
.proj p{{margin:0 0 8px;font-size:15px}} .stars{{float:right;color:var(--gold);font-size:14px}}
.tags{{display:flex;flex-wrap:wrap;gap:6px;list-style:none;padding:0;margin:0 0 8px}}
.tags li{{font-size:12px;background:#241e40;border-radius:4px;padding:1px 7px;color:var(--muted)}} .tags li.lang{{color:var(--saffron)}}
.links{{font-size:14px;font-weight:600}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}
.gallery img{{display:block;width:100%;height:auto;border-radius:8px}}
footer{{margin:60px 0 0;padding:24px 0 40px;border-top:2px solid #2c2550;color:var(--muted);font-size:14px}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
</head>
<body>
<div class="tape"></div>
<header class="hero"><img src="assets/hero.svg" width="1280" height="914" alt="{NAME}, AI/ML engineer, researcher and systems architect, painted in Pakistani truck art: two peacocks, a vase of roses and his name in Urdu and English."></header>
<main class="wrap">
<h1>{NAME}<span class="urdu" lang="ur" dir="rtl">{URDU}</span></h1>
<p class="role">AI/ML Engineer, Researcher &amp; Systems Architect</p>
<ul class="chips"><li>Voice AI agents</li><li>RAG &amp; LLM evaluation</li><li>Multi-tenant SaaS</li><li>Agentic coding</li><li>Claude Code + MCP</li><li>Open-source developer tools</li></ul>
<p>I build AI systems that have to work in production: <b>voice agents</b> that answer real phone calls, <b>RAG and LLM agents</b> judged by cost per correct answer, and <b>multi-tenant SaaS platforms</b> with row-level security and field-level encryption. I also publish the research behind them, including the numbers that went against me, and open-source tools that catch problems before they ship: Microsoft gov-cloud gaps, broken Make.com scenarios, Postgres images that crash on older CPUs and packages an AI coding agent made up. Based in Pakistan, working with US teams, <b>open to contract work</b>.</p>
<p><a class="cta" href="{X}">Message me on X</a><a class="cta alt" href="{GH}">GitHub profile</a></p>

<h2 id="build">What I build</h2>
<ul class="plain">{li(BUILD)}</ul>

<h2 id="projects">Open-source projects</h2>
<p>{tools} public repositories, grouped by what they are for. Descriptions come straight from each repository.</p>
{"".join(groups_html)}

<h2 id="gallery">From the truck</h2>
<p>Every project card on my GitHub profile is hand-coded, animated SVG in the style of Pakistani truck art.</p>
<div class="gallery">{gallery}</div>

<h2 id="architecture">System architecture</h2>
<p>I design systems end to end, from the data model to the deploy pipeline. Patterns I use in production:</p>
<ul class="plain">{li(ARCH)}</ul>

<h2 id="hire">Work with me</h2>
<p>I take on <b>contract and freelance work</b>:</p>
<ul class="plain">{li(HIRE)}</ul>
<p><a class="cta" href="{X}">Message @AzamIntikhab on X</a></p>
</main>
<footer><div class="wrap">
<p>{NAME} ({URDU}) · <a href="{GH}">GitHub</a> · <a href="{X}">X</a> · <a href="llms.txt">llms.txt</a> · Updated {dt.date.today().isoformat()}</p>
<p>AI engineer · machine learning engineer · LLM engineer · AI researcher · systems architect · voice AI agent developer · RAG · LLM evaluation · Claude Code · MCP · multi-tenant SaaS · GCC High · Azure Government · Make.com · PostgreSQL · remote AI engineer in Pakistan</p>
<p><b>Dekh magar pyar se</b>: look, but with love.</p>
</div></footer>
</body>
</html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")

    head = (f"# {NAME}\n\n> {DESC}\n\n{NAME} ({URDU}) builds production AI systems (voice agents on Vapi and Twilio, "
            "RAG and LLM agents evaluated by cost per correct answer, multi-tenant SaaS) and publishes open-source "
            f"developer tools and research. Contact: {X} · Code: {GH}\n")
    sites = "\n## Project sites\n\n" + "\n".join(f"- [{n}]({SITE}{n}/): has its own llms.txt at {SITE}{n}/llms.txt"
                                                 for n in ("fairfax", "blueprint-runtime"))
    (ROOT / "llms.txt").write_text(head + "\n".join(llms) + "\n" + sites + "\n\n## Optional\n\n"
                                   f"- [Full project list with topics]({SITE}llms-full.txt)\n", encoding="utf-8", newline="\n")
    work = "\n## What I build\n\n" + "\n".join(f"- {a}: {b}" for a, b in BUILD) + \
           "\n\n## Work with me\n\n" + "\n".join(f"- {a}: {b}" for a, b in HIRE)
    (ROOT / "llms-full.txt").write_text(head + work + "\n" + "\n".join(full), encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n" + "".join(f"Sitemap: {SITE}{p}sitemap.xml\n"
                                               for p in ("", "fairfax/", "blueprint-runtime/", "pgvector-cpu-check/")),
        encoding="utf-8", newline="\n")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE}</loc><lastmod>{dt.date.today().isoformat()}</lastmod></url>\n</urlset>\n",
        encoding="utf-8", newline="\n")
    print(f"wrote index.html ({len(page)} chars, {tools} projects), llms.txt, llms-full.txt, robots.txt, sitemap.xml")


if __name__ == "__main__":
    main()
