FROM eclipse-mosquitto
COPY config/password.txt /mosquitto/config/
RUN mosquitto_passwd -U /mosquitto/config/password.txt
COPY config/mosquitto.conf /mosquitto/config/
CMD ["/usr/sbin/mosquitto","-c","/mosquitto/config/mosquitto.conf"]