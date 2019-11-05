FROM python:3.7-buster

ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ARG AWS_DEFAULT_REGION
ENV AWS_DEFAULT_REGION ${AWS_DEFAULT_REGION}
ENV PYTHONPATH "${PYTHONPATH}:/app/src/main/python"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

EXPOSE 5000

CMD [ "src/main/python/server/app.py" ]
