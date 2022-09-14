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

   - 1

.. rest_status_code:: error ../status.yaml

   - 0
   - -1

Request
-------

.. rest_parameters:: parameters.yaml

   - host_name: host_name
   - module_name: module_name
   - program_name: program_name
   - level: level
   - user_id: user_id
   - project_id: project_id
   - query: query
   - start_time: start_time
   - page_size: page_size
   - index_type: index_type

Response
--------

**Example: JSON request**


.. literalinclude:: ./samples/search-log/search-logs-download-show-response.json
   :language: javascript
