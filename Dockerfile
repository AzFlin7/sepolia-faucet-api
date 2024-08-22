FROM python:3.12.2

WORKDIR /usr/src/app

COPY . .

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x ./entrypoint.sh



ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
