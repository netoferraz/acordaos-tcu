from scripts.funcs import initiate_db, ResultIter, insert_into_db

conn, cur = initiate_db("./db/acordaos-download.db")
conn_pub, cur_pub = initiate_db("./db/tcu-acordaos.db")

QUERY = """SELECT urn, urn_year, numero_acordao, relator, 
        processo, tipo_processo, data_sessao, numero_ata, interessado_reponsavel_recorrente,
        entidade, representante_mp, unidade_tecnica, repr_legal, assunto, sumario,
        acordao, quorum, relatorio, voto from download_acordaos"""

cols_to_insert = [
    "urn",
    "ano_acordao",
    "numero_acordao",
    "relator",
    "processo",
    "tipo_processo",
    "data_sessao",
    "numero_ata",
    "interessado_reponsavel_recorrente",
    "entidade",
    "representante_mp",
    "unidade_tecnica",
    "repr_legal",
    "assunto",
    "sumario",
    "acordao",
    "quorum",
    "relatorio",
    "voto",
]
bulk_insert = []
query_generator = ResultIter(cur, QUERY)

for data in query_generator:
    bulk_insert.append(data)

insert_into_db(
    data=bulk_insert, table_name="acordaos", cols_names=cols_to_insert, cursor=cur_pub
)
conn_pub.commit()
conn_pub.close()
conn.close()
