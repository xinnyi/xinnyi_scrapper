# example_publisher.py
import pika
import os
import json

# Parse CLODUAMQP_URL (fallback to localhost)
params = pika.URLParameters("amqp://klemens.li:5672")
params.socket_timeout = 5

connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel = connection.channel()  # start a channel
channel.queue_declare(queue='scrapper')  # Declare a queue
# send a message

message = {'url': 'https://www.20min.ch/story/parlament-muss-sich-mit-drei-dutzend-corona-vorstoessen-befassen-613331372526', 'userid': "1234"}

channel.basic_publish(
    exchange='', routing_key='artistore_articles', body=json.dumps(message))
print("[x] Message sent to consumer")
connection.close()
