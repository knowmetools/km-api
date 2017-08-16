from know_me import models, serializers


def test_create(profile_factory):
    """
    Saving a serializer with valid data should create a new profile topic.
    """
    profile = profile_factory()
    data = {
        'name': 'Test Topic',
        'topic_type': models.ProfileTopic.TEXT,
    }

    serializer = serializers.ProfileTopicSerializer(data=data)
    assert serializer.is_valid()

    topic = serializer.save(profile=profile)

    assert topic.name == data['name']
    assert topic.topic_type == data['topic_type']
    assert topic.profile == profile


def test_serialize(
        api_rf,
        profile_item_factory,
        profile_topic_factory,
        serializer_context):
    """
    Test serializing a km_user.
    """
    topic = profile_topic_factory()
    profile_item_factory(topic=topic)
    profile_item_factory(topic=topic)

    serializer = serializers.ProfileTopicSerializer(
        topic,
        context=serializer_context)
    item_serializer = serializers.ProfileItemSerializer(
        topic.items.all(),
        context=serializer_context,
        many=True)

    url_request = api_rf.get(topic.get_absolute_url())
    item_list_request = api_rf.get(topic.get_item_list_url())

    expected = {
        'id': topic.id,
        'url': url_request.build_absolute_uri(),
        'name': topic.name,
        'topic_type': topic.topic_type,
        'items_url': item_list_request.build_absolute_uri(),
        'items': item_serializer.data,
        'permissions': {
            'read': topic.has_object_read_permission(item_list_request),
            'write': topic.has_object_write_permission(item_list_request),
        }
    }

    assert serializer.data == expected
