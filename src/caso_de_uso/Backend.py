import pika
import json
import smtplib
from email.mime.text import MIMEText

# Configuración de la conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaración de la cola (debe ser la misma que la del productor)
channel.queue_declare(queue='order_queue')

def send_email(email, subject, message):
    # Configuración del correo
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = 'noreply@tiendaonline.com'
    msg['To'] = email
    
    # Enviar el correo (este ejemplo utiliza un servidor SMTP ficticio)
    # Asegúrate de configurar un servidor SMTP real
    try:
        with smtplib.SMTP('localhost') as server:
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print(f"Correo enviado a {email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def process_order(ch, method, properties, body):
    order = json.loads(body)
    print(f"Procesando orden: {order}")
    
    # Simulación de validación de la compra y el pago
    if order['payment_method'] == 'transferencia bancaria':
        print("Pago validado con éxito.")
        
        # Enviar correo de confirmación
        send_email(order['customer_email'], 
                   f"Confirmación de compra: Orden {order['order_id']}",
                   f"Su orden {order['order_id']} ha sido confirmada. Gracias por su compra.")
    else:
        print("Error en el método de pago.")
        
        # Enviar correo de fallo de transacción
        send_email(order['customer_email'], 
                   f"Error en la compra: Orden {order['order_id']}",
                   f"Su orden {order['order_id']} no pudo ser procesada debido a un error en el pago. Por favor, intente nuevamente o contacte con soporte.")
    
    # Confirmar que el mensaje fue procesado
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Configurar el consumidor para que escuche en la cola
channel.basic_consume(queue='order_queue',
                      on_message_callback=process_order)

print('Esperando órdenes. Presiona Ctrl+C para salir.')
channel.start_consuming()