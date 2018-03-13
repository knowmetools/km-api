from django.db import models
from django.utils.translation import ugettext_lazy as _


from permission_utils import model_mixins as mixins


def get_entry_attachment_upload_path(entry, filename):
    """
    Get the path to upload a journal entry's attachment to.

    Args:
        entry:
            The Journal entry that the file will be attached to.
        filename:
            The attachment's original filename.

    Returns:
        The path to upload the attachment to.
    """
    return 'know-me/users/{id}/journal/attachments/{file}'.format(
        file=filename,
        id=entry.km_user.id)


class Entry(mixins.IsAuthenticatedMixin, models.Model):
    """
    An entry in the journal that describes the events of a particular
    time period.
    """
    attachment = models.FileField(
        blank=True,
        help_text=_('The file attached to the journal entry.'),
        upload_to=get_entry_attachment_upload_path,
        verbose_name=_('attachment'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time that the entry was created.'),
        verbose_name=_('created at'))
    km_user = models.ForeignKey(
        'know_me.KMUser',
        help_text=_('The Know Me user who owns the entry.'),
        on_delete=models.CASCADE,
        related_name='journal_entries',
        related_query_name='journal_entry',
        verbose_name=_('Know Me user'))
    text = models.TextField(
        help_text=_('The text that the entry contains.'),
        verbose_name=_('text'))
    updated_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time that the entry was last updated.'),
        verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('journal entry')
        verbose_name_plural = _('journal entries')

    def __str__(self):
        """
        Get a string representation of the instance.

        Returns:
            A string containing the time that the entry was published.
        """
        return 'Entry for {}'.format(self.created_at)

    def has_object_read_permission(self, request):
        """
        Check read permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has read
            permissions on the instance.
        """
        return self.km_user.has_object_read_permission(request)

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has write
            permissions on the instance.
        """
        return self.km_user.has_object_write_permission(request)
