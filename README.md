# 👑 **ArchonKit** — A Django-Style Framework for FastAPI (MPA-First Approach)

ArchonKit is **more than just a scaffolder** — it’s a **CLI-powered web framework** for building **server-rendered (MPA) applications** with **FastAPI**.

It provides a **Django-like project structure** and developer experience while keeping FastAPI’s **async-native performance**, **flexibility**, and **modern Python tooling**.  
ArchonKit helps developers build traditional, **monolithic, server-rendered web apps** — without sacrificing the benefits of an async architecture.

> 🧱 **MPA-First. Monolithic. Modern.**

---

## 🧠 Why FastAPI Instead of Django

ArchonKit is built on **FastAPI** — not for APIs, but as the foundation of a **modern, MPA-first, monolithic web framework**.

While Django remains a proven full-stack framework, it’s also highly opinionated and rigid in structure. Its tightly coupled components make it difficult to experiment with new patterns or async workflows.  
FastAPI, on the other hand, provides a clean and modular foundation that allows ArchonKit to stay **monolithic by choice**, yet **modern in design**.

### Why It Fits ArchonKit
- ⚡ **ASGI & Async-Native** – Runs on modern Python async I/O for high performance and scalability.  
- 🧩 **Monolithic by Design** – Everything lives in one cohesive project for simplicity and clarity.  
- 🧠 **MPA-First** – Focused on classic, server-rendered pages using Jinja2 templates.  
- 🧱 **Opinionated, Not Restrictive** – Provides structure while staying flexible where it matters. 
- 🔮 **Future-Ready** – Built to support WebSockets, streaming, and reactive UI patterns.

Although ArchonKit integrates tightly with **SQLAlchemy**, this coupling is **intentional and modular** — providing a powerful database layer without the heavy abstractions of Django’s stack.

> In short, FastAPI gives ArchonKit the perfect balance: the **performance and modern architecture** of an async framework, with the **simplicity and developer experience** of a classic monolithic web framework.

---

## 🌍 Why MPA-First

ArchonKit follows an **MPA-first (Multi-Page Application)** philosophy — prioritizing **server-rendered pages** over heavy front-end frameworks.

Modern web stacks have become increasingly complex, with layers of client-side routing, hydration, and state management. ArchonKit brings back the simplicity of traditional web development while embracing the best of modern async Python.

### Why It Matters
- 🧩 **Simplicity by Design** – Each request is rendered on the server — no build tools, hydration, or complex front-end state to manage.  
- ⚡ **Performance & SEO** – Server-rendered HTML means faster first paint, better SEO, and minimal JavaScript.  
- 🧠 **Developer Productivity** – Focus on Python, templates, and logic — not front-end pipelines.  
- 🔌 **Async & Real-Time Ready** – Powered by FastAPI, ArchonKit supports async I/O, WebSockets, and streaming responses.  
- 🪶 **Light but Dynamic** – Combine with htmx or Alpine.js for SPA-like interactivity without the overhead.

> In 2025, MPAs aren’t outdated — they’re *evolving*.  
> ArchonKit embraces this evolution, merging the **clarity of classic web apps** with the **performance and capabilities of modern async frameworks**.

---

## ✨ Features

- 🏗️ **Project & App Scaffolding** – Quickly create new projects and modular apps (`users`, `blog`, etc.) with a clean layout.  
- 📂 **Django-Like Structure** – Familiar organization: `forms.py`, `models.py`, `routes.py`, `templates/`, and `static/`.  
- 🗄️ **SQLAlchemy ORM + Alembic** – Built-in database layer with migrations.  
- ⚡ **Async-Native** – Full FastAPI async support, even for MPA development.  
- 🛠️ **Developer Workflow** – Inspired by Django’s commands (`makemigrations`, `migrate`, etc.).  

---

> ArchonKit combines the elegance of Django’s structure with the power of FastAPI’s async engine — bringing back the joy of building classic MPAs in the modern Python ecosystem.
