# MyGrid2 : mailings
This python package is a MyGrid2 microservice. 

mailings is responsible for stocking mails templates (not images, only html),
writing emails from templates and sending emails.

## Deployment
This fastapi app is excepted to be deployed from MyGrid2 root, with uvicorn.

    uvicorn backend/mailings/main:app --port <port-number>

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
