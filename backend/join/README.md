# MyGrid2 : join
This python package is a MyGrid2 microservice. 

join is responsible for handling leagues invitations inside 
MyGrid2 (deep links and shadow users).

## Deployment
This fastapi app is excepted to be deployed from MyGrid2 root, with uvicorn.

    uvicorn backend/mailings/main:app --port <port-number>

## .env
    DEBUG (activate fastapi auto docs)

## How it works
### join router
This router manages the leagues.