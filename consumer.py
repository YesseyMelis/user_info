import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "user_info.settings")
django.setup()

from user_infos.models import UserInfo
from user_infos.serializers import UserInfoSerializer

params = pika.URLParameters('amqps://mcmaaeit:gn6IUolkO-1VI-7ieVW30COo-_Po71RC@sparrow.rmq.cloudamqp.com/mcmaaeit')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='info')


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(data)
    if properties.content_type == 'user_created':
        UserInfo.objects.create(
            id=data['id'],
            email=data.get('email', None),
            telegram=data.get('telegram', None),
            instagram=data.get('instagram', None),
            phone=data.get('phone', None)
        )
        print('User Created')
    elif properties.content_type == 'user_updated':
        user_info = UserInfo.objects.get(id=data['id'])
        if data.get('email', None):
            user_info.email = data.get('email')
        if data.get('telegram', None):
            user_info.telegram = data.get('telegram')
        if data.get('instagram', None):
            user_info.instagram = data.get('instagram')
        if data.get('phone', None):
            user_info.phone = data.get('phone')
        user_info.save()
        print('User Updated')
    elif properties.content_type == 'user_info':
        user_infos = UserInfo.objects.all()
        serializer = UserInfoSerializer(user_infos, many=True)
        channel.basic_publish(
                        exchange='',
                        routing_key=properties.reply_to,
                        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                        body=json.dumps(serializer.data))
        # channel.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='info', on_message_callback=callback, auto_ack=True)
print('Started Consuming')
channel.start_consuming()
channel.close()
