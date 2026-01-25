# MyGrid2

## How to install the backend
### Pre-requisites
    - python >=3.11
    - postgresql (https://www.postgresql.org/)
    - poetry (https://python-poetry.org/)
    - dbmate (https://github.com/amacneil/dbmate)

### Install for dev
1. Clone this repository.
2. cd in the repository and ``git checkout dev``
3. run ``poetry install``
4. run ``dbmate --migrations-dir ./backend/db/migrations --env TEST_DATABASE_URL --env-file ./backend/.env --schema-file ./backend/db/schema.sql up``
5. run the app ``poetry run uvicorn backend.main:app``(Warning: .env files must be created)