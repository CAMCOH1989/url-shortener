url-shortener
*************
Url shortening & redirecting back to original.

.. contents:: **Contents**
   :depth: 3

Usage
=====
.. code-block:: shell

 # Migrate db
 docker run -it --rm \
        --env psql -h 0.0.0.0 -p 5452 -U api --dbname=url_shortener -f initdb.sql



 #createURL
 /api/urls
	 POST
	 GET

 # Run HTTP API
 docker run -d --rm -p8080:8080 \
     --env CHEKIST_AMQP_URL=amqp://guest:guest@${HOST}/ \
     --env CHEKIST_PG_URL=postgresql://api:hackme@${HOST}:5432/chekist \
     --volume ${HOST_DIR}:/files \
     janeturueva/chekist

/api/url/:id
	GET
	DELETE

/r/:shortLink
	GET

