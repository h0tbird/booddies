##### Destroy a Ceph cluster:

Purge a Ceph cluster so you can re-deploy it from scratch:

```
fleetctl stop ceph-osd
fleetctl stop ceph-mon
etcdctl rm --recursive /ceph-config
loopssh sudo rm -rf /etc/ceph/*
loopssh sudo rm -rf /var/lib/ceph/*
```
