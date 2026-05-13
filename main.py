import json
from contextlib import asynccontextmanager
from pathlib import Path

import jinja2
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from scraper import scrape_all, load_data, save_data

BASE_DIR = Path(__file__).parent

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=True,
    cache_size=0,
)


def render_template(name: str, **context) -> str:
    template = jinja_env.get_template(name)
    return template.render(**context)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        data = await scrape_all()
        save_data(data)
    except Exception as e:
        print(f"Initial scrape failed: {e}")
    yield


app = FastAPI(title="智慧住建", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def load_systems() -> list[dict]:
    path = BASE_DIR / "systems.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def group_systems_by_dept(systems: list[dict]) -> list[dict]:
    groups = {}
    for s in systems:
        dept = (s.get("department") or "").split("\n")[0].strip()
        if not dept:
            dept = "其他"
        groups.setdefault(dept, []).append(s)
    return [{"department": dept, "systems": sys_list} for dept, sys_list in groups.items()]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    data = load_data()
    systems = load_systems()
    dept_groups = group_systems_by_dept(systems)
    html = render_template(
        "index.html",
        banners=data.get("banners", []),
        news=data.get("news", {}),
        dept_groups=dept_groups,
        updated_at=data.get("updated_at", ""),
    )
    return HTMLResponse(html)


@app.get("/api/refresh")
async def refresh():
    try:
        data = await scrape_all()
        save_data(data)
        return {"ok": True, "updated_at": data["updated_at"]}
    except Exception as e:
        return {"ok": False, "error": str(e)}
