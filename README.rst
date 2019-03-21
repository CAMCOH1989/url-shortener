url-shortener
*************
Url shortening & redirecting back to original.

.. contents:: **Contents**
   :depth: 3


Usage
=====
.. code-block:: shell

    # Download source
    git clone git@github.com:CAMCOH1989/url-shortener.git

    # Get to the working direction
    cd url-shortener

    # Install virtualenv & deps
    make devenv

    # Activate virtualenv
    source env/bin/activate

    # Run docker-compose environment
    docker-compose up -d

    # Run HTTP API
    url-shortener-api



REST API methods
================
API
----

Create new short URL.
~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

    http POST 0.0.0.0:8080/api/urls url='https://ya.ru'

.. code-block:: json

    {
        "data": {
        "created_at": "2019-03-20T13:10:24.909897+00:00",
        "short_url": "0.0.0.0:8080/r/ACc=",
        "url": "https://ya.ru",
        "url_id": 13,
        "visited_at": null
        }
    }

Get all URLs from database.
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

    http 0.0.0.0:8080/api/urls

.. code-block:: json

    {
        "data": [
            {
            "created_at": "2019-03-20T12:52:44.314142+00:00",
            "short_url": "0.0.0.0:8080/r/ACY=",
            "url": "https://raw.githubusercontent.com/JaneTurueva/chekist/master/README.rst",
            "url_id": 12,
            "visited_at": null
            },
            {
            "created_at": "2019-03-20T13:10:24.909897+00:00",
            "short_url": "0.0.0.0:8080/r/ACc=",
            "url": "https://ya.ru",
            "url_id": 13,
            "visited_at": null
            }
        ]
    }

Get one URL and short URL from database.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

    http POST 0.0.0.0:8080/api/urls/13

.. code-block:: json

    {
        "data": [
            {
            "created_at": "2019-03-20T13:10:24.909897+00:00",
            "short_url": "0.0.0.0:8080/r/ACc=",
            "url": "https://ya.ru",
            "url_id": 13,
            "visited_at": null
            }
        ]
    }

Delete URL from database.
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: shell

    http DELETE 0.0.0.0:8080/api/urls/13

.. code-block:: http

   HTTP/1.1 204 No Content


Redirect
--------
Make a redirect.
~~~~~~~~~~~~~~~~
.. code-block:: shell

    http GET 0.0.0.0:8080/r/ACc=

.. code-block:: http

   HTTP/1.1 302 Found

#TODO Make an auto cleaning.

Development
===========

.. code-block:: shell

    # Install virtualenv & deps
    make devenv

    # Activate virtualenv
    source env/bin/activate

    # Run docker-compose environment
    docker-compose up -d

    # Run HTTP API
    url-shortener-api
