# TLIM — Tibia Loot & Inventory Manager
### Stage 1: Python / FastAPI / SQLite

![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)

> The first stage of a three-stage portfolio project. Stage 2 rebuilds this as a production-grade REST API in [Java / Spring Boot / PostgreSQL](https://github.com/calgadev/tlim-java). A React frontend is planned for Stage 3.

---

## What is TLIM?

TLIM is a personal portfolio project built to solve real problems faced by players of the MMORPG [Tibia](https://www.tibia.com):

- **What should I do with my loot after a hunt?** Keep it, sell to an NPC, or list on the market?
- **Where should I grind?** Which hunting spots actually generate the most value over time?

Stage 1 proves the concept with a working MVP: a server-side rendered web application that classifies loot, calculates passive gold, and stores hunt history per character for future comparison.

---

## Project Roadmap

| Stage | Stack | Repository | Status |
|---|---|---|---|
| Stage 1 — Backend + Server-side UI | Python 3.12 · FastAPI · SQLAlchemy 2.0 · SQLite · Jinja2 | tlim-python2 | ✅ Complete |
| Stage 2 — Backend rewrite | Java 17 · Spring Boot · Spring Data JPA · PostgreSQL · Maven | tlim-java | ✅ Complete |
| Stage 3 — Modern frontend | React · JavaScript ES6+ · React Router · Axios | tlim-frontend (coming soon) | 🚧 In Progress |

The project is intentionally developed in three stages with different stacks to demonstrate that the same problem can be solved across different languages and technologies — showing transferable knowledge rather than familiarity with a single tool.

---

## How this project was built

Stage 1 was developed using a three-prompt AI-assisted methodology: a **Research** prompt to explore the problem domain and existing codebase before writing any code, a **Spec** prompt to produce a detailed implementation plan file-by-file before touching the editor, and a **Code** prompt to implement exactly what the Spec described — no more, no less.

The AI was instructed never to make decisions unilaterally: every ambiguity was surfaced as a question and resolved before proceeding. To keep context small and avoid hallucination, the workflow was executed feature-by-feature — each feature got its own Research → Spec → Code cycle in a fresh session.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy 2.0 |
| Templates | Jinja2 |
| Validation | Pydantic |
| Server | Uvicorn |
| UI | Bootstrap 5 |

---

## Architecture

```
tlim-python2/
├── main.py              ← FastAPI app entry point
├── database.py          ← SQLAlchemy + SQLite configuration
├── seed.py              ← Populates the database with initial data
├── models/              ← Database tables via SQLAlchemy ORM
├── schemas/             ← Input/output validation via Pydantic
├── routers/             ← HTTP endpoints (no business logic)
├── services/            ← Business logic (sale decision, hunt import)
├── parsers/             ← Hunt Analyser text and JSON parsers
├── templates/           ← Jinja2 HTML templates
├── static/              ← CSS
└── seed_data/           ← JSON files with initial servers, items and creatures
```

---

## Key Technical Decisions

**Market price at server level** — shared across all characters on the same server, avoiding duplicate registration.

**`npc_buyable` as explicit boolean** — avoids the ambiguity of using `npc_price = 0` as a sentinel value. A price of zero and the absence of a price are meaningfully different states.

**Atomic hunt import** — all or nothing: if any item or creature in the log is missing from the database, nothing is persisted. This keeps hunt records consistent and trustworthy.

**`balance` not stored** — calculated at display time as `loot_total - supplies`, since both values are immutable after import. Storing the difference would be redundant.

**Sale decision engine** — four possible outcomes per item: Keep, Sell to NPC, Sell on market, No price available.

---

## Prerequisites

- Python 3.12+

---

## Configuration

Stage 1 uses SQLite with no external database server. No environment variables or credentials are required — the database file is created automatically when `seed.py` is run for the first time.

---

## Running Locally

```bash
# Clone the repository
git clone https://github.com/calgadev/tlim-python2.git
cd tlim-python2

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Populate the database with initial data (servers, items, creatures)
python seed.py

# Start the development server
uvicorn main:app --reload
```

Access at `http://127.0.0.1:8000`

> **Note:** Running `python seed.py` is required before using the application. It creates the database and populates it with 30 servers, 20 items and 20 creatures.

---

## UI Navigation

Stage 1 is a server-side rendered application — there is no REST API or Swagger UI. All functionality is accessible through the web interface:

| Page | Path | Description |
|---|---|---|
| User selection | `/` | Select or create a user |
| Characters | `/characters` | Register and list characters |
| Hunt import | `/hunt/import` | Paste text or upload JSON from the Hunt Analyser |
| Hunt history | `/hunt/history` | View past sessions per character |
| Hunt detail | `/hunt/{id}` | Full breakdown of a single session |
| Inventory | `/inventory` | Stock levels, goals, and sale decisions |
| Items & prices | `/items` | Item list and market price management |

---

## Hunt Analyser Import

Two import modes accept hunt session data exported from the in-game Hunt Analyser:

| Mode | Format |
|---|---|
| Text paste | Raw text copied from the Hunt Analyser |
| JSON upload | JSON file exported from the Hunt Analyser |

Both formats are parsed into the same internal `ParsedHunt` dataclass before persistence. If any item or creature name in the log is not found in the database, the entire import is rejected (atomic behaviour).

---

## What is NOT in scope for Stage 1

- TibiaWiki scraping (added in Stage 2)
- JWT authentication (added in Stage 2)
- REST API / Swagger UI (Stage 2)
- React frontend (Stage 3)
- Mini wiki for items and creatures (Stage 2)
- Email, OAuth, or any auth mechanism beyond basic user selection
- Pagination

---

## Project Roadmap

### Stage 1 — Python / FastAPI / SQLite *(current)*
- [x] Project structure and virtual environment
- [x] Database configuration (SQLAlchemy + SQLite)
- [x] Base FastAPI app running with Uvicorn
- [x] 10 SQLAlchemy models (User, Server, Character, Item, Creature, ServerItemPrice, Inventory, HuntSession, HuntSessionItem, HuntSessionMonster)
- [x] Seed script (30 servers, 20 items, 20 creatures)
- [x] User and character management
- [x] Hunt session import — text and JSON formats
- [x] Hunt history and detail views
- [x] Inventory management with stock goals
- [x] Sale decision engine (Keep / Sell to NPC / Sell on market / No price available)
- [x] Market price management per server

### Stage 2 — Java / Spring Boot / PostgreSQL
- [x] Full domain model and Flyway migrations
- [x] JWT authentication (stateless Bearer token)
- [x] Swagger UI with Bearer auth scheme
- [x] Full CRUD REST API (Servers, Characters, Items, Creatures, Inventory, Hunt Sessions, Server Item Prices)
- [x] Hunt Analyser import — text and JSON formats
- [x] Sale Decision Engine
- [x] TibiaWiki scraper (three-level MediaWiki API crawl)
- [x] Admin API
- [ ] Deploy

### Stage 3 — React frontend *(planned)*

---

## Sobre o projeto

O TLIM nasceu de duas dores reais de um jogador de Tibia: saber o que fazer com o loot após uma hunt, e ter histórico estruturado de sessões para comparar onde vale mais a pena caçar.

Este projeto é desenvolvido em três etapas com stacks diferentes — Python/FastAPI/SQLite, Java/Spring Boot/PostgreSQL e React — como demonstração de evolução técnica e capacidade de transferir conhecimento entre linguagens. A ideia central é mostrar que o mesmo problema pode ser resolvido com ferramentas diferentes, evidenciando raciocínio transferível em vez de familiaridade com uma única tecnologia.

Faz parte de uma transição de carreira de Analista de Sistemas para Desenvolvedor.

---

## Author

**Guilherme Calgaro**
Systems Analyst | AI-assisted development methodologies
[LinkedIn](https://www.linkedin.com/in/guilherme-de-oliveira-calgaro/) · [GitHub](https://github.com/calgadev)
