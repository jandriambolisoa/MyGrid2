from collections import defaultdict

no_templates_found_message = defaultdict(
    lambda: "No templates found.",
    {
        "fr": "Aucun template trouvé.",
    }
)

template_not_found_message = defaultdict(
    lambda: "The {{ template_name }} template was not found.",
    {
        "fr": "Le template {{ template_name }} n'existe pas.",
    }
)

invalid_html_exception_message = defaultdict(
    lambda: "HTML content invalid.",
    {
        "fr": "Le contenu HTML n'est pas valide.",
    }
)

invalid_html_exception_wrong_decl_message = defaultdict(
    lambda: "Wrong HTML doctype declaration.",
    {
        "fr": "La déclaration HTML n'est pas valide.",
    }
)

invalid_html_exception_no_html_tag_message = defaultdict(
    lambda: "An 'html' tag was not found.",
    {
        "fr": "Un tag 'html' n'a pas été trouvé.",
    }
)

invalid_html_exception_no_head_tag_message = defaultdict(
    lambda: "An 'head' tag was not found.",
    {
        "fr": "Un tag 'head' n'a pas été trouvé.",
    }
)

invalid_html_exception_no_body_tag_message = defaultdict(
    lambda: "An 'body' tag was not found.",
    {
        "fr": "Un tag 'body' n'a pas été trouvé.",
    }
)

template_already_exists_exception_messsage =  defaultdict(
    lambda: "This template already exists.",
    {
        "fr": "Ce template existe déjà.",
    }
)