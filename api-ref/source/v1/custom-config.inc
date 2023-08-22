.. -*- rst -*-

Custom Config
=============

Users can customize some important configurations, such as the retention days of ElasticSearch index.

Get custom config
~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/custom_config

Get all custom config.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/custom-config/get-custom-config-show-response.json
   :language: javascript


Set custom config
~~~~~~~~~~~~~~~~~

.. rest_method:: POST /v1/custom_config

Set one custom config.

Request
-------

.. rest_parameters:: parameters.yaml

   - id: id
   - value: value

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/custom-config/set-custom-config-show-response.json
   :language: javascript
