from elasticsearch import Elasticsearch

# Connect to elasticseatch
es = Elasticsearch(["localhost:9200"])


res = es.search(index="scrapper", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print(hit["_source"]["timestamp"], hit["_id"])
