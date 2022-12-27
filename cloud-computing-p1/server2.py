import pika, sys, os
import image_storage as i
import image_tagger as it
import database as d
import server1 as s
import mail as m

AMQP_URL = "amqps://hjusozzq:hDeZfzaQ_9nZ0fkpx6wR46FvcMYLdmVj@whale.rmq.cloudamqp.com/hjusozzq"

def main():
    cursor,db_connection = d.database_connection()
    connection = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    channel = connection.channel()

    channel.queue_declare(queue='id9')

    def callback(ch, method, properties, body):
        id = int.from_bytes(body, byteorder='little') - 48
        print(id)
        i.download_image_s3(id)
        path = "./temp/"+str(id)+".png"
        category,state = it.upload_get_tag(id)
        d.database_update(cursor,db_connection,id,category,state)

        if state == 'rejected':
            text = "Your ad has not been accepted"

        if state == 'accepted':
            text = "Your ad has been accepted"

        email = d.database_get_email(cursor,id)
        print(email['email'])

        response = m.send_simple_message(email['email'], 'state update for your ad', text)
        print(response.json())

        os.remove(path)

    channel.basic_consume(queue='id9', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)