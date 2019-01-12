from know_me.profile import serializers


def test_serialize(api_rf, profile_item_factory, profile_topic_factory):
    """
    Test serializing a profile topic.
    """
    topic = profile_topic_factory()
    api_rf.user = topic.profile.km_user.user
    request = api_rf.get(topic.get_absolute_url())

    profile_item_factory(topic=topic)
    profile_item_factory(topic=topic)

    serializer = serializers.ProfileTopicDetailSerializer(
        topic, context={"request": request}
    )

    item_serializer = serializers.ProfileItemListSerializer(
        topic.items.all(), context={"request": request}, many=True
    )
    list_serializer = serializers.ProfileTopicListSerializer(
        topic, context={"request": request}
    )

    additional = {"items": item_serializer.data}

    expected = dict(list_serializer.data.items())
    expected.update(additional)

    assert serializer.data == expected


def test_validate():
    """
    Test validating the attributes required to create a new profile
    topic.
    """
    data = {"is_detailed": True, "name": "Test Topic"}
    serializer = serializers.ProfileTopicDetailSerializer(data=data)

    assert serializer.is_valid()
