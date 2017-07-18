from unittest import mock

from templated_email import utils


def test_render_template_default():
    """
    This function should accept the template's base name, extension, and
    some context and then attempt to render the text version of that
    template with the provided context.
    """
    base_name = 'myapp/template'
    context = {
        'foo': 'bar',
    }

    expected_template = '{base}.txt'.format(base=base_name)

    with mock.patch(
            'templated_email.utils.render_to_string',
            autospec=True,
            return_value='template content') as mock_render:
        content = utils.render_template(base_name, context=context)

    assert mock_render.call_count == 1
    assert mock_render.call_args[0] == (expected_template, context)
    assert content == mock_render.return_value


def test_render_template_extension():
    """
    If an extension is given to the function, the template with the
    given extension should be used.
    """
    base_name = 'myapp/template'
    extension = 'html'
    context = {
        'foo': 'bar',
    }

    expected_template = '{base}.{extension}'.format(
        base=base_name,
        extension=extension)

    with mock.patch(
            'templated_email.utils.render_to_string',
            autospec=True,
            return_value='template content') as mock_render:
        content = utils.render_template(
            base_name,
            extension=extension,
            context=context)

    assert mock_render.call_count == 1
    assert mock_render.call_args[0] == (expected_template, context)
    assert content == mock_render.return_value
