#escrever um arquivo com as urn que geraram erro no crawler
import re
pattern = 'ERROR: Spider error processing <GET https?:\/\/.*[\r\n]*'
logfilename = 'error.log'
with open(f"./logs/{logfilename}", 'r', encoding='utf8') as f:
    with open("./logs/urns_to_delete_0.log", "w", encoding='utf8') as _:
        d = f.readlines()
        for line in d:
            l = line.replace("\n", "")
            find_error = re.search(pattern, l)
            if find_error:
                error_urn = find_error.group(0).split("/")[-1][:-1].split(">")[0]
                #error_urn = find_error.group(0).split('(')[-1].split('referer')[-1][2:].split("/")[-1][:-1]
                _.write(f"{error_urn}\n")