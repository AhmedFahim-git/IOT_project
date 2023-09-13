# Getting Started
![alt text for badge](https://github.com/AhmedFahim-git/IOT_project/actions/workflows/python_test.yml/badge.svg)


The following doesn't work. Sorry. Follow instructions.txt instead.

To start the services run

```bash
docker compose up --build
```

And to stop the services, in a separate terminal run

```bash
docker compose down
```

# Ports exposed

This exports the port 1883 for MQTT broker; the port 3306 for the MySQL database, and the port 8000 for the ML service. It also exposes port 8080 for adminer, which is used to inspect the database.

# Changes to implement

1. Currently all the passwords are used directly within the files. These should be extracted into a .env file instead.
2. I'm not sure about the range of values of sensor. So there might be some changes in the ML Service as well.
