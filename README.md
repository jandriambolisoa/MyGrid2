# MyGrid2

## How to install the backend
### Pre-requisites
    - python >=3.11
    - postgresql (https://www.postgresql.org/)
    - poetry (https://python-poetry.org/)
    - dbmate (https://github.com/amacneil/dbmate)

### Install
1. Clone this repository.
2. cd in the repository and ``git checkout dev``
3. run ``poetry install``
4. run ``cd backend; dbmate up``
5. cd back to the repo root and run ``poetry run uvicorn backend.main:app``
6. run the mailings microservice ``poetry run uvicorn backend.mailings.main:app --port 8002``
7. run the openf1 microservice ``poetry run uvicorn backend.openf1.main:app --port 8003``
