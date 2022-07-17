import pika, json

params = pika.URLParameters('amqps://mcmaaeit:gn6IUolkO-1VI-7ieVW30COo-_Po71RC@sparrow.rmq.cloudamqp.com/mcmaaeit')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='user', body=json.dumps(body), properties=properties)
