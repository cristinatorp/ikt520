import pika
import sys
import re

# Run RabbitMQ:
# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


status_codes = {
    "200": "OK",
    "206": "Partial consent",
    "301": "Permanently moved",
    "304": "Not modified",
    "404": "Not found",
    "502": "Bad gateway"
}

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

# Receive filter info (status code) from the user
# Can be several (e.g. 206 404 304), one (e.g. 200) or none (includes all)
user_input = sys.argv[1:]
if not user_input:
    for code in status_codes:
        user_input.append(code)

for code in user_input:
    channel.queue_bind(exchange="direct_logs", queue=queue_name, routing_key=code)

print(f"Waiting for logs...")


def callback(ch, method, properties, body):
    code = method.routing_key
    code_color = colors.OKGREEN if code == "200" else (colors.WARNING if code == "206" else colors.FAIL)

    message = body.decode().split(" ")
    ip, date, time, request, url = message[0], message[3][1:12], message[3][13:], message[5], message[6]

    # [date & time] [status code & message] source IP | url & HTTP method
    formatted_output = f"[{date} {time}] " \
                       f"{code_color}[{code}: {status_codes[code].upper()}]" \
                       f"{colors.ENDC} Source IP: {colors.HEADER}{colors.BOLD}{ip}{colors.ENDC} | " \
                       f"Tried to access {colors.OKBLUE}\"{url}\"{colors.ENDC} ({request[1:]})"

    # Print to terminal with colors
    print(formatted_output)

    # Write to file without colors
    ansi_re = re.compile(r'\x1b\[[0-9;]*m')
    with open("./Lab4/output/formatted_output_404.log", "a") as file:
        file.write(re.sub(ansi_re, "", formatted_output) + "\n")


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
