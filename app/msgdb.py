import sqlite3
from typing import *

__db = sqlite3.connect('messages.db')
__db.execute("CREATE TABLE IF NOT EXISTS Messages(message TEXT NOT NULL)")


def insert(message: str) -> int:
    cur = __db.execute("INSERT INTO Messages(message) VALUES (?)", [message])
    return cur.lastrowid


def select(rowid: int) -> Optional[Tuple[str]]:
    cur = __db.execute("SELECT message FROM Messages WHERE rowid=?", [rowid])
    return cur.fetchone()


def select_all() -> List[Tuple[str]]:
    cur = __db.execute("SELECT message FROM Messages")
    return cur.fetchall()
