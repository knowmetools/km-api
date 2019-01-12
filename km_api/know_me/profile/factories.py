import factory


class ListEntryFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ``ListEntry`` instances.
    """

    profile_item = factory.SubFactory(
        "know_me.profile.factories.ProfileItemFactory"
    )
    text = factory.Sequence(lambda n: "List Entry {}".format(n))

    class Meta:
        model = "profile.ListEntry"


class MediaResourceCategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ``MediaResourceCategory`` instances.
    """

    km_user = factory.SubFactory("know_me.factories.KMUserFactory")
    name = factory.Sequence(lambda n: "Category {n}".format(n=n))

    class Meta:
        model = "profile.MediaResourceCategory"


class MediaResourceFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ``MediaResource`` instances.
    """

    file = factory.django.FileField(
        data=b"The quick brown fox jumps over the lazy dog.",
        filename="foo.txt",
    )
    km_user = factory.SubFactory("know_me.factories.KMUserFactory")
    name = factory.Sequence(lambda n: "Resource {}".format(n))

    class Meta:
        model = "profile.MediaResource"


class ProfileFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ``Profile`` instances.
    """

    km_user = factory.SubFactory("know_me.factories.KMUserFactory")
    name = factory.Sequence(lambda n: "Profile {}".format(n))

    class Meta:
        model = "profile.Profile"


class ProfileItemFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ``ProfileItem`` instances.
    """

    name = factory.Sequence(lambda n: "Item {}".format(n))
    topic = factory.SubFactory("know_me.profile.factories.ProfileTopicFactory")

    class Meta:
        model = "profile.ProfileItem"


class ProfileTopicFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating ``ProfileTopic`` instances.
    """

    name = factory.Sequence(lambda n: "Topic {}".format(n))
    profile = factory.SubFactory("know_me.profile.factories.ProfileFactory")

    class Meta:
        model = "profile.ProfileTopic"
