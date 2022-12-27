#-------------- RabbitMQ code --------------
# in this file we have a functions to send data to our queue (we store ids)

import pika

def RabbitMQ_send(id):
   AMQP_URL = "amqps://hjusozzq:hDeZfzaQ_9nZ0fkpx6wR46FvcMYLdmVj@whale.rmq.cloudamqp.com/hjusozzq"
   connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
   channel = connection.channel()

   channel.queue_declare(queue='id9')

   channel.basic_publish(exchange='', routing_key='id9', body=str(id))
   print("id Sent")
   connection.close()