.. -*- rst -*-

Search API
==========

Users can search, download and analyze logs, instance callchain.

Get search params
~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/params

Get the value list of search parameter, such as host list, module list.

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


Search logs
~~~~~~~~~~~

.. rest_method:: GET /v1/search/logs

Search logs by host name, modules name, level, etc.

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


Download logs
~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/logs/download

Download the logs searched.

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


Analyse logs
~~~~~~~~~~~~

.. rest_method:: GET v1/search/analyse/logs

Analyse logs of by host_name, module_name, program_name, level, etc.

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

Search typical error log, such as error logs of all modules, RabbitMQ related error logs, MariaDB related error logs.

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

Get instance request id list.

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


Search instance callchain(Only create operation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/search/instance/callchain

Search instance callchain, export the logs of nova-api, nova-conductor, nova-scheduler and nova-compute.

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
   - uuid: uuid

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/search-log/search-instance-callchain-show-response.json
   :language: javascript
