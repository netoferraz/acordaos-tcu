#escrever um arquivo com as urn que geraram erro no crawler
import re
pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\sERROR\s\[scrapy.core.scraper\]\sSpider error processing\s<GET https?:\/\/.*[\r\n]*'
pattern_2 = r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s\[scrapy\.core\.scraper\]\sERROR:\sSpider\serror\sprocessing\s<GET https?:\/\/.*[\r\n]*'
multiple_pattern = f"{pattern}|{pattern_2}"
find_urn = 'urn:lex:br:.+'
logfilename = '2019_08_31_00.log'
with open(f"./logs/{logfilename}", 'r', encoding='utf8') as f:
    with open("./logs/urns_to_delete_4.log", "w", encoding='utf8') as _:
        d = f.readlines()
        for line in d:
            l = line.replace("\n", "")
            find_error = re.search(multiple_pattern, l)
            if find_error:
                split_str = find_error.group(0).split("/")
                try:
                    error_urn = [text for text in split_str if re.search(find_urn, text)][0][:-1]
                except IndexError:
                    url_to_crawl = find_error.group(0).split('<GET')[1].split('>')[0]
                    if 'ACORDAO-COMPLETO' in url_to_crawl:
                        _.write(f"{url_to_crawl}\n")
                else:
                    _.write(f"{error_urn}\n")