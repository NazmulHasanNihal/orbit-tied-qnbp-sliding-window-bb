---
name: antigravity-skill-vault
description: >-
  Access and route across 300+ enterprise-ready Antigravity agent skills from the
  Antigravity Skill Vault (by @rmyndharis). Use when you need specialized engineering,
  architecture, performance optimization, debugging, database, security, or domain-specific
  capabilities across the software lifecycle that go beyond the built-in workspace skills.
---

# Antigravity Skill Vault (300+ Skills)

This vault houses 307 specialized agent skills curated for Google Antigravity. It enables progressive disclosure: instead of loading hundreds of skills into context, query this catalog on-demand and load only the skill needed for the task.

---

## 1. Finding a Skill in the Vault

Search the local catalog using `catalog.json` or `bundles.json`:

```bash
# Search by keyword in the catalog:
python -c "import json; [print(s['name'], ':', s['description'][:90]) for s in json.load(open('.agent/skills/antigravity-skill-vault/catalog.json')) if '<keyword>' in (s['name'] + ' ' + s['description']).lower()]"
```

Or view pre-assembled bundles in `bundles.json`:
- `core-dev`: Essential engineering (clean code, refactoring, review, debugging, Git).
- `data-core`: Data engineering, database optimization, Spark, PostgreSQL, SQL.
- `ai-core`: Machine learning pipelines, evaluation, RAG, prompt engineering, vector databases.
- `security-core`: Threat modeling, code scanning, secrets management, auth patterns.
- `ops-core`: Observability, tracing, Prometheus, Grafana, SLOs, incident response.

---

## 2. Using a Skill from the Vault

Once you identify the appropriate skill folder under `.agent/skills/antigravity-skill-vault/skills/<skill-name>/`:

1. Read `.agent/skills/antigravity-skill-vault/skills/<skill-name>/SKILL.md`.
2. Follow its step-by-step procedures, references, and scripts.
3. If this skill is used frequently in this repository, you may copy it directly to the root `.agent/skills/<skill-name>/` folder.

