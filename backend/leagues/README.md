# MyGrid2 : leagues
This python package is a MyGrid2 microservice. 

leagues is responsible for handling leagues inside MyGrid2 (crud, deep links
and shadow users).

## Deployment
This fastapi app is excepted to be deployed from MyGrid2 root, with uvicorn.

    uvicorn backend/mailings/main:app --port <port-number>

## .env
    DEBUG (activate fastapi auto docs)

## How it works
### Manage router
This router manages the leagues.