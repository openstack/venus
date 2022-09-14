.. -*- rst -*-

Search instance request_ids
===========================

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

**Example: JSON request**


.. literalinclude:: ./samples/search-log/search-instance-request-ids-show-response.json
   :language: javascript
