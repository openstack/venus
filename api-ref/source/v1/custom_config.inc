.. -*- rst -*-

Custom Config
=============

Get Custom Config
~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /custom_config

Get the value of all custom config.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example: JSON request**


.. literalinclude:: ./samples/custom-config/custom-config-show-response.json
   :language: javascript
