# example_publisher.py
import pika
import os
import logging
logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
channel = connection.channel()  # start a channel
channel.queue_declare(queue='scrapper')  # Declare a queue
# send a message

channel.basic_publish(
    exchange='', routing_key='scrapper', body='https://www.20min.ch/story/parlament-muss-sich-mit-drei-dutzend-corona-vorstoessen-befassen-613331372526')
print("[x] Message sent to consumer")
connection.close()
