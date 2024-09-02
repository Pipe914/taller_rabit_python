import pika
import json

# Configuración de la conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaración de la cola
channel.queue_declare(queue='order_queue')

def send_order(order):
    # Convertir la orden a un formato JSON y enviarla a la cola
    channel.basic_publish(exchange='',
                          routing_key='order_queue',
                          body=json.dumps(order))
    print(f"Orden enviada: {order}")

# Ejemplo de una orden de compra
order = {
    'order_id': 5678,
    'items': [
        {'product': 'Tela de algodón', 'quantity': 10, 'unit': 'metros'},
        {'product': 'Tela de lino', 'quantity': 5, 'unit': 'metros'}
    ],
    'total_price': 150.0,
    'payment_method': 'transferencia bancaria',
    'customer_email': 'afanadoraf@gmail.com'
}

# Enviar la orden
send_order(order)

# Cerrar la conexión
connection.close()