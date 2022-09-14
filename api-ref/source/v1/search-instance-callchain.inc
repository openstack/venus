.. -*- rst -*-

Search instance callchain
=========================

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

**Example List Api Versions: JSON response**


.. literalinclude:: ./samples/search-log/search-instance-callchain-show-response.json
   :language: javascript
