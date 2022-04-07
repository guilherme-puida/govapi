FROM python:3.10-slim

RUN update-ca-certificates
RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY . /code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
