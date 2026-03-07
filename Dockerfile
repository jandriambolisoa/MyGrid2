FROM python:3.12
LABEL authors="jandriambolisoa"

WORKDIR /usr/src/app

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_VIRTUALENVS_CREATE=false

COPY poetry.lock ./
COPY pyproject.toml ./

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry install --no-interaction --no-ansi

COPY backend ./backend

CMD ["poetry", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]