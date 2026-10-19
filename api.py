import json
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API Santander (local)")
DB = "banco.db"


def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


# O banco de dados: id automático e cartão UNIQUE (as "constraints")
with conectar() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            card_number TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL DEFAULT 0,
            news TEXT NOT NULL DEFAULT '[]'
        )
    """)


class NovoUsuario(BaseModel):
    name: str
    card_number: str


class Noticia(BaseModel):
    description: str


def para_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "account": {"balance": row["balance"]},
        "card": {"number": row["card_number"]},
        "news": json.loads(row["news"]),
    }


@app.post("/users", status_code=201)
def criar_usuario(dados: NovoUsuario):
    try:
        with conectar() as con:
            cur = con.execute(
                "INSERT INTO users (name, card_number) VALUES (?, ?)",
                (dados.name, dados.card_number),
            )
            row = con.execute("SELECT * FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Cartão já cadastrado.")
    return para_dict(row)


@app.get("/users")
def listar_usuarios():
    with conectar() as con:
        return [para_dict(r) for r in con.execute("SELECT * FROM users")]


@app.get("/users/{user_id}")
def buscar_usuario(user_id: int):
    with conectar() as con:
        row = con.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return para_dict(row)


@app.post("/users/{user_id}/news")
def adicionar_noticia(user_id: int, noticia: Noticia):
    with conectar() as con:
        row = con.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        lista = json.loads(row["news"]) + [noticia.model_dump()]
        con.execute("UPDATE users SET news = ? WHERE id = ?", (json.dumps(lista), user_id))
    return {"id": user_id, "news": lista}

class NoticiaPut(BaseModel):
    icon: str | None = None
    description: str


class UsuarioPut(BaseModel):
    news: list[NoticiaPut]


@app.put("/users/{user_id}")
def atualizar_usuario(user_id: int, dados: UsuarioPut):
    with conectar() as con:
        row = con.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        news = [n.model_dump() for n in dados.news]
        con.execute("UPDATE users SET news = ? WHERE id = ?", (json.dumps(news), user_id))
        row = con.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return para_dict(row)