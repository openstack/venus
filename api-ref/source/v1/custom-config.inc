.. -*- rst -*-

Custom Config
=============

Users can customize some important configurations, such as the retention days of ElasticSearch index.
However, only these configurations can be read now, implement modification later.

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

**Example: JSON request**


.. literalinclude:: ./samples/custom-config/custom-config-show-response.json
   :language: javascript
