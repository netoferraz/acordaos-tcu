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
        url_lexml TEXT,
        numero_acordao TEXT,
        numero_acordao_href TEXT,
        relator TEXT,
        processo TEXT,
        processo_href TEXT,
        tipo_processo TEXT,
        data_sessao TEXT,
        numero_ata TEXT,
        numero_ata_href TEXT,
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
        voto TEXT,
        url_tcu TEXT,
        was_downloaded  DEFAULT 0,
        downloaded_at DATE
);
""")
cursor.execute("CREATE INDEX urnindex ON download_acordaos(urn);")
conn.commit()
conn.close()