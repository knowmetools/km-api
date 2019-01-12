"""Utility functions used to build an email message.
"""

from django.template.loader import render_to_string


def render_template(template_base, extension="txt", context=dict()):
    """
    Render a template's text version.

    Args:
        template_base (str):
            The template's base name.
        extension (:obj:`str`, optional):
            The file extension to render. Defaults to ``txt``.
        context (:obj:`dict`, optional):
            The context to render the template with.

    Returns:
        str:
            The result of rendering the given template.
    """
    template_name = "{base}.{extension}".format(
        base=template_base, extension=extension
    )

    return render_to_string(template_name, context)
