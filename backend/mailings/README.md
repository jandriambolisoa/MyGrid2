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

## How it works
### Templates router
This router manages the templates.
A template is an HTML file containing the mail to send.
Best practice is to embed sources as urls as much as possible.
This service uses jinja2 to write emails, so templates can use the
jinja '{{ FIELD }}' syntax to include arguments to be overridden.

### Writing router
This router writes email based on the templates available.
The main use of this router is the 'read_template_fields' endpoint
to get expected fields. Trying to write with the wrong fields
will raise an exception.

### Sending router
This router is responsible for sending emails.
The 'send_email' endpoint carries finding the template, 
writing the mail and sending the mail operation. If you need
to send multiples emails, use this endpoint in a loop.

### Send an email with python
```
requests.post({{url}}/{{template_name}}, data = {
    "receiver": "an_adress@email.com",
    "subject": "The subject of the mail",
    "fields": {
        "fields": "to replace",
        "in": "the template"
    }
})
```
