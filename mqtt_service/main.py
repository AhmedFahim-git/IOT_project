import paho.mqtt.client as mqtt
from mysql.connector import connect, Error
import json
from datetime import datetime, timezone

import time

topic = "Test"
username = "user"
password = "password"
broker_hostname = "localhost"
port = 1883

db_host = "localhost"
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


def write_db(timestamp: str, moisture: int, humidity: float, temp_celsius: float):
    cursor.execute(
        f"INSERT into moistures (reading_timestamp, moisture, humidity, temp_celsius) values ('{timestamp}', {moisture}, {humidity}, {temp_celsius})"
    )
    connection.commit()


def on_message(client, userdata, message):
    parsed_message = json.loads(str(message.payload.decode("utf-8")))
    write_db(
        timestamp=datetime.fromtimestamp(
            parsed_message["timestamp"], tz=timezone.utc
        ).isoformat(),
        moisture=int(
            parsed_message["moisture"],
        ),
        humidity=float(parsed_message["humidity"]),
        temp_celsius=float(parsed_message["temp_celsius"]),
    )
    # print("Received message: ", str(message.payload.decode("utf-8")))


def init_db():
    cursor.execute(
        "CREATE TABLE if not exists moistures (reading_timestamp DATETIME NOT NULL PRIMARY KEY, moisture INT, humidity FLOAT, temp_celsius FLOAT)"
    )


def main():
    client = mqtt.Client("MQTT_database_service")
    client.username_pw_set(username=username, password=password)
    client.on_connect = on_connect
    client.on_message = on_message

    init_db()

    client.connect(broker_hostname, port)

    client.loop_forever()


if __name__ == "__main__":
    print("here")
    main()
