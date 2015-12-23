##### Re-deploy a Ceph cluster:

Stop:

```
fleetctl stop ceph-osd
fleetctl stop ceph-mon
```

Destroy:

```
etcdctl rm --recursive /ceph-config
loopssh sudo rm -rf /etc/ceph/*
loopssh sudo rm -rf /var/lib/ceph/*
loopssh sudo parted /dev/sdb -s rm 2
loopssh sudo umount /dev/sdb
```

Start:

```
fleetctl start ceph-mon
fleetctl start ceph-osd
```
