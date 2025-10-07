# 👑 **ArchonKit** - Django-style scaffolder  for FastAPI [MPA-First approach]

ArchonKit is a CLI toolkit for building **server-rendered applications** with FastAPI using a familiar **Django-like structure**. It focuses on **MPA (Multi-Page Applications)** but still gives you FastAPI’s full **async-native performance and concurrency**.

## 🧠 Why FastAPI Instead of Django
ArchonKit is built on **FastAPI** — not for APIs, but as the foundation of a **modern, MPA-first and monolithic web framework**.

While Django has long been the standard for full-stack development, it’s also highly opinionated and rigid in structure. Its tightly coupled components make it less flexible for experimenting with new patterns or modern async workflows.  

FastAPI offers a clean, async-native foundation that allows ArchonKit to stay **monolithic by choice**, yet **modern in design**.

### Why It Fits ArchonKit
- ⚡ **ASGI & Async-Native** – Runs on modern Python async I/O for high performance and scalability.  
- 🧩 **Monolithic by Design** – Everything lives under one project, keeping development simple and cohesive.  
- 🧠 **MPA-First** – Focused on server-rendered pages with Jinja2.  
- 🧱 **Opinionated, Not Restrictive** – Provides structure while staying flexible where it matters.  
- 🔮 **Future-Ready** – Built to handle WebSockets, streaming, and reactive UI patterns.

Although ArchonKit uses **SQLAlchemy** as its ORM, this integration is **intentional and modular** — offering a powerful database layer without the heavy abstractions of Django’s stack.

> In short, FastAPI gives ArchonKit the perfect balance: the performance and modern architecture of an async framework, with the simplicity and developer experience of a classic monolithic web framework.

## ✨ Features

- 🏗️ **Scaffolding**: Create new projects and modular apps (`users`, `blog`, etc.) with a clean layout.
- 📂 **Django-like structure**: `forms.py`, `models.py`, `routes.py`, `templates/`, `static/`.
- 🗄️ **SQLAlchemy ORM** (default) + Alembic migrations.
- ⚡ **Async-native**: Full FastAPI async support even for MPA development.
- 🛠️ **Developer workflow**: Inspired by Django’s `makemigrations` / `migrate`