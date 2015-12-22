##### Destroy a Ceph cluster:

Purge a Ceph cluster so you can re-deploy it from scratch:

```
for i in `seq 1 12`; do ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no core-${i} -C "sudo rm -rf /etc/ceph/*"; done
for i in `seq 1 12`; do ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no core-${i} -C "sudo rm -rf /var/lib/ceph/*"; done
for i in `seq 1 8`; do ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no core-${i} -C "sudo parted /dev/sdb -s rm 2"; done
for i in `seq 1 8`; do ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no core-${i} -C "sudo umount /dev/sdb"; done
etcdctl rm --recursive /ceph-config
```
