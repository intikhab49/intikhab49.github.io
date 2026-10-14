"""Everything the site says. Client work is anonymized on purpose: no client names, product names or personal
details. Every result here is one that can be shown in a call; problems are stated as the job, never invented."""

HEADLINES = [
    "I build AI that answers the phone, reads the data and ships.",
    "Voice agents that take real calls, tested before every change.",
    "Multi-tenant platforms that keep every client’s data apart.",
    "RAG and LLM agents, judged by cost per correct answer.",
    "Automation that turns 200 Slack channels into one board.",
    "Open-source tools that catch problems before they ship.",
]

GLANCE = [("6", "client systems shown below"), ("20+", "open-source repositories"),
          ("6", "tools on the GitHub Marketplace"), ("148", "API endpoints in one client platform")]

MARQUEE = ["Vapi", "Twilio", "Stripe", "Cloudflare Workers", "NestJS", "Prisma", "PostgreSQL", "Next.js", "Claude",
           "MCP", "PyTorch", "FastAPI", "n8n", "Docker", "Kubernetes", "Playwright"]

CASES = [
    dict(sector="US mobility company", kind="Voice AI", title="Three production voice agents on the phone lines",
         problem="Answer inbound calls, run outbound follow-ups and recover failed payments by phone, with the same "
                 "quality on every call.",
         built="An inbound receptionist, an outbound caller and a payment-recovery agent on Vapi. Payment links and "
               "SMS go through a Cloudflare Worker to Stripe; returning callers are recognized by caller ID.",
         results=["Every prompt change is tested with scripted call batteries before it is pushed (30 of 30 on one "
                  "branching flow)", "Dev and production organizations kept separate, with a promote step between them"],
         stack=["Vapi", "Twilio", "Stripe", "Cloudflare Workers"]),
    dict(sector="Provider network", kind="Multi-tenant SaaS", title="A multi-tenant platform for sensitive personal data",
         problem="Many provider organizations needed one platform without ever seeing each other’s records.",
         built="A NestJS and Prisma API on PostgreSQL with tenant isolation on every row, roles checked per endpoint, "
               "and a Next.js portal whose sessions stay in httpOnly cookies behind a backend-for-frontend.",
         results=["148 API endpoints across 26 areas, each with its roles documented",
                  "A Playwright end-to-end suite runs on every pull request",
                  "Built with a coordinated team of AI coding agents and a human developer, behind spec files and test gates"],
         stack=["NestJS", "Prisma", "PostgreSQL", "Next.js", "Docker", "Playwright"]),
    dict(sector="Agency executive", kind="AI automation", title="Slack triage for someone in 200+ channels",
         problem="Approvals and blockers were getting lost across more than 200 Slack channels.",
         built="A triage system that reads the day’s Slack and files what matters as cards on a Notion board: a "
               "keyword matrix, a Notion schema and a triage prompt checked by hand on 11 of 11 test cases.",
         results=["Runs on a daily schedule",
                  "No new access to the client’s systems: it works through the connectors they already had"],
         stack=["Claude", "Slack", "Notion"]),
    dict(sector="Billing-services company", kind="Website", title="A company website with motion that means something",
         problem="A new company site that feels established, plus a way for the team to update it themselves.",
         built="Designed and built the site on Cloudflare Pages with four motion systems, and built a contact form "
               "backend and a CMS for the team.",
         results=["Live on Cloudflare Pages", "Mobile spacing and overflow fixed across the whole site"],
         stack=["Cloudflare Pages", "Resend", "Sveltia CMS"]),
    dict(sector="Sales team", kind="Lead generation", title="A lead engine past the Google Places limit",
         problem="Google Places stops at 60 results per search, so whole areas of local businesses never showed up.",
         built="A self-hosted engine that grid-searches an area, falls back to OpenStreetMap, finds websites and "
               "emails, removes duplicates and resumes after a stop.",
         results=["Built for a client’s outbound sales team", "An open-source version is on GitHub"],
         stack=["Python", "FastAPI", "Streamlit", "Google Places"]),
    dict(sector="Dental practice", kind="Voice AI", title="An AI receptionist for a dental practice",
         problem="Let the owner hear exactly how an AI receptionist would handle their calls before committing to one.",
         built="A voice receptionist on Vapi that greets callers, answers common questions and hands off to the team, "
               "set up as a working demo for the owner.",
         results=["Tested on live phone calls before it was shown"],
         stack=["Vapi", "Prompt design"]),
]

SITE = "https://intikhab49.github.io/"
# id (repo), group, kind, language, display name, search tags, line, proof, extra link label, extra link
PROJECTS = [
    ("fairfax", "tools", "Gov cloud", "Python", "fairfax", "microsoft azure gcc high government mcp github action pypi",
     "Is it available in GCC High? Checks a Microsoft 365 GCC, GCC High or DoD and Azure Government plan against "
     "Microsoft’s own tables, and finds commercial endpoints in code.",
     "633 features, every row cited · weekly re-check with Wayback copies", "Website", SITE + "fairfax/"),
    ("starsift", "tools", "Security", "Python", "starsift", "github stars fake stars star farm stargazers gh archive pypi",
     "Are a repo’s GitHub stars real? Compares the accounts behind them with random accounts from the same hours, "
     "now that GitHub hides who starred.",
     "21 of 25 suspected fake-star repos flagged, 0 of 25 others · on PyPI", "PyPI", "https://pypi.org/project/starsift/"),
    ("blueprint-runtime", "tools", "Automation", "TypeScript", "blueprint-runtime", "make.com integromat no-code testing ci npm",
     "Test Make.com scenarios offline. Replays real Make runs locally so a broken mapping fails in CI, not in production.",
     "71 of 79 real runs reproduced exactly, 0 differ", "Website", SITE + "blueprint-runtime/"),
    ("pgvector-cpu-check", "tools", "Infrastructure", "Python", "pgvector-cpu-check", "postgres postgresql docker cpu sigill qemu github action",
     "Which CPU crashes your Postgres image? Runs it on 7 CPU models and names the faulting instruction behind SIGILL.",
     "13 popular images audited · 3 build bugs found", "Website", SITE + "pgvector-cpu-check/"),
    ("lifeboat", "tools", "Containers", "Shell", "lifeboat", "postgres postgresql bitnami helm kubernetes docker",
     "Bitnami’s PostgreSQL and PostgreSQL HA images, rebuilt from upstream source as drop-ins for the Bitnami Helm charts.",
     "every source SHA-256 pinned · amd64 and arm64", "", ""),
    ("diff-gate", "tools", "Security", "JavaScript", "diff-gate", "claude code ai agents security supply chain github action",
     "Fails a coding agent’s diff when an import resolves to nothing, before attackers register the name.",
     "Claude Code skill and GitHub Action · zero dependencies", "", ""),
    ("minio-from-source", "tools", "Containers", "Shell", "minio-from-source", "minio docker s3 object storage ghcr",
     "A free MinIO server and mc image built from source at pinned, commit-verified releases, for amd64 and arm64.",
     "smoke-tested · on the GitHub Marketplace", "", ""),
    ("pushback", "tools", "Developer tools", "Python", "pushback", "claude code agents claude.md pypi",
     "How often do you correct your coding agent? Measures it from Claude Code transcripts and drafts CLAUDE.md rules.",
     "on PyPI · tests in CI", "PyPI", "https://pypi.org/project/pushback/"),
    ("open-jev-typed-decision-engine", "research", "Research", "Python", "Open Jev", "machine learning model calibration onnx colab",
     "An open 150M typed decision engine: label, choice and score in one pass, with calibrated confidence.",
     "0.697 vs 0.727 accuracy · 2.5x better calibrated · 4x faster", "", ""),
    ("rag-cost-curve", "research", "Research", "Python", "rag-cost-curve", "rag llm agents benchmark claude cost",
     "What agentic RAG really costs: cost per correct answer for four RAG designs on multi-hop questions.",
     "+32.5 exact match at 2.5x the cost per correct answer", "", ""),
    ("pdf-cpu-bench", "research", "Benchmark", "Python", "pdf-cpu-bench", "pdf rag ocr parsing benchmark cpu",
     "The best PDF-to-Markdown parser for RAG without a GPU: accuracy, seconds per page, peak RAM and install size.",
     "9 parsers · 1,403 PDFs · MinerU CPU tier leads at 74.6%", "", ""),
    ("whofetched", "research", "Investigation", "JavaScript", "whofetched", "ai crawlers chatgpt claude gemini cloudflare seo",
     "Which AI actually read your page? Canary links and a Cloudflare Worker log, tested on six AI apps.",
     "every log in the repo, timestamped", "", ""),
    ("edgeproof-crypto-trading-backtest", "research", "Quant research", "Python", "EdgeProof", "machine learning trading backtest lightgbm lstm crypto",
     "Crypto strategy backtesting and ML validation: triple-barrier labels, purged k-fold CV, deflated Sharpe and a "
     "positive control.", "reports the honest result: no edge after fees", "", ""),
    ("vapi-voice-agent-crm", "apps", "Voice AI", "Node.js", "vapi-voice-agent-crm", "vapi voice agents twilio stripe crm",
     "Call ops for AI voice agents: webhook ingestion, a predictive dialer, auto-redial and Stripe-verified conversions.",
     "Vapi · Twilio · Stripe · Express", "", ""),
    ("local-business-lead-finder", "apps", "Automation", "Python", "local-business-lead-finder", "leads scraping google places openstreetmap fastapi streamlit",
     "Self-hosted lead generation past the Google Places 60-result cap, with an OpenStreetMap fallback and resumable runs.",
     "FastAPI · Streamlit · grid search · dedup", "", ""),
    ("npi-healthcare-lead-pipeline", "apps", "Data pipeline", "Python", "npi-lead-pipeline", "data pipeline github actions scraping leads",
     "Provider directory to practice websites to emails, resumable and scheduled on GitHub Actions, with zero paid APIs.",
     "runs on a schedule in GitHub Actions", "", ""),
    ("ai-wealth-advisor", "apps", "RAG agent", "Python", "ai-wealth-advisor", "rag llm agent tool calling langchain chromadb",
     "A RAG and tool-calling financial assistant for portfolio risk: VaR, Sharpe, drawdown and diversification scoring.",
     "LangChain · ChromaDB memory · Flask", "", ""),
    ("secureface-liveness-detection", "apps", "Computer vision", "Python", "secureface", "computer vision face recognition liveness opencv",
     "Face recognition access control with head-pose liveness, rPPG pulse detection and vector matching.",
     "InsightFace · OpenCV · ChromaDB", "", ""),
    ("cryptoaion-price-prediction", "apps", "ML API", "Python", "cryptoaion", "machine learning pytorch lstm fastapi api",
     "A BiLSTM-with-attention price prediction API with WebSocket streaming and JWT auth.",
     "PyTorch · FastAPI · WebSockets", "", ""),
]
FILTERS = [("all", "All"), ("tools", "Developer tools"), ("research", "Research"), ("apps", "AI apps")]

STEPS = [
    ("Scope it in writing", "A short spec with the acceptance checks agreed before any code, so “done” "
     "means the same thing to both of us."),
    ("Build in parallel", "AI coding agents and people work behind the spec, a claims board and test gates, so "
     "speed does not cost correctness."),
    ("Prove the behavior", "Scripted call batteries for voice agents, end-to-end suites for apps, benchmarks for "
     "models. Results go in writing."),
    ("Ship and hand over", "Deployed, documented and monitored, with the numbers that went against us reported too."),
]

STACK = [
    ("ai", "AI and LLMs", [
        ("Claude", "LLM", "rag-cost-curve, the Slack triage system, pushback"),
        ("Claude Code", "Coding agent", "the multi-tenant platform build, diff-gate, pushback"),
        ("MCP", "Agent protocol", "fairfax, which runs as an MCP server for coding agents"),
        ("Codex", "Coding agent", "the multi-tenant platform build, as part of the agent team"),
        ("DeepSeek", "Coding agent", "the multi-tenant platform build, as part of the agent team"),
        ("Gemini", "LLM", "ai-wealth-advisor"),
        ("OpenRouter", "LLM gateway", "ai-wealth-advisor"),
        ("LangChain", "LLM framework", "ai-wealth-advisor"),
        ("Hugging Face", "Models", "Open Jev, the open typed decision engine")]),
    ("voice", "Voice", [
        ("Vapi", "Voice agents", "voice agents for a mobility company, a dental practice receptionist, vapi-voice-agent-crm"),
        ("Twilio", "Telephony", "voice agents for a mobility company, vapi-voice-agent-crm"),
        ("Stripe", "Payments", "payment-recovery calls with SMS payment links, vapi-voice-agent-crm"),
        ("ElevenLabs", "Voices", "part of my voice-agent stack"),
        ("Deepgram", "Speech to text", "part of my voice-agent stack"),
        ("Retell AI", "Voice agents", "part of my voice-agent stack")]),
    ("ml", "Machine learning", [
        ("PyTorch", "Deep learning", "Open Jev, cryptoaion"),
        ("LightGBM", "Gradient boosting", "EdgeProof backtesting"),
        ("XGBoost", "Gradient boosting", "the first crypto prediction API"),
        ("ONNX", "Model export", "Open Jev"),
        ("OpenCV", "Computer vision", "secureface liveness detection"),
        ("scikit-learn", "Classic ML", "part of my ML stack"),
        ("pandas", "Data", "EdgeProof, the data pipelines"),
        ("NumPy", "Numerics", "every Python research project")]),
    ("backend", "Backend", [
        ("NestJS", "API framework", "the multi-tenant platform, 148 endpoints"),
        ("Prisma", "ORM", "the multi-tenant platform"),
        ("PostgreSQL", "Database", "the multi-tenant platform, lifeboat, pgvector-cpu-check"),
        ("FastAPI", "API framework", "the lead engine, cryptoaion"),
        ("Node.js", "Runtime", "vapi-voice-agent-crm, blueprint-runtime"),
        ("Express", "API framework", "vapi-voice-agent-crm"),
        ("Python", "Language", "fairfax, pdf-cpu-bench, rag-cost-curve and more"),
        ("TypeScript", "Language", "blueprint-runtime, the multi-tenant platform")]),
    ("frontend", "Frontend", [
        ("Next.js", "Web framework", "the multi-tenant platform portal"),
        ("React", "UI", "the multi-tenant platform portal"),
        ("Streamlit", "Data apps", "the lead engine, secureface"),
        ("Tailwind CSS", "Styling", "part of my frontend stack"),
        ("Astro", "Sites", "part of my frontend stack"),
        ("Vite", "Build tool", "part of my frontend stack")]),
    ("infra", "Infra and automation", [
        ("Docker", "Containers", "the multi-tenant platform, lifeboat, minio-from-source"),
        ("Kubernetes", "Orchestration", "lifeboat for the Bitnami Helm charts, kubernetes-flask-microservices"),
        ("GitHub Actions", "CI", "fairfax, pgvector-cpu-check, diff-gate, the lead pipeline schedule"),
        ("Cloudflare Workers", "Edge compute", "the payment-link and SMS pipeline, whofetched"),
        ("Cloudflare Pages", "Hosting", "the billing-services company website"),
        ("Playwright", "E2E tests", "the multi-tenant platform, on every pull request"),
        ("Slack + Notion", "Workflow", "the Slack triage system"),
        ("QEMU", "CPU emulation", "pgvector-cpu-check, 7 CPU models"),
        ("ClickHouse", "Analytics SQL", "starsift, which samples a public archive of 11 billion GitHub events")]),
]

SERVICES = [
    ("AI voice agents", "Vapi and Twilio receptionists and outbound callers, wired into CRMs, payments and SMS."),
    ("Multi-tenant SaaS architecture", "Postgres row-level security, BFF auth, field-level encryption, event-driven jobs."),
    ("RAG and LLM agents", "Knowledge-base chatbots with tool calling and memory, judged by cost per correct answer."),
    ("LLM evals and research", "Calibration, benchmarks and backtests that report the losing numbers too."),
    ("Agentic coding setups", "Claude Code skills, MCP servers and CI gates for AI-written code."),
    ("Automation and data pipelines", "n8n, Cloudflare Workers, Slack and Notion, lead generation and enrichment."),
    ("Developer tools and CI checks", "CLIs, GitHub Actions and MCP servers for gov clouds, Make.com, Postgres images and more."),
]

KNOWS = ["Voice AI agents", "Vapi", "Twilio", "Retrieval-augmented generation", "Agentic RAG", "LLM evaluation",
         "Model calibration", "Claude Code", "Model Context Protocol", "Multi-tenant SaaS", "PostgreSQL row-level security",
         "System architecture", "Machine learning", "PyTorch", "FastAPI", "NestJS", "Next.js", "n8n",
         "Cloudflare Workers", "Microsoft 365 GCC High", "Azure Government", "Make.com", "Docker", "Kubernetes",
         "GitHub Actions"]
