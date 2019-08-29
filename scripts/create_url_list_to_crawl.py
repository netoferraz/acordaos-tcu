from scripts.funcs import initiate_db

conn, cur = initiate_db("./db/acordaos-download.db")

urls = cur.execute(f"SELECT url_lexml from download_acordaos where was_downloaded =0").fetchall()

with open("./data/url_to_crawl.csv", 'w', encoding='utf8') as file:
    file.write("url\n")
    for url in urls:
        file.write(f"{url[0]}\n")

conn.close()