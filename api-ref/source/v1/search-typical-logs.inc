.. -*- rst -*-

Search typical logs
===================

Search typical error logs of all modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET v1/search/typical/logs

Search host_name, module_name,program_name,level more informations for all Venus modules typical error  logs.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - 0
   - -1

Response
--------

**Example: JSON request**


.. literalinclude:: ./samples/search-log/search-typical-logs-show-response.json
   :language: javascript
