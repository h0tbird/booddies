#### Re-deploy a Ceph cluster:

Below I use [loopssh](https://github.com/h0tbird/puppet-r_kvm/blob/7af814a9655975117445f4e338466f0ec45b8b9e/templates/coreos/cloud-config.erb#L106-L114). It is `ssh` in a for loop.

##### Stop:

```
fleetctl stop ceph-osd
fleetctl stop ceph-mon
```

##### Destroy:

```
etcdctl rm --recursive /ceph-config
loopssh sudo rm -rf /etc/ceph
loopssh sudo rm -rf /var/lib/ceph
loopssh sudo umount /dev/sdb
loopssh sudo parted /dev/sdb -s mklabel gpt
loopssh sudo partprobe /dev/sdb
```

##### Start:

```
fleetctl start ceph-mon
fleetctl start ceph-osd
```
