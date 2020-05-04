rabbitmq in docker:
docker run -d --name rabbitmq -p 5672:5672 rabbitmq

elasticsearch in docker:
docker run -d --name elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.6.2
