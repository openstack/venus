.. -*- rst -*-

Anomaly Detect
==============

Users can add, delete, modify and query anomaly rules, query and delete anomaly records.


Get Anomaly Rule
~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/anomaly/rule/{id}

Get information of an anomaly rule.

Request
-------

.. rest_parameters:: parameters.yaml

   - id: rule_id

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example Get An Anomaly Rule response:**


.. literalinclude:: ./samples/anomaly-detect/get-anomaly-rule-show-response.json
   :language: javascript


Update Anomaly Rule
~~~~~~~~~~~~~~~~~~~

.. rest_method:: POST /v1/anomaly/rule/{id}

Update an anomaly rule.

Request
-------

.. rest_parameters:: parameters.yaml

   - id: rule_id
   - title: rule_title
   - desc: rule_desc
   - keyword: rule_keyword
   - log_type: rule_log_type
   - module: rule_module
   - flag: rule_flag

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - -1


Delete anomaly rule
~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: DELETE /v1/anomaly/rule/{id}

Delete anomaly rule.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - -1

Request
-------

.. rest_parameters:: parameters.yaml

   - id: rule_id

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/anomaly-detect/delete-anomaly-rule-show-response.json
   :language: javascript


Get anomaly record
~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/anomaly/record/list

Get all anomaly records.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Request
-------

.. rest_parameters:: parameters.yaml

   - title: title
   - log_type: anomaly_log_type
   - module: module_name
   - start_time: start_time
   - end_time: end_time
   - page_num: page_num
   - page_size: page_size

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/anomaly-detect/get-anomaly-record-show-response.json
   :language: javascript


Delete anomaly record
~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: DELETE /v1/anomaly/record/{id}

Delete anomaly record.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Request
-------

.. rest_parameters:: parameters.yaml

   - id: record_id

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/anomaly-detect/delete-anomaly-record-show-response.json
   :language: javascript
