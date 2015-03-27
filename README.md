# Booddies

Boot buddies is a set of Docker containers used to bootstrapp a DCOS-like platform.
Although it can be used to boot any PXE compliant system, it is not intended to be a general purpose bootstrapping system.

| Docker Image  | Container ID  | Process       | Service       |
| ------------- | ------------- | ------------- | ------------- |
| h0tbird/boot  | boot01        | dnsmasq       | DNS,DHCP,TFTP |
| h0tbird/data  | data01        | httpd         | Apache        |
| h0tbird/gito  | gito01        | sshd          | Gitolite      |
| h0tbird/cgit  | cgit01        | httpd         | CGit          |

###### Install
```
git clone --recursive https://github.com/h0tbird/booddies.git

cd booddies && for i in `ls containers`; do
  pushd containers/${i}
  sudo ./bin/install
  popd
done
```

###### Start the services:
```
sudo systemctl start boot data gito cgit
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

###### Devel:
```
cd booddies
git remote set-url origin `git config --get remote.origin.url | sed s/github/h0tbird@github/`
git submodule foreach git checkout master

for i in containers data; do
  for j in `ls $i`; do
    pushd ${i}/${j}
    git remote set-url origin `git config --get remote.origin.url | sed s/github/h0tbird@github/`
    popd
  done
done

git submodule foreach git config --get remote.origin.url
```
