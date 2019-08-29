from scrapy import cmdline
years=['2011']
for year in years:
    query =  f"scrapy crawl api -a year='{year}' -s HTTPCACHE_ENABLED=1 -o ../../../../db/{year}.json"
    cmdline.execute(query.split())