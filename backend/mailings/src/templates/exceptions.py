from fastapi import HTTPException, status

from jinja2 import Environment

from backend.mailings.src.templates.texts import (
    no_templates_found_message,
    template_not_found_message,
    invalid_html_exception_message,
    invalid_html_exception_wrong_decl_message,
    invalid_html_exception_no_html_tag_message,
    invalid_html_exception_no_head_tag_message,
    invalid_html_exception_no_body_tag_message
)


class NoTemplateFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_templates_found_message[language]


class TemplateNotFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, template_name: str, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        jinja_template = Environment().from_string(template_not_found_message[language])  # TODO Check Jinja code
        self.detail = jinja_template.render(template_name=template_name)


class InvalidHTMLException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self,
                 invalid_decl: bool = False,
                 invalid_html_tag: bool = False,
                 invalid_head_tag: bool = False,
                 invalid_body_tag: bool = False,
                 language: str = "en",
                 **kwargs):
        super().__init__(self.status_code, **kwargs)

        final_message = invalid_html_exception_message[language]

        if invalid_decl:
            " ".join([final_message, invalid_html_exception_wrong_decl_message[language]])
        if invalid_html_tag:
            " ".join([final_message, invalid_html_exception_no_html_tag_message[language]])
        if invalid_head_tag:
            " ".join([final_message, invalid_html_exception_no_head_tag_message[language]])
        if invalid_body_tag:
            " ".join([final_message, invalid_html_exception_no_body_tag_message[language]])

        self.detail = final_message


class TemplateAlreadyExistsException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, language: str = "en", **kwargs):
        super().__init__(self.status_code, **kwargs)
        self.detail = no_templates_found_message[language]
