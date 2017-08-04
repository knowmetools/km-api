from know_me import serializers


def test_create(km_user_factory):
    """
    Saving a serializer containing valid data should create a new
    emergency contact attached to the given KMUser.
    """
    km_user = km_user_factory()
    data = {
        'name': 'My Name',
        'relation': 'My relation',
        'phone_number': '19199911919',
        'alt_phone_number': '18008008000',
        'email': 'email@gmail.com'
    }

    serializer = serializers.EmergencyContactSerializer(data=data)
    assert serializer.is_valid()

    emergencycontact = serializer.save(km_user=km_user)

    assert emergencycontact.name == data['name']


def test_serialize(api_rf, emergency_contact_factory, serializer_context):
    """
    Test serilaizing emergency contact
    """
    emergencycontact = emergency_contact_factory()

    serializer = serializers.EmergencyContactSerializer(
        emergencycontact,
        context=serializer_context)

    url_request = api_rf.get(emergencycontact.get_absolute_url())

    expected = {
        'id': emergencycontact.id,
        'url': url_request.build_absolute_uri(),
        'name': emergencycontact.name,
        'relation': emergencycontact.relation,
        'phone_number': emergencycontact.phone_number,
        'alt_phone_number': emergencycontact.alt_phone_number,
        'email': emergencycontact.email
    }

    assert serializer.data == expected


def test_update(km_user_factory, emergency_contact_factory):
    """
    Testing update for emergency contacts
    """
    emergency_contact = emergency_contact_factory()
    data = {
        'alt_phone_number': '3213219876'
    }

    serializer = serializers.EmergencyContactSerializer(
        emergency_contact,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    emergency_contact.refresh_from_db()

    assert emergency_contact.alt_phone_number == data['alt_phone_number']
