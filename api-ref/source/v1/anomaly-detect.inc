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

Response
--------

**Example: JSON response**


.. literalinclude:: ./samples/anomaly-detect/get-anomaly-detect-show-response.json
   :language: javascript
