.. -*- rst -*-

Search analyse logs
===================

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
