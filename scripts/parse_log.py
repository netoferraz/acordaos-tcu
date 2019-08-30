import re
pattern = 'ERROR: Spider error processing <GET https://www\.\w+\.\w+\.\w+/.+'

with open(r"C:\Users\netof\Documents\opensource\acordaos-tcu\crawlers\projects\api_acordaos\apiacordao\error.log", 'r', encoding='utf8') as f:
    with open("./logs/urns_to_delete.log", "w", encoding='utf8') as _:
        d = f.readlines()
        for line in d:
            l = line.replace("\n", "")
            find_error = re.search(pattern, l)
            if find_error:
                error_urn = find_error.group(0).split("/")[-1][:-1].split(">")[0]
                _.write(f"{error_urn}\n")