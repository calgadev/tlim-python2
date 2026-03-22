# TLIM — Tibia Loot & Inventory Manager

A personal portfolio project built to solve real problems faced by Tibia players:
deciding what to do with loot after a hunt, and tracking hunt history to make
data-driven decisions about where to grind.

## Project Roadmap

| Stage | Stack | Status |
|-------|-------|--------|
| **Stage 1** — Backend + Server-side UI | Python 3.12 · FastAPI · SQLAlchemy 2.0 · SQLite · Jinja2 | 🔄 In progress |
| **Stage 2** — Backend rewrite | Java 17 · Spring Boot · Spring Data JPA · PostgreSQL · Maven | ⏳ Planned |
| **Stage 3** — Modern frontend | React · JavaScript ES6+ · React Router · Axios | ⏳ Planned |

The project is developed in three stages with different stacks to demonstrate
that the same problem can be solved across different languages and technologies —
showing transferable knowledge rather than familiarity with a single tool.

## About Stage 1

**What it does (MVP scope):**
- Classify loot items: keep, sell to NPC, or sell on the market
- Calculate available passive gold after accounting for stock goals
- Import hunt sessions from the Hunt Analyser (text and JSON formats)
- Store hunt history per character for future comparison

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
- [ ] Parser: shared ParsedHunt dataclass
- [ ] Parser: text format (Hunt Analyser)
- [ ] Parser: JSON format (Hunt Analyser)
- [ ] Service: hunt import and persistence
- [ ] Router: hunt
- [ ] Template: hunt import (text paste and JSON upload)
- [ ] Template: hunt history
- [ ] Template: hunt detail

### Inventory & Sale Decision Engine
- [ ] Service: sale decision engine
- [ ] Service: passive gold calculation
- [ ] Router: inventory
- [ ] Router: items
- [ ] Template: inventory (stock, goals, sale decision)
- [ ] Template: items and market prices

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

# Start the development server
uvicorn main:app --reload
```

Access at `http://127.0.0.1:8000`

## Stage 2 — Planned additions

- TibiaWiki scraping for complete item and creature catalog
- Mini wiki for creatures: resistances, weaknesses, immunities, XP, hunting locations, possible loot
- Mini wiki for items: description, weight, NPC buyers, drop sources
- Cross-links between creature and item wiki pages
- npc_seller data via separate item_npc_prices table
- Authentication with password

---

## Sobre o projeto (português)

O TLIM nasceu de duas dores reais de um jogador de Tibia: saber o que fazer
com o loot após uma hunt, e ter histórico estruturado de sessões para comparar
onde vale mais a pena caçar.

Este projeto é desenvolvido em três etapas com stacks diferentes (Python, Java
e React), como demonstração de evolução técnica e capacidade de transferir
conhecimento entre linguagens. Faz parte de uma transição de carreira de
Analista de Sistemas para Desenvolvedor.
