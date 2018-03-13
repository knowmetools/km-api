from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rest_framework.reverse import reverse

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
        auto_now=True,
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

    def get_absolute_url(self):
        """
        Get the URL of the instance's detail view.

        Returns:
            The absolute URL of the instance's detail view.
        """
        return reverse('know-me:journal:entry-detail', kwargs={'pk': self.pk})

    def get_comments_url(self):
        """
        Get the URL of the instance's comment list view.

        Returns:
            The absolute URL of the instance's comment list view.
        """
        return reverse(
            'know-me:journal:entry-comment-list',
            kwargs={'pk': self.pk})

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


class EntryComment(mixins.IsAuthenticatedMixin, models.Model):
    """
    A comment on a Journal Entry.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The time that the comment was created.'),
        verbose_name=_('created at'))
    entry = models.ForeignKey(
        'journal.Entry',
        help_text=_('The entry that the comment is attached to.'),
        on_delete=models.CASCADE,
        related_name='comments',
        related_query_name='comment',
        verbose_name=_('entry'))
    text = models.TextField(
        help_text=_('The body of the comment.'),
        verbose_name=_('text'))
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('The time that the comment was last updated.'),
        verbose_name=_('updated at'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text=_('The user who made the comment.'),
        on_delete=models.CASCADE,
        related_name='journal_comments',
        related_query_name='journal_comment',
        verbose_name=_('user'))

    class Meta:
        verbose_name = _('entry comment')
        verbose_name_plural = _('entry comments')

    def has_object_destroy_permission(self, request):
        """
        Check destroy permissions on the instance for a request.

        The user who made the comment, the owner of the journal, and any
        account administrators of the journal owner are able to delete a
        journal comment.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has destroy
            permissions on the instance.
        """
        return (
            request.user == self.user
            or self.entry.has_object_write_permission(request))

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
        return self.entry.has_object_read_permission(request)

    def has_object_update_permission(self, request):
        """
        Check update perissions on the instance for a request.

        Only the user who created the comment is allowed to update it.

        Args:
            request:
                The request to check permissions for.

        Returns:
            A boolean indicating if the requesting user has update
            permissions on the instance.
        """
        return request.user == self.user

    def has_object_write_permission(self, request):
        """
        Check write permissions on the instance for a request.

        No one is granted blanket write permissions. More granular
        permissions are handled by the 'destroy' and 'update' checks.

        Returns:
            ``False``
        """
        return False
