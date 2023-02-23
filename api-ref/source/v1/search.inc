.. -*- rst -*-

Search API
=============

Get Search Params
~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/params

Get the value list of one search parameter.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Request
-------

.. rest_parameters:: parameters.yaml

   - type: param_type
   - module_name: module_name
   - index_type: index_type

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-params-show-response.json
   :language: javascript
.. -*- rst -*-


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
.. -*- rst -*-


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

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-logs-download-show-response.json
   :language: javascript
.. -*- rst -*-


Search analyse logs of all modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET v1/search/analyse/logs

Search host_name, module_name,program_name,level more informations for all Venus modules analyse logs.

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

   - group_name: group_name
   - host_name: host_name
   - module_name: module_name
   - program_name: program_name
   - level: level
   - start_time: start_time
   - end_time: end_time

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-analyse-logs-show-response.json
   :language: javascript
.. -*- rst -*-


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

Request
-------

.. rest_parameters:: parameters.yaml

   - type: typical_log_type
   - start_time: start_time
   - end_time: end_time

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-typical-logs-show-response.json
   :language: javascript
.. -*- rst -*-


Search the list of instance request id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET v1/search/instance/request_ids

Search instance request id from a start time to end time

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

   - start_time: start_time
   - end_time: end_time

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-instance-request-ids-show-response.json
   :language: javascript
.. -*- rst -*-


Search instance callchain of all modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/instance/callchain

Search nova-api, nova-conductor, nova-scheduler and nova-compute informations for all Venus modules instance callchain

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

   - request_id: request_id

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-instance-callchain-show-response.json
   :language: javascript
