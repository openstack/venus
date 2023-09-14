.. -*- rst -*-

Anomaly Detect
==============

Users can add, delete, modify and query anomaly rules, query and delete anomaly records.


Add anomaly rule
~~~~~~~~~~~~~~~~

.. rest_method:: POST /v1/anomaly/rule

Add an anomaly rule.

Request
-------

.. rest_parameters:: parameters.yaml

   - title: add_rule_title
   - desc: add_rule_desc
   - keyword: add_rule_keyword
   - log_type: add_rule_log_type
   - module: add_rule_module

**Example Add Anomaly rule request:**


.. literalinclude:: ./samples/anomaly-detect/add-anomaly-rule-request-curl.json
   :language: javascript

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example Add An Anomaly Rule response:**


.. literalinclude:: ./samples/anomaly-detect/add-anomaly-rule-show-response.json
   :language: javascript


Get anomaly rule
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


Update anomaly rule
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

**Example Update An Anomaly Rule request:**


.. literalinclude:: ./samples/anomaly-detect/update-anomaly-rule-request.json
   :language: javascript

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 1

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example Update An Anomaly Rule Success response:**


.. literalinclude:: ./samples/anomaly-detect/update-anomaly-rule-success-response.json
   :language: javascript


**Example Update An Anomaly Rule Failed response:**


.. literalinclude:: ./samples/anomaly-detect/update-anomaly-rule-failed-response.json
   :language: javascript


Get anomaly rule list
~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: GET /v1/anomaly/rule/list

Get all anomaly rules.

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Request
-------

.. rest_parameters:: parameters.yaml

   - title: rule_title
   - desc: rule_desc
   - keyword: rule_keyword
   - log_type: rule_log_type
   - module: rule_module
   - flag: rule_flag
   - page_num: page_num
   - page_size: page_size

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/anomaly-detect/get-anomaly-rule-list-show-response.json
   :language: javascript


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

**Example Get Anomaly record request:**


.. literalinclude:: ./samples/anomaly-detect/get-anomaly-record-request-curl.json
   :language: javascript

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/anomaly-detect/get-anomaly-record-show-response.json
   :language: javascript


Delete anomaly record
~~~~~~~~~~~~~~~~~~~~~

.. rest_method:: DELETE /v1/anomaly/record/{id}

Delete anomaly record.

Request
-------

.. rest_parameters:: parameters.yaml

   - id: record_id

**Example Get Anomaly record request:**


.. literalinclude:: ./samples/anomaly-detect/delete-anomaly-record-request-curl.json
   :language: javascript

Response codes
--------------

.. rest_status_code:: success ../status.yaml

   - 0

.. rest_status_code:: error ../status.yaml

   - -1

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/anomaly-detect/delete-anomaly-record-show-response.json
   :language: javascript
