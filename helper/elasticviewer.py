from elasticsearch import Elasticsearch

# Connect to elasticseatch
es = Elasticsearch(["localhost:9200"])

body = {"userid": "1234", "url": "https://www.20min.ch/story/parlament-muss-sich-mit-drei-dutzend-corona-vorstoessen-befassen-613331372526"}

res = es.search(index="article", body={"_source": False, "query": {
    "bool": {"should": [
        {"term": {"userid": body['userid']}},
        {"term": {"url": body['url']}}
    ]
    }}})

print("Got %d Hits:" % res['hits']['total']['value'])
if res['hits']['total']["value"] == 1:
    print(res['hits']['hits'][0]["_id"])
