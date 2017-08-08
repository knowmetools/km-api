========
REST API
========

The API is available at the following URLs. The endpoints given should be appended to the base URL.

Production
  https://new-api.knowmetools.com

Staging
  https://dev.new-api.knowmetools.com

-------------
Authorization
-------------

This API uses tokens to authenticate and authorize requests. Authentication is done by setting the ``Authorization: Token <token content>`` on your requests.


-------------
API Endpoints
-------------

.. toctree::
    :maxdepth: 2

    API/authentication
    API/account
    API/know-me-emergency
    API/know-me-gallery
    API/know-me-profile
