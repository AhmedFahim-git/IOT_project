import paho.mqtt.client as mqtt
from mysql.connector import connect, Error
import json
from functools import partial

topic = "Test"
username = "user"
password = "password"
broker_hostname = "mosquitto"
port = 1883

db_host = "db"
db_user = "user"
db_password = "password"
db_database = "readings"


connection = connect(
    host=db_host, user=db_user, password=db_password, database=db_database
)
cursor = connection.cursor()


def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
        client.subscribe(topic)
    else:
        print("could not connect, return code:", return_code)


def write_db(timestamp: str, moisture: int):
    cursor.execute(
        f"INSERT into moistures (Times, moisture) values ('{timestamp}', {moisture})"
    )
    connection.commit()


def on_message(client, userdata, message):
    parsed_message = json.loads(str(message.payload.decode("utf-8")))
    write_db(
        timestamp=parsed_message["timestamp"], moisture=int(parsed_message["moisture"])
    )
    # cursor.execute(
    #     f"INSERT into moistures (Times, moisture) values ('{parsed_message['timestamp']}', {parsed_message['moisture']})"
    # )
    # connection.commit()
    print("Received message: ", str(message.payload.decode("utf-8")))


def init_db():
    cursor.execute(
        "CREATE TABLE if not exists moistures (Times DATETIME NOT NULL PRIMARY KEY, moisture INT)"
    )
    # return connection, cursor


def main():
    client = mqtt.Client("MQTT_database_service")
    client.username_pw_set(
        username=username, password=password
    )  # uncomment if you use password auth
    client.on_connect = on_connect
    client.on_message = on_message

    init_db()

    client.connect(broker_hostname, port)

    # connection, cursor = init_db()

    # connection = connect(
    #     host=db_host, user=db_user, password=db_password, database=db_database
    # )
    # cursor = connection.cursor()
    # cursor.execute(
    #     "CREATE TABLE if not exists moistures (Times DATETIME, moisture INT)"
    # )

    client.loop_forever()
