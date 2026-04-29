# TLIM — Tibia Loot & Inventory Manager

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![Status](https://img.shields.io/badge/Stage%201-Complete-brightgreen)

A personal portfolio project built to solve real problems faced by Tibia players:
deciding what to do with loot after a hunt, and tracking hunt history to make
data-driven decisions about where to grind.

---

## Project Roadmap

| Stage | Stack | Repository | Status |
|-------|-------|------------|--------|
| **Stage 1** — Backend + Server-side UI | Python 3.12 · FastAPI · SQLAlchemy 2.0 · SQLite · Jinja2 | [tlim-python2](https://github.com/calgadev/tlim-python2) | ✅ Complete |
| **Stage 2** — Backend rewrite | Java 17 · Spring Boot · Spring Data JPA · PostgreSQL · Maven | [tlim-java](https://github.com/calgadev/tlim-java) | ✅ Complete |
| **Stage 3** — Modern frontend | React · JavaScript ES6+ · React Router · Axios | tlim-frontend *(coming soon)* | ⏳ Planned |

The project is intentionally developed in three stages with different stacks to demonstrate
that the same problem can be solved across different languages and technologies —
showing transferable knowledge rather than familiarity with a single tool.

---

## About Stage 1

### What it does (MVP scope)

- Classify loot items: keep, sell to NPC, or sell on the market
- Calculate available passive gold after accounting for stock goals
- Import hunt sessions from the Hunt Analyser (text and JSON formats)
- Store hunt history per character for future comparison
- Sale decision engine comparing NPC prices vs market prices per server

### Architecture
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

### Key technical decisions

- **Market price at server level** — shared across all characters on the same server, avoiding duplicate registration
- **`npc_buyable` as explicit boolean** — avoids ambiguity of using `npc_price = 0` as a sentinel value
- **Atomic hunt import** — all or nothing: if any item or creature in the log is missing from the database, nothing is persisted
- **`balance` not stored** — calculated at display time as `loot_total - supplies`, since both values are immutable after import
- **Sale decision engine** — four possible outcomes per item: Keep, Sell to NPC, Sell on market, No price available

---

## Running locally
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

> **Note:** Running `python seed.py` is required before using the application.
> It creates the database and populates it with 30 servers, 20 items and 20 creatures.

---

## Stage 1 — Progress Checklist

### Infrastructure
- [x] Project structure and virtual environment
- [x] Database configuration (SQLAlchemy + SQLite)
- [x] Base FastAPI app running with Uvicorn

### Database Models
- [x] User
- [x] Server
- [x] Character
- [x] Item
- [x] Creature
- [x] ServerItemPrice
- [x] Inventory
- [x] HuntSession
- [x] HuntSessionItem
- [x] HuntSessionMonster

### Seed Data
- [x] Servers
- [x] Items
- [x] Creatures

### User & Character Management
- [x] Router: users
- [x] Router: characters
- [x] Template: user selection screen
- [x] Template: character registration and listing

### Hunt Import
- [x] Parser: shared ParsedHunt dataclass
- [x] Parser: text format (Hunt Analyser)
- [x] Parser: JSON format (Hunt Analyser)
- [x] Service: hunt import and persistence
- [x] Router: hunt
- [x] Template: hunt import (text paste and JSON upload)
- [x] Template: hunt history
- [x] Template: hunt detail

### Inventory & Sale Decision Engine
- [x] Service: sale decision engine
- [x] Service: passive gold calculation
- [x] Router: inventory
- [x] Router: items
- [x] Template: inventory (stock, goals, sale decision)
- [x] Template: items and market prices

---

## Stage 2 — Planned additions

- TibiaWiki scraping for complete item and creature catalog
- Mini wiki for creatures: resistances, weaknesses, immunities, XP, hunting locations, possible loot
- Mini wiki for items: description, weight, NPC buyers, drop sources
- Cross-links between creature and item wiki pages
- `item_npc_prices` table replacing the `npc_seller` field omitted in Stage 1
- Authentication with password (user structure already exists)
- Inventory: filter by NPC seller
- Inventory: stock goal editing on item wiki page
- Items page: categories from scraping, pagination, links to item wiki pages
- Market price average suggestion across servers

---

## Sobre o projeto (português)

O TLIM nasceu de duas dores reais de um jogador de Tibia: saber o que fazer
com o loot após uma hunt, e ter histórico estruturado de sessões para comparar
onde vale mais a pena caçar.

Este projeto é desenvolvido em três etapas com stacks diferentes — Python/FastAPI/SQLite,
Java/Spring Boot/PostgreSQL e React — como demonstração de evolução técnica e capacidade
de transferir conhecimento entre linguagens. A ideia central é mostrar que o mesmo
problema pode ser resolvido com ferramentas diferentes, evidenciando raciocínio
transferível em vez de familiaridade com uma única tecnologia.

Faz parte de uma transição de carreira de Analista de Sistemas para Desenvolvedor.

---

*Built with Python 3.12 · FastAPI · SQLAlchemy · SQLite · Jinja2 · Bootstrap 5*
