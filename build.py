"""Builds intikhab49.github.io: the portfolio page plus the files search engines and AI crawlers read.

Copy lives in content.py, the look in site.css, the interactions in site.js. This script renders index.html
with every case study, project and stack card in the HTML itself, so crawlers see everything; site.js only
adds the motion, filters and tabs. Public repositories not featured on the page are listed under "Also on
GitHub", read from the GitHub API at build time.

Usage: python build.py            (needs `gh` signed in, or GITHUB_TOKEN for the API)
"""
import datetime as dt
import html
import json
import os
import subprocess
import urllib.request
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent
USER = "intikhab49"
SITE = f"https://{USER}.github.io/"
NAME = "Intikhab Azam"
TITLE = "Intikhab Azam · AI/ML Engineer, Researcher & Systems Architect"
DESC = ("AI/ML engineer and systems architect working remotely with US teams: production voice agents, multi-tenant "
        "platforms, RAG and LLM agents, automation and open-source developer tools.")
X = "https://x.com/AzamIntikhab"
GH = f"https://github.com/{USER}"
BING_VERIFY = "8696AEC33B172905558B45B0DB631DAD"
SKIP = {USER, f"{USER}.github.io"}
ROTATE_SECONDS = 10


def e(s) -> str:
    return html.escape(str(s), quote=True)


def repos() -> dict:
    token = os.environ.get("GITHUB_TOKEN") or subprocess.run(["gh", "auth", "token"], capture_output=True,
                                                             text=True).stdout.strip()
    req = urllib.request.Request(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner",
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return {d["name"]: d for d in data if not d["fork"] and not d["private"]}


def case_html(i, c):
    res = "".join(f"<li>{e(r)}</li>" for r in c["results"])
    tags = "".join(f"<span>{e(t)}</span>" for t in c["stack"])
    return (f'<article class="case"><div class="meta"><span class="k">{i:02d} · {e(c["sector"])}</span>'
            f'<span class="t">{e(c["kind"])}</span></div><h3>{e(c["title"])}</h3>'
            f'<div class="pb"><div><h4>THE PROBLEM</h4><p>{e(c["problem"])}</p></div>'
            f'<div><h4>WHAT I BUILT</h4><p>{e(c["built"])}</p></div></div>'
            f'<ul class="results">{res}</ul><div class="tags">{tags}</div></article>')


def project_html(p):
    rid, group, kind, lang, name, tags, line, proof, xl, xh = p
    text = " ".join([name, line, tags, kind]).lower()
    extra = f'<a href="{e(xh)}">{e(xl)} →</a>' if xh else ""
    return (f'<article class="proj" data-group="{group}" data-text="{e(text)}"><div class="meta"><span class="k">'
            f'{e(kind)}</span><span class="t">{e(lang)}</span></div><h3>{e(name)}</h3><p>{e(line)}</p>'
            f'<p class="proof">{e(proof)}</p><div class="links"><a href="{GH}/{rid}">GitHub →</a>{extra}</div></article>')


def stack_html():
    tabs, panels = [], []
    for i, (key, label, tools) in enumerate(C.STACK):
        tabs.append(f'<button class="tab" type="button" role="tab" id="tab-{key}" aria-controls="panel-{key}" '
                    f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
                    f'<span>{e(label)}</span><small>{len(tools)}</small></button>')
        cards = []
        for name, role, used in tools:
            mark = "".join(ch for ch in name if ch.isalpha())[:2].upper()
            cards.append(f'<article class="flip" tabindex="0" aria-label="{e(name)}, {e(role)}. Used in: {e(used)}">'
                         f'<div class="inner"><div class="face front" aria-hidden="true"><em>{e(mark)}</em><div>'
                         f'<strong>{e(name)}</strong><span>{e(role)}</span></div></div>'
                         f'<div class="face back" aria-hidden="true"><small>USED IN</small><span>{e(used)}</span></div>'
                         f'</div></article>')
        panels.append(f'<div class="panel" role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}">'
                      f'{"".join(cards)}</div>')
    return (f'<div class="stackwrap"><div class="tabs" role="tablist" aria-label="Stack categories" '
            f'aria-orientation="vertical">{"".join(tabs)}</div><div class="panels">{"".join(panels)}</div></div>')


def main():
    data = repos()
    featured = {p[0] for p in C.PROJECTS}
    missing = [p for p in featured if p not in data]
    if missing:
        raise SystemExit(f"featured projects not found as public repos: {missing}")
    also = sorted((n for n in data if n not in featured and n not in SKIP), key=lambda n: (data[n]["archived"], n))
    today = dt.date.today().isoformat()

    person = {"@type": "Person", "@id": SITE + "#person", "name": NAME, "alternateName": "انتخاب اعظم",
              "jobTitle": "AI/ML Engineer, Researcher & Systems Architect", "description": DESC, "url": SITE,
              "image": SITE + "assets/og.png", "sameAs": [GH, X], "knowsAbout": C.KNOWS,
              "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}}
                             for n, d in C.SERVICES]}
    items = [{"@type": "SoftwareSourceCode", "name": p[4], "description": p[6], "codeRepository": f"{GH}/{p[0]}",
              "url": p[9] or f"{GH}/{p[0]}", "programmingLanguage": p[3], "author": {"@id": SITE + "#person"}}
             for p in C.PROJECTS]
    cases = [{"@type": "CreativeWork", "name": c["title"], "about": c["kind"],
              "description": c["built"], "author": {"@id": SITE + "#person"}} for c in C.CASES]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ProfilePage", "@id": SITE, "url": SITE, "name": TITLE, "description": DESC, "inLanguage": "en",
         "dateModified": today, "mainEntity": {"@id": SITE + "#person"}},
        person,
        {"@type": "ItemList", "name": "Client work by " + NAME,
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": c} for i, c in enumerate(cases)]},
        {"@type": "ItemList", "name": "Open-source projects by " + NAME,
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": x} for i, x in enumerate(items)]}]}

    heads = "".join(f"<span>{e(h)}</span>" for h in C.HEADLINES)
    dots = "".join(f'<button type="button" aria-label="Show headline {i + 1} of {len(C.HEADLINES)}" '
                   f'aria-pressed="{"true" if i == 0 else "false"}"><i></i></button>' for i in range(len(C.HEADLINES)))
    glance = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in C.GLANCE)
    marquee = " · ".join(C.MARQUEE * 2) + " · "
    cases_html = "".join(case_html(i + 1, c) for i, c in enumerate(C.CASES))
    chips = "".join(f'<button class="chip" type="button" data-group="{k}" aria-pressed="{"true" if k == "all" else "false"}">'
                    f'{e(v)}</button>' for k, v in C.FILTERS)
    projects = "".join(project_html(p) for p in C.PROJECTS)
    also_html = " · ".join(f'<a href="{GH}/{n}">{e(n)}</a>' for n in also)
    steps = "".join(f"<li><b>{i + 1:02d}</b><h3>{e(t)}</h3><p>{e(b)}</p></li>" for i, (t, b) in enumerate(C.STEPS))
    services = "".join(f"<div><b>{i + 1:02d}</b><div><h3>{e(t)}</h3><p>{e(b)}</p></div></div>"
                       for i, (t, b) in enumerate(C.SERVICES))

    page = f"""<!doctype html>
<html lang="en" class="no-js" style="--secs:{ROTATE_SECONDS}s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<meta name="author" content="{NAME}">
<meta name="theme-color" content="#0b0c0e">
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
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header class="wrap top">
  <a class="brand" href="#top"><b>IA</b><span>Intikhab Azam</span></a>
  <nav class="nav" aria-label="Main"><a href="#clients">Client work</a><a href="#open-source">Open source</a><a href="#process">How I work</a><a href="#stack">Stack</a><a href="#services">Services</a><a class="hire" href="#contact">Hire me</a></nav>
</header>
<main id="top">
<section class="wrap hero" aria-labelledby="hero-title">
  <div class="hero-text">
    <p class="avail rise"><span class="dot"></span>Open to contract work · remote with US teams</p>
    <div class="rotor-area rise2">
      <h1 id="hero-title"><span class="sr">Intikhab Azam, AI/ML engineer building voice agents, multi-tenant platforms, RAG and LLM agents, automation and open-source tools.</span><span class="heads" aria-hidden="true">{heads}</span></h1>
      <div class="rotor"><div class="dots" role="group" aria-label="Headlines">{dots}</div><div class="bar" aria-hidden="true"><i></i></div><button class="pause" type="button">Pause</button></div>
    </div>
    <p class="lede rise3">Intikhab Azam, AI/ML engineer, researcher and systems architect. Production voice agents, multi-tenant platforms, RAG and LLM agents, automation for teams, and open-source tools that catch problems before they ship.</p>
    <div class="ctas rise3"><a class="btn" href="#clients">See client work</a><a class="btn ghost" href="{X}">Message on X</a></div>
  </div>
  <div class="stage"><canvas id="knot" role="img" aria-label="An interactive wireframe knot in three dimensions. Drag to rotate it."></canvas><p>drag to rotate</p></div>
</section>
<section class="glance" aria-label="At a glance">
  <div class="wrap glance-grid">{glance}</div>
  <div class="marquee" aria-hidden="true"><div>{e(marquee)}</div></div>
</section>
<section id="clients" class="wrap block" aria-labelledby="clients-title">
  <p class="label">01 · Client work</p>
  <div class="sec-head"><h2 id="clients-title" class="sec" style="max-width:760px">Systems running for real businesses.</h2><p class="note">Client names are left out on purpose. Every result below is one I can show in a call.</p></div>
  <div class="cases">{cases_html}</div>
</section>
<section id="open-source" class="wrap block" aria-labelledby="oss-title">
  <p class="label">02 · Open source and research</p>
  <h2 id="oss-title" class="sec">Public work, with the numbers left in.</h2>
  <div class="controls"><div class="chips" role="group" aria-label="Filter projects">{chips}</div>
    <div class="search"><label for="q">SEARCH PROJECTS</label><input id="q" type="search" placeholder="Postgres, RAG, Make.com…" autocomplete="off"></div></div>
  <p class="count" aria-live="polite">{len(C.PROJECTS)} of {len(C.PROJECTS)} projects</p>
  <div class="projects">{projects}</div>
  <p class="empty" hidden>Nothing matches that search. Try a tool name like Postgres, Claude or Stripe.</p>
  <p class="also">Also on GitHub: {also_html}</p>
</section>
<section id="process" class="wrap block" aria-labelledby="process-title">
  <p class="label">03 · How I work</p>
  <h2 id="process-title" class="sec">Fast because it's checked.</h2>
  <ol class="steps">{steps}</ol>
</section>
<section id="stack" class="wrap block" aria-labelledby="stack-title">
  <p class="label">04 · Stack</p>
  <div class="sec-head"><h2 id="stack-title" class="sec">The stack, and where it shipped.</h2><p class="note">Hover or tab to a tool to flip it and see the work it was used in.</p></div>
  {stack_html()}
</section>
<section id="services" class="wrap block" aria-labelledby="services-title">
  <p class="label">05 · Services</p>
  <h2 id="services-title" class="sec">Work I take on.</h2>
  <div class="services">{services}</div>
</section>
<section id="contact" class="wrap contact" aria-labelledby="contact-title">
  <div class="contact-box">
    <div style="flex:1 1 480px;min-width:0"><p class="label">06 · Contact</p><h2 id="contact-title">Have an AI system that has to work on day one?</h2><p class="big">Voice agents, multi-tenant platforms, RAG and LLM evals, automation and developer tools. Contract and freelance, remote with US teams.</p></div>
    <div class="contact-links"><a href="{X}">Message @AzamIntikhab <span aria-hidden="true">→</span></a><a class="ghost" href="{GH}">github.com/{USER} <span aria-hidden="true">→</span></a></div>
  </div>
</section>
</main>
<footer class="wrap"><span>Intikhab Azam · AI/ML engineer, researcher and systems architect · updated {today}</span><span class="mono">Client names withheld · every figure checkable · <a href="llms.txt">llms.txt</a></span></footer>
<script src="site.js" defer></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")

    head = (f"# {NAME}\n\n> {DESC}\n\nContact: {X} · Code: {GH} · Site: {SITE}\n")
    case_lines = "\n".join(f"- {c['title']} ({c['sector']}, {c['kind']}): {c['built']} Results: "
                           + "; ".join(c["results"]) + "." for c in C.CASES)
    proj_lines = "\n".join(f"- [{p[4]}]({GH}/{p[0]}): {p[6]} Proof: {p[7]}." + (f" {p[8]}: {p[9]}" if p[9] else "")
                           for p in C.PROJECTS)
    also_lines = "\n".join(f"- [{n}]({GH}/{n}){' (archived early project)' if data[n]['archived'] else ''}: "
                           f"{data[n]['description'] or ''}" for n in also)
    services_lines = "\n".join(f"- {t}: {b}" for t, b in C.SERVICES)
    stack_lines = "\n".join(f"- {label}: " + ", ".join(f"{n} ({u})" for n, _, u in tools) for _, label, tools in C.STACK)
    llms = (head + "\n## Client work (anonymized)\n\n" + case_lines + "\n\n## Open-source projects\n\n" + proj_lines
            + "\n\n## Services\n\n" + services_lines + "\n\n## Optional\n\n"
            + f"- [Full profile, stack and every public repository]({SITE}llms-full.txt)\n")
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8", newline="\n")
    full = (head + "\n## Client work (anonymized)\n\n" + case_lines + "\n\n## Open-source projects\n\n" + proj_lines
            + "\n\n## Also on GitHub\n\n" + also_lines + "\n\n## How I work\n\n"
            + "\n".join(f"{i + 1}. {t}: {b}" for i, (t, b) in enumerate(C.STEPS))
            + "\n\n## Stack, and where each tool was used\n\n" + stack_lines + "\n\n## Services\n\n" + services_lines + "\n")
    (ROOT / "llms-full.txt").write_text(full, encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n" + "".join(f"Sitemap: {SITE}{p}sitemap.xml\n"
                                               for p in ("", "fairfax/", "blueprint-runtime/", "pgvector-cpu-check/")),
        encoding="utf-8", newline="\n")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{SITE}</loc><lastmod>{today}</lastmod></url>\n</urlset>\n", encoding="utf-8", newline="\n")
    print(f"wrote index.html ({len(page) // 1024} KB: {len(C.CASES)} case studies, {len(C.PROJECTS)} projects, "
          f"{len(also)} more on GitHub), llms.txt, llms-full.txt, robots.txt, sitemap.xml")


if __name__ == "__main__":
    main()
