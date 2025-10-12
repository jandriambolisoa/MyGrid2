# MyGrid2 : images
This python package is a MyGrid2 microservice. 

images is responsible for stocking and managing images.

## Deployment
This fastapi app is excepted to be deployed from MyGrid2 root, with uvicorn.

    uvicorn backend/mailings/main:app --port <port-number>

## .env
    DEBUG (activate fastapi auto docs)
