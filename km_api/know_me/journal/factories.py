import factory


class EntryFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating ``Entry`` instances.
    """
    km_user = factory.SubFactory('know_me.factories.KMUserFactory')
    text = factory.Sequence(lambda n: 'Journal Entry {}'.format(n))

    class Meta:
        model = 'journal.Entry'
