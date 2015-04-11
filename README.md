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
- [x] **gito:** A [`gitolite`][gitolite-web] server with [`R10K`][r10k-web] and Puppet code.
- [x] **cgit:** An `apache` server acting as a frontend to `gitolite`.
- [x] **regi:** A python [`docker registry`][registry-web] to distribute docker images.
- [ ] **ntpd:** A `ntpd` server to provide clock synchronization. 

## Batteries included

This is what you get when you install `booddies`:

```
/
├── data <-------------------------- Persistent data directories mounted by containers.
│   ├── boot/
│   ├── data/
│   ├── gito/
│   └── regi/
├── etc
│   ├── booddies <------------------ Per container configuration files.
│   │   ├── boot.conf
│   │   ├── cgit.conf
│   │   ├── data.conf
│   │   ├── gito.conf
│   │   └── regi.conf
│   └── systemd
│       └── system <---------------- Per container systemd service unit files.
│           ├── boot.service
│           ├── cgit.service
│           ├── data.service
│           ├── gito.service
│           └── regi.service
└── usr
    └── local
        └── sbin <------------------ Pre-run, run and post-run logic.
            ├── runctl-boot
            ├── runctl-cgit
            ├── runctl-data
            ├── runctl-gito
            └── runctl-regi
```

And of course you also get the docker images:

| Docker Image               | Status                          | ID     | Config file                | Systemd unit                                        | Run logic |
| -------------------------- | ------------------------------- |:------:| -------------------------- | --------------------------- | ------------------------- |
| [h0tbird/boot][boot-image] | [![boot][boot-image]][boot-web] | boot01 | [*boot.conf*][boot-config] | [*boot.service*][boot-unit] | [*runctl-boot*][boot-run] |
| [h0tbird/data][data-image] | [![data][data-image]][data-web] | data01 | [*data.conf*][data-config] | [*data.service*][data-unit] | [*runctl-data*][data-run] |
| [h0tbird/gito][gito-image] | [![gito][gito-image]][gito-web] | gito01 | [*gito.conf*][gito-config] | [*gito.service*][gito-unit] | [*runctl-gito*][gito-run] |
| [h0tbird/cgit][cgit-image] | [![cgit][cgit-image]][cgit-web] | cgit01 | [*cgit.conf*][cgit-config] | [*cgit.service*][cgit-unit] | [*runctl-cgit*][cgit-run] |
| [h0tbird/regi][regi-image] | [![regi][regi-image]][regi-web] | regi01 | [*regi.conf*][regi-config] | [*regi.service*][regi-unit] | [*runctl-regi*][regi-run] |

## Prerequisites
* Docker must be installed in the system and the option `--insecure-registry regi01.demo.lan:5000` must be used for the private docker registry to work.
* Also make sure you have about 20GB of free space in `/data`.

## Installation
##### 1. Clone and install
A recursive git clone is needed in order to pull all git submodules:
```
git clone --recursive https://github.com/h0tbird/booddies.git
```
This will provide the file and directory structure previously detailed:
```
cd booddies && ./bin/install
```

##### 2. Start the services
The first time you start the services all docker images will be downloaded from docker hub:
```
sudo systemctl start boot data gito cgit regi
```

## Data synchronization
##### 1. Mirror external repositories
About 15GB of data will be downloaded, check the [`datasync`][datasync-code] code for more details:
```
docker exec -it data01 datasync base
docker exec -it data01 datasync updates
docker exec -it data01 datasync puppetlabs-products
docker exec -it data01 datasync puppetlabs-deps
docker exec -it data01 datasync epel
docker exec -it data01 datasync coreos
```

##### 2. Package R10K
R10K is not in EPEL so it must be provided by other means. Using docker and [`fpm`][fpm-web] is a very clean solution:
```
docker run -it --rm -e GEM=r10k \
-v /data/data/centos/7/misc:/newgems centos:7 bash -c "
yum install -y ruby-devel gcc libffi-devel make rpm-build
gem install --no-document --verbose fpm
mkdir /tmp/gems
gem install --no-document --verbose --install-dir /tmp/gems \$GEM
cd /newgems
find /tmp/gems -name '*.gem' | \
xargs -rn1 fpm -d ruby -d rubygems --edit --prefix /usr/share/gems -s gem -t rpm"
```

Now the `misc` repository can be generated.
```
docker exec -it data01 datasync misc
```

##### 3. Kernel and initrd
This is needed because the kernel and the initrd provided by the `boot` service must match those on the instalation media.
```
sudo mkdir -p /data/boot/images/centos/7/x86_64
sudo ln /data/data/centos/7/os/x86_64/images/pxeboot/vmlinuz /data/boot/images/centos/7/x86_64/
sudo ln /data/data/centos/7/os/x86_64/images/pxeboot/initrd.img /data/boot/images/centos/7/x86_64/
```

##### 4. Populate the private docker registry
Zookeeper:
```
docker pull jplock/zookeeper
docker tag jplock/zookeeper regi01.demo.lan:5000/zookeeper
docker push regi01.demo.lan:5000/zookeeper
```

Mesos master:
```
docker pull mesosphere/mesos-master:0.20.1
docker tag mesosphere/mesos-master:0.20.1 regi01.demo.lan:5000/mesos-master:0.20.1
docker push regi01.demo.lan:5000/mesos-master:0.20.1
```

Mesos slave:
```
docker pull mesosphere/mesos-slave:0.20.1
docker tag mesosphere/mesos-slave:0.20.1 regi01.demo.lan:5000/mesos-slave:0.20.1
docker push regi01.demo.lan:5000/mesos-slave:0.20.1
```

Marathon:
```
docker pull mesosphere/marathon:v0.7.5
docker tag mesosphere/marathon:v0.7.5 regi01.demo.lan:5000/marathon:v0.7.5
docker push regi01.demo.lan:5000/marathon:v0.7.5
```

##### 5. Populate the gitolite repositories

```
docker exec -it gito01 repoimport \
--admin admin \
--owner 'Marc Villacorta' \
--description 'Masterless puppet config' \
--category configuration \
--repo https://github.com/h0tbird/puppet-config.git \
--mirror
```

## Devel:
##### Switch git repos to RW mode:
First the parent:
```
git remote set-url origin `git config --get remote.origin.url | sed s/github/h0tbird@github/`
```

Now the submodules:
```
git submodule foreach git checkout master

for i in containers data; do
  for j in `ls $i`; do
    pushd ${i}/${j}
    git remote set-url origin `git config --get remote.origin.url | \
    sed s/github/h0tbird@github/`
    popd
  done
done
```

Verify:
```
git submodule foreach git config --get remote.origin.url
```
##### Push local changes to mirror repos:
```
docker exec -it gito01 su git -c '            
for i in ~/repositories/*; do                 
  pushd $i                                    
  target=$(git config --get gitolite.mirror.simple)
  [ -z "$target" ] || git push --mirror $target
  popd
done'
```

## License

Copyright 2015 Marc Villacorta Morera

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

[containers-counter]: https://img.shields.io/badge/containers-5/6-yellow.svg
[containers]: https://hub.docker.com/u/h0tbird
[license-image]: http://img.shields.io/badge/license-Apache--2-blue.svg?style=flat
[license]: http://www.apache.org/licenses/LICENSE-2.0
[dcos-web]: http://mesosphere.com/product
[dnsmasq-web]: http://www.thekelleys.org.uk/dnsmasq/doc.html
[apache-web]: http://httpd.apache.org
[gitolite-web]: http://gitolite.com
[r10k-web]: https://github.com/puppetlabs/r10k
[registry-web]: https://github.com/docker/docker-registry
[datasync-code]: https://github.com/h0tbird/docker-data/blob/master/rootfs/usr/sbin/datasync
[fpm-web]: https://github.com/jordansissel/fpm

[boot-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[boot-web]: https://registry.hub.docker.com/u/h0tbird/boot
[data-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[data-web]: https://registry.hub.docker.com/u/h0tbird/data
[gito-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[gito-web]: https://registry.hub.docker.com/u/h0tbird/gito
[cgit-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[cgit-web]: https://registry.hub.docker.com/u/h0tbird/cgit
[regi-image]: https://img.shields.io/badge/build-unknown-lightgrey.svg
[regi-web]: https://registry.hub.docker.com/u/h0tbird/regi

[boot-config]: https://github.com/h0tbird/docker-boot/blob/master/boot.conf
[data-config]: https://github.com/h0tbird/docker-data/blob/master/data.conf
[gito-config]: https://github.com/h0tbird/docker-gito/blob/master/gito.conf
[cgit-config]: https://github.com/h0tbird/docker-cgit/blob/master/cgit.conf
[regi-config]: https://github.com/h0tbird/docker-regi/blob/master/regi.conf

[boot-unit]: https://github.com/h0tbird/docker-boot/blob/master/boot.service
[data-unit]: https://github.com/h0tbird/docker-data/blob/master/data.service
[gito-unit]: https://github.com/h0tbird/docker-gito/blob/master/gito.service
[cgit-unit]: https://github.com/h0tbird/docker-cgit/blob/master/cgit.service
[regi-unit]: https://github.com/h0tbird/docker-regi/blob/master/regi.service

[boot-run]: https://github.com/h0tbird/docker-boot/blob/master/bin/runctl
[data-run]: https://github.com/h0tbird/docker-data/blob/master/bin/runctl
[gito-run]: https://github.com/h0tbird/docker-gito/blob/master/bin/runctl
[cgit-run]: https://github.com/h0tbird/docker-cgit/blob/master/bin/runctl
[regi-run]: https://github.com/h0tbird/docker-regi/blob/master/bin/runctl
