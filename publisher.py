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
    exchange='', routing_key='scrapper', body='https://stackoverflow.com/questions/534839/how-to-create-a-guid-uuid-in-python')
print("[x] Message sent to consumer")
connection.close()
