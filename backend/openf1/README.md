# MyGrid2 : openf1
This python package is a MyGrid2 microservice. 

openf1 is responsible for fetching and returning live f1 sessions datas.

## OpenF1 API
OpenF1 is a free and open-source API that offers real-time and historical Formula 1 data.

## Deployment
This fastapi app is excepted to be deployed from MyGrid2 root, with uvicorn.

    uvicorn backend/mailings/main:app --port <port-number>

## .env
    DEBUG (activate fastapi auto docs)

    OPENF1_API_USERNAME
    OPENF1_API_PASSWORD
