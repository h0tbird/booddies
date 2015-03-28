# Booddies

[ ![Containers counter] [containers-counter] ] [containers]
[ ![License] [license-image] ] [license]

<img src="https://www.lucidchart.com/publicSegments/view/551701de-fe3c-4e49-84e1-431d0a008e9b/image.png"
 alt="Booddies logo" title="Booddies" align="right" />

Boot buddies or `booddies` is a set of Docker containers used to bootstrapp a [`DCOS`][dcos-web]-like platform.
Although it can be used to boot any PXE compliant system, it is not intended to be a general purpose bootstrapping system.

Six containers are planned:

- [x] **boot:** A [`dnsmasq`][dnsmasq-web] server that handles PXE, DHCP, TFTP, and DNS.
- [x] **data:** An [`apache`][apache-web] server with YUM repositories and other data.
- [x] **gito:** A [`gitolite`][gitolite-web] server with R10K and Puppet code.
- [x] **cgit:** An [`apache`][apache-web] server acting as a frontend to `gitolite`.
- [ ] **regi:** A python [`docker registry`][registry-web] to distribute docker images.
- [ ] **ntpd:** A `ntpd` server to provide clock synchronization. 

## The containers

| Docker Image | Status                          | Container ID | Config file               | Systemd unit |
| ------------ | ------------------------------- | ------------ | ------------------------- | ------------ |
| h0tbird/boot | [![boot][boot-image]][boot-web] | boot01       | */etc/booddies/boot.conf* | boot.service |
| h0tbird/data | [![data][data-image]][data-web] | data01       | */etc/booddies/data.conf* | data.service |
| h0tbird/gito | [![gito][gito-image]][gito-web] | gito01       | */etc/booddies/gito.conf* | gito.service |
| h0tbird/cgit | [![cgit][cgit-image]][cgit-web] | cgit01       | */etc/booddies/cgit.conf* | cgit.service |

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
git remote set-url origin `git config --get remote.origin.url | \
sed s/github/h0tbird@github/`
git submodule foreach git checkout master

for i in containers data; do
  for j in `ls $i`; do
    pushd ${i}/${j}
    git remote set-url origin `git config --get remote.origin.url | \
    sed s/github/h0tbird@github/`
    popd
  done
done

git submodule foreach git config --get remote.origin.url
```

[containers-counter]: https://img.shields.io/badge/containers-4/6-yellow.svg
[containers]: https://hub.docker.com/u/h0tbird
[license-image]: http://img.shields.io/badge/license-Apache--2-blue.svg?style=flat
[license]: http://www.apache.org/licenses/LICENSE-2.0
[dcos-web]: http://mesosphere.com/product
[dnsmasq-web]: http://www.thekelleys.org.uk/dnsmasq/doc.html
[apache-web]: http://httpd.apache.org
[gitolite-web]: http://gitolite.com
[registry-web]: https://github.com/docker/docker-registry
[boot-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[boot-web]: https://registry.hub.docker.com/u/h0tbird/boot
[data-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[data-web]: https://registry.hub.docker.com/u/h0tbird/data
[gito-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[gito-web]: https://registry.hub.docker.com/u/h0tbird/gito
[cgit-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[cgit-web]: https://registry.hub.docker.com/u/h0tbird/cgit
