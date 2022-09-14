.. -*- rst -*-

Search logs download
====================

Search logs download of all modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/logs/download

Download the search logs of all Venus modules.

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


.. literalinclude:: ./samples/search-log/search-logs-download-show-response.json
   :language: javascript
