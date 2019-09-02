from scripts.funcs import initiate_db, load_csv_into_db, load_json_into_db

conn, cur = initiate_db("./db/acordaos-download.db")
#years = list(range(1992, 2000))
filename = "./data/api/raw/2018_2019.json"
load_json_into_db(filename, cursor=cur)
#load_csv_into_db(years, cur)
conn.commit()
conn.close()
