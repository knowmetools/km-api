from know_me import serializers
from know_me.serializers.profile_item_content_serializers import (
    ImageContentSerializer
)


def test_create(profile_topic_factory, serializer_context):
    """
    Saving a serializer with valid data should create a new profile
    item.
    """
    topic = profile_topic_factory()

    serializer_context['km_user'] = topic.profile.km_user

    data = {
        'name': 'My Profile Item',
        'image_content': {
            'description': 'Sample image content description.',
        }
    }

    serializer = serializers.ProfileItemSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid(), serializer.errors

    item = serializer.save(topic=topic)

    assert item.name == data['name']
    assert item.topic == topic

    content = item.image_content

    assert content.description == data['image_content']['description']


def test_serialize_image_item(
        api_rf,
        image_content_factory,
        profile_item_factory,
        serializer_context):
    """
    Test serializing a profile item.
    """
    item = profile_item_factory()
    image_content_factory(profile_item=item)

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context)

    image_content_serializer = ImageContentSerializer(
        item.image_content,
        context=serializer_context)

    url_request = api_rf.get(item.get_absolute_url())

    expected = {
        'id': item.id,
        'url': url_request.build_absolute_uri(),
        'name': item.name,
        'image_content': image_content_serializer.data,
    }

    assert serializer.data == expected


def test_update(profile_item_factory, serializer_context):
    """
    Saving a bound serializer with additional data should update the
    profile item bound to the serializer.
    """
    item = profile_item_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    item.refresh_from_db()

    assert item.name == data['name']


def test_update_image_content(image_content_factory, serializer_context):
    """
    Updating a profile item's image content with nested data should work
    properly.
    """
    content = image_content_factory(description='Old description.')
    item = content.profile_item

    data = {
        'image_content': {
            'description': 'New description.',
        },
    }

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    content.refresh_from_db()

    assert content.description == data['image_content']['description']
