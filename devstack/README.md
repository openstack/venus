# Enabling Venus in DevStack

To enable Venus in DevStack, perform the following steps:

## 1. Enabling Venus in local.conf
Enable the plugin by adding the following section to `local.conf`
```
    [[local|localrc]]
    enable_plugin venus https://review.opendev.org/openstack/venus
    enable_plugin venus-dashboard https://review.opendev.org/openstack/venus-dashboard
```
## 2. Modify service log format
After `stack.sh` process finished, replace the lines begin with `logging_default_format_string =` and `logging_context_format_string =` with
```
logging_default_format_string = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [- req-None - - - - -] %(instance)s%(message)s
logging_context_format_string = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(global_request_id)s %(request_id)s 
```

in files
- /etc/nova/nova.conf
- /etc/cinder/cinder.conf
- /etc/neutron/neutron.conf

Restart nova, cinder and neutron service:

```
systemctl restart devstack@n-api.service
systemctl restart devstack@c-api.service
systemctl restart devstack@q-svc.service
```

## 3. [Optional] Manually download td-agent and es
If you want to download td-agent and es yourself when the official download link is not available,
you cloud get them via the following links:

- https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.16.deb
- https://packages.treasuredata.com.s3.amazonaws.com/4/ubuntu/bionic/pool/contrib/t/td-agent/td-agent_4.1.0-1_amd64.deb

And save the files to `/opt/stack/venus/devstack/files`
