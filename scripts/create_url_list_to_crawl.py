from scripts.funcs import initiate_db
import json
conn, cur = initiate_db("./db/acordaos-download.db")

urls = cur.execute(f"SELECT url_lexml from download_acordaos where was_downloaded =0").fetchall()

container = {}
for index, url in enumerate(urls):
    container[index] = url[0]

with open("./crawlers/projects/api_acordaos/apiacordao/apiacordao/request/urls.json", 'w', encoding='utf8') as file:
    json.dump(container, file)

conn.close()