from unittest import mock

from django.template import TemplateDoesNotExist

import templated_email


def test_send_email(settings):
    """
    If there is an HTML version of the template, the email should be
    sent with both a text and HTML version.
    """
    email = "test@example.com"
    subject = "Test Email"
    template_name = "myapp/template"

    with mock.patch(
        "templated_email.utils.render_template",
        autospec=True,
        return_value="template content",
    ) as mock_render:
        with mock.patch(
            "templated_email.mail.send_mail", autospec=True
        ) as mock_mail:
            templated_email.send_email(
                subject=subject, template=template_name, to=email
            )

    assert mock_render.call_count == 2
    assert mock_mail.call_count == 1
    assert mock_mail.call_args[1] == {
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "html_message": "template content",
        "message": "template content",
        "recipient_list": [email],
        "subject": subject,
    }


def test_send_email_no_html(settings):
    """
    If there is no HTML version of a template, the email should only be
    sent with text content.
    """

    def render_text_only(template, extension="txt", context=dict()):
        if extension != "txt":
            raise TemplateDoesNotExist(msg="foo")

        return "template content"

    email = "test@example.com"
    subject = "Test Email"
    template_name = "myapp/template"

    with mock.patch(
        "templated_email.utils.render_template",
        autospec=True,
        side_effect=render_text_only,
    ) as mock_render:
        with mock.patch(
            "templated_email.mail.send_mail", autospec=True
        ) as mock_mail:
            templated_email.send_email(
                subject=subject, template=template_name, to=email
            )

    assert mock_render.call_count == 2
    assert mock_mail.call_count == 1
    assert mock_mail.call_args[1] == {
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "html_message": None,
        "message": "template content",
        "recipient_list": [email],
        "subject": subject,
    }
