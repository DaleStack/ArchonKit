# 👑 ArchonKit: The Fast, Familiar, MPA-First Python ToolKit

## 🚀 Why ArchonKit?
ArchonKit was born out of frustration. Coming from Django, I’m used to a **batteries-included** framework — one that makes building projects smooth without too much boilerplate.  
FastAPI is amazing for APIs, but when it comes to **multi-page apps (MPA)** setup with templates and static files, things get repetitive.  

ArchonKit fixes that by providing a **FastAPI-based toolkit** with a **Django-like developer experience**, while staying fast and modern.

---

## ❓ Why FastAPI if ArchonKit is MPA-first?

Good question! If you’re building server-rendered multi-page apps (MPAs), Django might feel like the obvious choice. So why does ArchonKit use **FastAPI** instead?

- ⚡ **Concurrency by default** – FastAPI is built on Starlette/ASGI and can handle many requests concurrently, even if your views are not async.  
- 🧠 **Modern async support** – You can seamlessly write async database queries or API calls when you need them.  
- 🔌 **Extensible** – FastAPI integrates well with modern Python tooling (pydantic, SQLAlchemy, Alembic, etc.).  
- 🎯 **Leverages Django knowledge without lock-in** – ArchonKit gives you the familiar "apps + templates + ORM + migrations" workflow from Django, but on a leaner, async-native stack.

In short: **ArchonKit = Django’s developer experience + FastAPI’s async performance**.

---

## ✨ Features
- **MPA-First**: Templates and static files are built-in.  
- **SQLAlchemy by Default**: Database integration comes ready-to-use.  
- **Alembic by Default**: Database Model Migrations
- **Familiar Structure**: Opinionated project layout inspired by Django, but simplified.  
- **CLI Included**: Quickly scaffold apps and project files. 
- **Extendable**: Use FastAPI’s async power, but without losing the batteries.