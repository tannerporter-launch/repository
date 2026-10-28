import hmac
import os
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

BASE = Path(__file__).parent
DB_PATH = os.environ.get("DB_PATH", str(BASE.parent / "data" / "app.db"))
APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")

if not APP_PASSWORD or not SECRET_KEY:
    raise RuntimeError("APP_PASSWORD and SECRET_KEY must be set (see .env.example)")

CLIENT_STATUSES = ["lead", "active", "paused", "churned"]
PROJECT_STATUSES = ["planned", "in_progress", "blocked", "done"]

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=60 * 60 * 24 * 14,
    same_site="strict",
    https_only=os.environ.get("COOKIE_SECURE", "1") == "1",
)
templates = Jinja2Templates(directory=str(BASE / "templates"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, contact TEXT DEFAULT '',
  email TEXT DEFAULT '', status TEXT NOT NULL DEFAULT 'active', notes TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS projects (
  id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
  name TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'planned', due_date TEXT DEFAULT '',
  budget REAL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  title TEXT NOT NULL, due_date TEXT DEFAULT '', done INTEGER NOT NULL DEFAULT 0
);
"""


def db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def query(sql, args=()):
    with closing(db()) as conn:
        return conn.execute(sql, args).fetchall()


def execute(sql, args=()):
    with closing(db()) as conn, conn:
        return conn.execute(sql, args).lastrowid


def authed(request: Request) -> bool:
    return bool(request.session.get("ok"))


def login_redirect():
    return RedirectResponse("/login", status_code=303)


def render(request, name, **ctx):
    return templates.TemplateResponse(request, name, ctx)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/login")
def login_form(request: Request):
    return render(request, "login.html", error=None)


@app.post("/login")
def login(request: Request, password: str = Form(...)):
    if hmac.compare_digest(password.encode(), APP_PASSWORD.encode()):
        request.session["ok"] = True
        return RedirectResponse("/", status_code=303)
    return render(request, "login.html", error="Wrong password")


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return login_redirect()


@app.get("/")
def dashboard(request: Request):
    if not authed(request):
        return login_redirect()
    today = date.today().isoformat()
    stats = {
        "clients": query("SELECT COUNT(*) c FROM clients WHERE status='active'")[0]["c"],
        "projects": query("SELECT COUNT(*) c FROM projects WHERE status IN ('in_progress','blocked')")[0]["c"],
        "open_tasks": query("SELECT COUNT(*) c FROM tasks WHERE done=0")[0]["c"],
    }
    overdue = query(
        """SELECT t.id, t.title, t.due_date, p.id pid, p.name project, c.name client
           FROM tasks t JOIN projects p ON p.id=t.project_id JOIN clients c ON c.id=p.client_id
           WHERE t.done=0 AND t.due_date != '' AND t.due_date < ? ORDER BY t.due_date""",
        (today,),
    )
    blocked = query(
        """SELECT p.id, p.name, c.name client FROM projects p JOIN clients c ON c.id=p.client_id
           WHERE p.status='blocked'"""
    )
    return render(request, "dashboard.html", stats=stats, overdue=overdue, blocked=blocked)


@app.get("/clients")
def clients(request: Request, status: str = ""):
    if not authed(request):
        return login_redirect()
    sql = """SELECT c.*, (SELECT COUNT(*) FROM projects p WHERE p.client_id=c.id) projects
             FROM clients c"""
    args = ()
    if status in CLIENT_STATUSES:
        sql += " WHERE c.status=?"
        args = (status,)
    rows = query(sql + " ORDER BY c.name COLLATE NOCASE", args)
    return render(request, "clients.html", clients=rows, statuses=CLIENT_STATUSES, current=status)


@app.post("/clients")
def add_client(request: Request, name: str = Form(...), contact: str = Form(""),
               email: str = Form(""), status: str = Form("active"), notes: str = Form("")):
    if not authed(request):
        return login_redirect()
    if status not in CLIENT_STATUSES:
        status = "active"
    cid = execute("INSERT INTO clients(name,contact,email,status,notes) VALUES(?,?,?,?,?)",
                  (name.strip(), contact, email, status, notes))
    return RedirectResponse(f"/clients/{cid}", status_code=303)


@app.get("/clients/{cid}")
def client_detail(request: Request, cid: int):
    if not authed(request):
        return login_redirect()
    rows = query("SELECT * FROM clients WHERE id=?", (cid,))
    if not rows:
        return RedirectResponse("/clients", status_code=303)
    projects = query(
        """SELECT p.*, (SELECT COUNT(*) FROM tasks t WHERE t.project_id=p.id AND t.done=0) open_tasks
           FROM projects p WHERE client_id=? ORDER BY p.due_date""", (cid,))
    return render(request, "client.html", client=rows[0], projects=projects,
                  client_statuses=CLIENT_STATUSES, project_statuses=PROJECT_STATUSES)


@app.post("/clients/{cid}")
def update_client(request: Request, cid: int, name: str = Form(...), contact: str = Form(""),
                  email: str = Form(""), status: str = Form("active"), notes: str = Form("")):
    if not authed(request):
        return login_redirect()
    if status not in CLIENT_STATUSES:
        status = "active"
    execute("UPDATE clients SET name=?,contact=?,email=?,status=?,notes=? WHERE id=?",
            (name.strip(), contact, email, status, notes, cid))
    return RedirectResponse(f"/clients/{cid}", status_code=303)


@app.post("/clients/{cid}/delete")
def delete_client(request: Request, cid: int):
    if not authed(request):
        return login_redirect()
    execute("DELETE FROM clients WHERE id=?", (cid,))
    return RedirectResponse("/clients", status_code=303)


@app.post("/clients/{cid}/projects")
def add_project(request: Request, cid: int, name: str = Form(...), due_date: str = Form(""),
                budget: float = Form(0), status: str = Form("planned")):
    if not authed(request):
        return login_redirect()
    if status not in PROJECT_STATUSES:
        status = "planned"
    pid = execute("INSERT INTO projects(client_id,name,due_date,budget,status) VALUES(?,?,?,?,?)",
                  (cid, name.strip(), due_date, budget, status))
    return RedirectResponse(f"/projects/{pid}", status_code=303)


@app.get("/projects/{pid}")
def project_detail(request: Request, pid: int):
    if not authed(request):
        return login_redirect()
    rows = query("""SELECT p.*, c.name client FROM projects p JOIN clients c ON c.id=p.client_id
                    WHERE p.id=?""", (pid,))
    if not rows:
        return RedirectResponse("/", status_code=303)
    tasks = query("SELECT * FROM tasks WHERE project_id=? ORDER BY done, due_date", (pid,))
    return render(request, "project.html", project=rows[0], tasks=tasks,
                  statuses=PROJECT_STATUSES, today=date.today().isoformat())


@app.post("/projects/{pid}")
def update_project(request: Request, pid: int, name: str = Form(...), due_date: str = Form(""),
                   budget: float = Form(0), status: str = Form("planned")):
    if not authed(request):
        return login_redirect()
    if status not in PROJECT_STATUSES:
        status = "planned"
    execute("UPDATE projects SET name=?,due_date=?,budget=?,status=? WHERE id=?",
            (name.strip(), due_date, budget, status, pid))
    return RedirectResponse(f"/projects/{pid}", status_code=303)


@app.post("/projects/{pid}/delete")
def delete_project(request: Request, pid: int):
    if not authed(request):
        return login_redirect()
    rows = query("SELECT client_id FROM projects WHERE id=?", (pid,))
    execute("DELETE FROM projects WHERE id=?", (pid,))
    return RedirectResponse(f"/clients/{rows[0]['client_id']}" if rows else "/clients", status_code=303)


@app.post("/projects/{pid}/tasks")
def add_task(request: Request, pid: int, title: str = Form(...), due_date: str = Form("")):
    if not authed(request):
        return login_redirect()
    execute("INSERT INTO tasks(project_id,title,due_date) VALUES(?,?,?)", (pid, title.strip(), due_date))
    return RedirectResponse(f"/projects/{pid}", status_code=303)


@app.post("/tasks/{tid}/toggle")
def toggle_task(request: Request, tid: int):
    if not authed(request):
        return login_redirect()
    rows = query("SELECT project_id FROM tasks WHERE id=?", (tid,))
    execute("UPDATE tasks SET done = 1 - done WHERE id=?", (tid,))
    return RedirectResponse(f"/projects/{rows[0]['project_id']}" if rows else "/", status_code=303)


@app.post("/tasks/{tid}/delete")
def delete_task(request: Request, tid: int):
    if not authed(request):
        return login_redirect()
    rows = query("SELECT project_id FROM tasks WHERE id=?", (tid,))
    execute("DELETE FROM tasks WHERE id=?", (tid,))
    return RedirectResponse(f"/projects/{rows[0]['project_id']}" if rows else "/", status_code=303)
