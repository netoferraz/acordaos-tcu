#escrever um arquivo com as urn que geraram erro no crawler
import re
pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\sERROR\s\[scrapy.core.scraper\]\sSpider error processing\s<GET https?:\/\/.*[\r\n]*'

logfilename = 'log_apiacordao_14.txt'
with open(f"./logs/{logfilename}", 'r', encoding='utf8') as f:
    with open("./logs/urns_to_delete_2.log", "w", encoding='utf8') as _:
        d = f.readlines()
        for line in d:
            l = line.replace("\n", "")
            find_error = re.search(pattern, l)
            if find_error:
                error_urn = find_error.group(0).split("/")[4].split(">")[0]
                _.write(f"{error_urn}\n")