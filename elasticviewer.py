from elasticsearch import Elasticsearch

# Connect to elasticseatch
es = Elasticsearch(["localhost:9200"])


res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(url)s" % hit["_source"])
