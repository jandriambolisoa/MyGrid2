import os
from html.parser import HTMLParser

from constants import VALID_HTML_DECL
from exceptions import InvalidHTMLException

def get_contents_folder():
    folderpath = os.path.normpath(os.path.join(__file__, "contents"))
    return folderpath.replace("\\", "/")

class HTMLContentValidator(HTMLParser):
    """This class parse an HTML string and validate its content.
    It's looking for a file type declaration, a html tag,
    a head tag and a body tag. For each tag, it checks if
    their number is pair (this should mean the tag has a
    start and an end)."""
    def __init__(self, language: str = "en"):
        super().__init__()
        self.language = language
        self.has_html_decl = 0
        self.has_html_tag = 0
        self.has_head_tag = 0
        self.has_body_tag = 0

    def handle_starttag(self, tag, attrs):
        if tag == "html":
            self.has_html_tag += 1
        if tag == "head":
            self.has_head_tag += 1
        if tag == "body":
            self.has_body_tag += 1

    def handle_endtag(self, tag):
        if tag == "html":
            self.has_html_tag += 1
        if tag == "head":
            self.has_head_tag += 1
        if tag == "body":
            self.has_body_tag += 1

    def handle_decl(self, decl):
        if decl.lower() in VALID_HTML_DECL:
            self.has_html_decl += 1

    def feed(self, data):
        super().feed(data)

        if (not self.has_html_decl
                or self.has_html_tag%2 == 1
                or self.has_head_tag%2 == 1
                or self.has_body_tag%2 == 1
                or not self.has_html_tag
                or not self.has_head_tag
                or not self.has_body_tag):
            raise InvalidHTMLException(
                invalid_decl= not self.has_html_decl,
                invalid_html_tag= self.has_html_tag%2 if self.has_html_tag > 0 else True,
                invalid_head_tag= self.has_head_tag%2 if self.has_head_tag > 0 else True,
                invalid_body_tag= self.has_body_tag%2 if self.has_body_tag > 0 else True,
                language=self.language
            )

def check_html_content(content, language: str = "en"):
    parser = HTMLContentValidator(language)
    parser.feed(content)
