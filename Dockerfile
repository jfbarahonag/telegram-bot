# distro de linux
FROM alpine:3.15
# sistema base
RUN apk add --no-cache python3-dev \
    && apk update \
    && apk add py-pip \
    && mkdir app
    # establece el directorio de trabajo llamado app
WORKDIR /app
# copiar todo a la carpeta /app
COPY . /app
# instalar los requerimientos
RUN pip3 --no-cache install -r requirements.txt
# exponer el puerto del servidor (que esta encapsulado por docker)
# EXPOSE 4000
# ejecutar la app
CMD [ "python3", "bot.py" ]
