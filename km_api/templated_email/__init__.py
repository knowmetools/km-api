"""Utility for sending out templated email.
"""

from django.conf import settings
from django.core import mail
from django.template import TemplateDoesNotExist

from templated_email import utils


def send_email(to, subject, template, context=dict()):
    """
    Send a template email.

    Args:
        to (str):
            The email address to send the email to.
        subject (str):
            The subject line of the email to send.
        template (str):
            The base template name to render.
        context (:obj:`dict`, optional):
            The context to render the email with. Defaults to an empty
            dictionary.
    """
    text_content = utils.render_template(template, context=context)

    try:
        html_content = utils.render_template(
            template, context=context, extension="html"
        )
    except TemplateDoesNotExist:
        html_content = None

    mail.send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        html_message=html_content,
        message=text_content,
        recipient_list=[to],
        subject=subject,
    )
