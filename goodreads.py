import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "duJuPv6MUWcUjUKpV3CUJg",
 "isbns": "1250121000"})
k =res.json()
tab = list()
tab.append(k['books'][0]['work_ratings_count'])
tab.append(k['books'][0]['average_rating'])
print(tab)

