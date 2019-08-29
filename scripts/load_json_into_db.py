from pathlib import Path
from scripts.funcs import initiate_db
import json

list_files = Path("./data/api/parsed").rglob("*.json")
list_files = [f for f in list_files if 'dump' in f.name]
conn, cur = initiate_db("./db/acordaos-download.db")

for dump in list_files:
    with open(dump, 'r', encoding='utf8') as _:
        d = json.load(_)
        for item in d:
            query_string = f"""
            UPDATE download_acordaos 
            SET urn_year = {item['urn_year']}, 
            numero_acordao = '{item['numero_acordao']}', 
            numero_acordao_href = '{item['numero_acordao_href']}',
            relator = '{item['relator']}',
            processo = '{item['processo']}',
            processo_href = '{item['processo_href']}',
            tipo_processo = '{item['tipo_processo']}',
            data_sessao = '{item['data_sessao']}',
            numero_ata = '{item['numero_ata']}',
            interessado_reponsavel_recorrente = '{item['interessado_reponsavel_recorrente']}',
            entidade = '{item['entidade']}',
            representante_mp = '{item['representante_mp']}',
            unidade_tecnica = '{item['unidade_tecnica']}',
            repr_legal = '{item['repr_legal']}',
            assunto = '{item['assunto']}',
            sumario = '{item['sumario']}',
            acordao = '{item['acordao']}',
            quorum = '{item['quorum']}',
            relatorio = '{item['relatorio']}',
            voto = '{item['voto']}',
            was_downloaded = {item['was_downloaded']},
            downloaded_at = {item['downloaded_at']}
            WHERE urn = '{item['urn']}'"""
            cur.execute(query_string)
            conn.commit()
            print(f"Concluído o update de {item['urn']}.")