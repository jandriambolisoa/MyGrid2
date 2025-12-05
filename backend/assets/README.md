# MyGrid2 : assets
This python package is a MyGrid2 microservice. 

assets is responsible for stocking and managing images and 3d models.

## Deployment
This fastapi app is excepted to be deployed from MyGrid2 root, with uvicorn.

    uvicorn backend.assets.main:app --port <port-number>

## .env
    DEBUG (activate fastapi auto docs)
