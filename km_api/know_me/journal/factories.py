import factory


class EntryCommentFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``EntryComment`` instances.
    """
    entry = factory.SubFactory('know_me.journal.factories.EntryFactory')
    text = factory.Sequence(lambda n: 'Comment #{}'.format(n))
    user = factory.SubFactory('factories.UserFactory')

    class Meta:
        model = 'journal.EntryComment'


class EntryFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Entry`` instances.
    """
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')
    text = factory.Sequence(lambda n: 'Journal Entry {}'.format(n))

    class Meta:
        model = 'journal.Entry'
