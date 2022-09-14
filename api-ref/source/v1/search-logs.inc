.. -*- rst -*-

Search logs
===========

Search logs of all modules
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/logs

Search logs.

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
   - end_time: end_time
   - page_num: page_num
   - page_size: page_size
   - index_type: index_type

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - 0
   - -1

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-logs-show-response.json
   :language: javascript
