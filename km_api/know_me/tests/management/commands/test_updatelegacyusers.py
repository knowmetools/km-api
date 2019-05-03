from know_me import models
from know_me.management.commands.updatelegacyusers import Command


# for user in legacy_users:
#     query = Q(user__email_address__email=user.email)
#     query &= Q(user__email_address__is_verified=True)
#     KMUser.objects.filter(query).update(is_legacy_user=True)


def test_handle_match_email(email_factory, legacy_user_factory):
    """
    If the email address of a legacy user matches a verified email, the
    Know Me user corresponding to the owner of the email address should
    be marked as a legacy user.
    """
    email_inst = email_factory(
        is_verified=True, user__registration_signal__send=True
    )
    legacy_user_factory(email=email_inst.email)

    command = Command()
    command.handle()
    email_inst.refresh_from_db()

    assert email_inst.user.km_user.is_legacy_user
    assert not models.LegacyUser.objects.exists()


def test_handle_match_email_unverified(email_factory, legacy_user_factory):
    """
    If a legacy email matches a current user's email but the email is
    unverified, no action should be taken.
    """
    email_inst = email_factory(
        is_verified=False, user__registration_signal__send=True
    )
    legacy_user_factory(email=email_inst.email)

    command = Command()
    command.handle()
    email_inst.refresh_from_db()

    assert not email_inst.user.km_user.is_legacy_user
