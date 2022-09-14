.. -*- rst -*-

Search Params
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
