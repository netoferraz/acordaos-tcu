import sqlite3
from pathlib import Path
rootpathdb = Path("./db")
if not rootpathdb.is_dir():
    rootpathdb.mkdir(exist_ok=True, parents=True)
conn = sqlite3.connect('./db/acordaos-download.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE download_acordaos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        urn TEXT NOT NULL,
        url INTEGER,
        was_downloaded  DEFAULT 0,
        downloaded_at DATE
);
""")
conn.close()