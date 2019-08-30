from scripts.funcs import initiate_db

conn, cur = initiate_db("./db/acordaos-download.db")

with open("./logs/urns_to_delete_2.log", "r", encoding='utf8') as f:
    d = f.readlines()
    for urn in d:
        urn = urn.replace("\n","")
        query_string = f"""
        DELETE from download_acordaos 
        WHERE urn = '{urn}'"""
        cur.execute(query_string)
        conn.commit()
        print(f"Concluído o delete de {urn}.")
conn.close()
