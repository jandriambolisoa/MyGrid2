# MyGrid2 : mails-distrib
This python package is a MyGrid2 microservice. 

mails-distrib is responsible for stocking mails templates (not images, only html),
writing emails from templates and sending emails.

## Deployment
This fastapi app is excepted to be deployed from MyGrid2 root, with uvicorn at port 8001.

    uvicorn backend/mails-distrib/main:app --port 8001

## .env
    DEBUG (activate fastapi auto docs)

    MAIL_HOST
    MAIL_CRYPTAGE
    MAIL_PORT
    MAIL_USERLABEL (name appearing as sender)
    MAIL_ALIAS (define email's sender, alias@domain)
    MAIL_DOMAIN (define email's sender, alias@domain)
    MAIL_LOGIN
    MAIL_PASSWORD
