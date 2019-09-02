from scripts.funcs import mask_cnpj, ResultIter, initiate_db
conn, cur = initiate_db("./db/acordaos-download.db")
QUERY = """SELECT id, interessado_reponsavel_recorrente, repr_legal,sumario, acordao, quorum, 
relatorio, voto from download_acordaos where urn_year = 2018 or urn_year = 2019"""

mapping_index_feature = {
    1 : 'interessado_reponsavel_recorrente',
    2 : 'repr_legal',
    3 : 'sumario',
    4 : 'acordao',
    5 : 'quorum', 
    6 : 'relatorio',
    7 : 'voto'
    
}

query_generator = ResultIter(cur, QUERY)
with open("./logs/anonimizacao_logging_000.txt", 'w', encoding='utf8') as log:
    for data in query_generator:
        for index, feature in enumerate(data[1:], 1):
            #verifica se a feature tem cnpj caracterizado
            check_for_cpf = mask_cnpj(feature)
            if check_for_cpf:
                check_for_cpf = check_for_cpf.replace("'","")
                UPDATE_STRING = f"UPDATE download_acordaos SET {mapping_index_feature[index]} = '{check_for_cpf}' WHERE id = {data[0]}"
                cur.execute(UPDATE_STRING)
                log.write(f"id {data[0]} atualizado na feature {mapping_index_feature[index]}.\n")
        conn.commit()
conn.close()







