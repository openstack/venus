.. -*- rst -*-

Custom Config
=============

Users can customize some important configurations, such as the retention days of ElasticSearch index.

Get Custom Config
~~~~~~~~~~~~~~~~~~~~~

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
