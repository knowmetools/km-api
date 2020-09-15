import datetime

from django.core import management

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from know_me import models

from django.conf import settings


class Command(management.BaseCommand):
    """
    Management command to send out reminder emails
    """

    help = "Sends out a reminder email to users who opt into this service."

    def handle(self, *args, **options):
        """
        Execute the command.

        Args:
            *args:
                Positional arguments provided to the command.
            **options:
                Keyword arguments provided to the command.
        """
        today = datetime.datetime.now().date()
        frequency = "Daily"
        last_sent = self.last_date_sent(frequency)
        if last_sent is None or today != last_sent:
            self.send_reminder_emails(frequency)

        if today.weekday() == 6:
            """ If Sunday """
            frequency = "Weekly"
            last_sent = self.last_date_sent(frequency)
            today = datetime.datetime.now().date()
            if last_sent is None or today != last_sent:
                self.send_reminder_emails(frequency)

    def send_reminder_emails(self, frequency):
        self.stdout.write("Getting " + frequency + " email subscribers...")

        subs = models.ReminderEmailSubscriber.objects.filter(
            is_subscribed=True, schedule_frequency=frequency
        )  # noqa
        sub_count = subs.count()
        self.stdout.write(f"Reminder Email Subscriber Count: {sub_count}")

        now = datetime.datetime.now()
        log = models.ReminderEmailLog(
            sent_date=now,
            subscriber_count=subs.count(),
            schedule_frequency=frequency,
        )
        log.save()

        for sub in subs:
            self.send_reminder_email(sub)
        self.stdout.write(
            self.style.SUCCESS("Finished Sending " + frequency + " Emails")
        )

    def last_date_sent(self, frequency):
        emails = models.ReminderEmailLog.objects.filter(
            schedule_frequency=frequency
        ).order_by("-sent_date")
        if emails.count() > 0:
            return emails[0].sent_date.date()
        return None

    def send_reminder_email(self, sub):
        user_email = sub.user.primary_email.email
        name = sub.user.first_name
        uuid = sub.subscription_uuid
        unsub_link = "https://toolbox.knowmetools.com/know-me/reminder-email-unsubscribe/{}/{}/".format(  # noqa
            user_email, uuid
        )
        subject = "Journal Reminder Email"
        from_email = settings.DEFAULT_FROM_EMAIL
        template = settings.TEMPLATES[0]["DIRS"][0]
        template = template + "/know_me/emails/reminder.html"
        html_message = render_to_string(
            template, {"name": name, "subscription_url": unsub_link}
        )
        plain_message = strip_tags(html_message)

        mail_sent = send_mail(
            subject,
            plain_message,
            from_email,
            [user_email],
            html_message=html_message,
        )
        return mail_sent
