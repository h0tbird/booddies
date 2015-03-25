# Booddies

Boot buddies is a set of Docker containers used to bootstrapp a DCOS-like platform.
Although it can be used to boot any PXE compliant system, it is not a general purpose bootstrapping system.

###### Clone
```
git clone --recursive https://github.com/h0tbird/booddies.git
```

###### Setup the file system:
```
sudo mkdir -p /data/{boot,data,gito,regi}
sudo git clone https://github.com/h0tbird/pxelinux /data/boot/pxelinux
sudo git clone https://github.com/h0tbird/kickstart /data/data/kickstarts
```

###### Start the services:
```
git clone https://github.com/h0tbird/systemd-units
sudo cp systemd-units/arch/docker.service /usr/lib/systemd/system/
sudo cp systemd-units/arch/{boot,gito,regi,repo,cgit}*.service /etc/systemd/system/
sudo systemctl enable docker boot data gito cgit regi
```

###### Synchronize external data:
```
docker exec -it data01 datasync base
docker exec -it data01 datasync updates
docker exec -it data01 datasync puppetlabs-products
docker exec -it data01 datasync puppetlabs-deps
docker exec -it data01 datasync epel
docker exec -it data01 datasync coreos
docker exec -it data01 datasync misc
```
