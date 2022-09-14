.. -*- rst -*-

Search logs
===========

Search logs of all modules
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/logs

List host_name, module_name,program_name,level more informations for all Venus modules logs.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example: JSON request**


.. literalinclude:: ./samples/search-log/search-logs-show-response.json
   :language: javascript
