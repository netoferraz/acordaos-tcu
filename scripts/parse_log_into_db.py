"""
Atualiza o banco de dados com as informações contidas
nos arquivos de log do crawler.
"""
from pathlib import Path
import pandas as pd
from scripts.funcs import search_for_urn, initiate_db
conn, cur = initiate_db("./db/acordaos-download.db")
files_to_parse = Path("./logs").glob("*.log")
filter_files_of_interest = [f for f in files_to_parse if f.name != 'geckodriver.log' ]
is_downloaded = 1
for f in filter_files_of_interest:
    df = pd.read_csv(f, header=None, sep='|', names=['datetime', 'status', 'msg'])
    df['data'] = df['datetime'].apply(lambda x: x[:10])
    df['urn'] = df['msg'].apply(search_for_urn)
    filter_data = [(data.data, data.urn) for data in df.itertuples()]
    for data in filter_data:
        cur.execute(f"""
        UPDATE download_acordaos 
        SET was_downloaded = {is_downloaded}, downloaded_at = {data[0]}
        WHERE urn = '{data[1]}'
        """)
conn.commit()
conn.close()



