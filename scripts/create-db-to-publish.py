from scripts.funcs import initiate_db

import sqlite3
from pathlib import Path
rootpathdb = Path("./db")
if not rootpathdb.is_dir():
    rootpathdb.mkdir(exist_ok=True, parents=True)
conn = sqlite3.connect('./db/tcu-acordaos.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE acordaos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        urn TEXT NOT NULL,
        ano_acordao INTEGER,
        numero_acordao TEXT,
        relator TEXT,
        processo TEXT,
        tipo_processo TEXT,
        data_sessao DATE,
        numero_ata TEXT,
        interessado_reponsavel_recorrente TEXT,
        entidade TEXT,
        representante_mp TEXT,
        unidade_tecnica TEXT,
        repr_legal TEXT,
        assunto TEXT,
        sumario TEXT,
        acordao TEXT,
        quorum TEXT,
        relatorio TEXT,
        voto TEXT
);
""")
cursor.execute("CREATE INDEX urnindex ON acordaos(urn);")
cursor.execute("CREATE INDEX urnyear ON acordaos(ano_acordao);")
conn.commit()
conn.close()