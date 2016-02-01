##### Ephemeral bridge

The system where you run `booddies` for the first time is a throwaway system. `booddies` will transfer itself into every hipervisor it deploys. However, it will only be activated in the first hipervisor (`kvm-1`).  

Find below a fast way to create a VLAN tagged bridge in your throwaway system:

```
ip l add link em1 name em1.901 type vlan id 901
brctl addbr br0
brctl addif br0 em1.901
ip link set dev em1.901 up
ip link set dev br0 up
ip addr add 10.128.0.3/21 dev br0
ip r del default
ip r add default via 10.128.0.1 dev br0
```
