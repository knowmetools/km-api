import datetime

from know_me import models
from know_me.management.commands.sendreminderemails import Command


def test_send_reminder_emails(reminder_email_subscriber_factory):
    sub = reminder_email_subscriber_factory()

    command = Command()
    sub.user.primary_email.email = "test@knowme.works"
    sent = command.send_reminder_email(sub)

    assert sent


def test_send_log(reminder_email_log_factory):
    command = Command()
    frequency = "Daily"
    command.send_reminder_emails(frequency)

    log = models.ReminderEmailLog.objects.filter(schedule_frequency=frequency)
    assert log.count() == 1


def test_last_sent(reminder_email_log_factory):
    command = Command()
    frequency = "Daily"
    last_sent = command.last_date_sent(frequency)
    assert last_sent is None

    now = datetime.datetime.now()
    log = models.ReminderEmailLog(
        sent_date=now, subscriber_count=1, schedule_frequency=frequency
    )
    log.save()
    last_sent = command.last_date_sent(frequency)
    assert now.date() == last_sent


def test_handle(reminder_email_log_factory):
    """
    The entry point into the command should delegate to the methods
    responsible for each task in the command.
    """
    command = Command()
    command.handle()

    frequency = "Daily"
    log = models.ReminderEmailLog.objects.filter(schedule_frequency=frequency)
    assert log.count() == 1

    command.handle()

    log = models.ReminderEmailLog.objects.filter(schedule_frequency=frequency)
    assert log.count() == 1
