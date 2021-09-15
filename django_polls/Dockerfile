
RUN mkdir -p /code

COPY . /code/.

WORKDIR /code

RUN pip install pipenv && pipenv install

CMD sh docker-entrypoint.sh
