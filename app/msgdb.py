"""Simple wrapper over an sqlite3 database to store textual messages."""

import sqlite3
import logging
from typing import *

from .utils import Lazy

_logger = logging.getLogger(__name__)


def _open_db() -> sqlite3.Connection:
    db = sqlite3.connect('app/data/messages.db')
    db.execute("CREATE TABLE IF NOT EXISTS Messages(message TEXT NOT NULL)")
    return db


__db: Lazy[sqlite3.Connection] = Lazy(_open_db)


def insert(message: str) -> int:
    cur = __db.execute("INSERT INTO Messages(message) VALUES (?)", [message])
    __db.commit()
    _logger.debug("Message '{}' was saved with id {:d}".format(message, cur.lastrowid))
    return cur.lastrowid


def select(rowid: int) -> Optional[str]:
    cur = __db.execute("SELECT message FROM Messages WHERE rowid=?", [rowid])
    row = cur.fetchone()
    return row[0] if row else None


def _mock_database(tempfile):
    """Open another file as the database. Used internally for testing purposes."""
    conn = sqlite3.connect(tempfile)
    conn.execute("CREATE TABLE Messages(message TEXT NOT NULL)")
    __db._set_for_testing(conn)
