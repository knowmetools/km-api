"""Utility functions for interacting with Layer.

See https://github.com/layerhq/layer-identity-token-python/blob/master/layer.py
"""

from django.conf import settings
from django.utils import timezone

from Crypto.PublicKey import RSA

import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm


# Attempt to use the algorithm from PyCrypto. If it fails, it means the
# ``cryptography`` module is installed, and will be used instead. The
# only reason we attempt this is so we don't have to require the
# ``cryptography`` module since it has a more involved install process.
try:
    jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))
except ValueError:
    pass


def generate_identity_token(user, nonce):
    """
    Create a Layer identity token.

    See the `Identity Token documentation`_ for details of the required
    payload.

    .. _`Identity Token documentation`:
        https://docs.layer.com/sdk/web/authentication#identity-token

    Args:
        user:
            The user to generate an identity token for.
        nonce:
            The nonce the user was provided by Layer.

    Returns:
        A JWT for the user to use as their identity token with Layer.
    """
    jwt_token = jwt.encode(
        payload={
            'iss': settings.LAYER_PROVIDER_ID,
            'prn': str(user.id),

            'iat': timezone.now(),
            'exp': timezone.now() + settings.LAYER_IDENTITY_EXPIRATION,

            'nce': nonce,
        },
        key=_read_rsa_private_key(),
        headers={
            'alg': 'RS256',
            'cty': 'layer-eit;v=1',
            'kid': settings.LAYER_KEY_ID,
            'typ': 'JWT',
        },
        algorithm='RS256'
    )

    return jwt_token.decode('utf8')


def _read_rsa_private_key(file_path=settings.LAYER_RSA_KEY_FILE_PATH):
    """
    Read an RSA private key and returns it in the PEM format.

    Args:
        file_path (str, optional):
            The path to the key file to read. Defaults to the value of
            the ``LAYER_RSA_KEY_FILE_PATH`` setting.

    Returns:
        The content of the RSA key in the given file encoded in the PEM
        format.
    """
    with open(file_path) as file:
        rsa_private_key = RSA.importKey(file.read())

    # return the key in PEM (textual) format
    return rsa_private_key.exportKey().decode('utf8')
