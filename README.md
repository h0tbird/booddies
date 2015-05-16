# Booddies

[ ![Containers counter] [containers-counter] ] [containers]
[ ![License] [license-image] ] [license]

<img src="https://www.lucidchart.com/publicSegments/view/553bb3d2-a154-4ab0-99c6-1c420a004a17/image.png"
 alt="Booddies logo" title="Booddies" align="right" />

Boot buddies or `booddies` is a set of [`Docker`][docker-web] containers used to bootstrapp a [`Mesos`][mesos-web] cluster on top of Docker on top of [`CoreOS`][coreos-web] on top of [`KVM`][kvm-web] on top of bare metal.
Although it can be used to boot any PXE compliant system, it is not intended to be a general purpose bootstrapping system.

Six containers are planned:

- [x] **boot:** A [`dnsmasq`][dnsmasq-web] server that handles PXE, DHCP, TFTP, and DNS.
- [x] **data:** An [`apache`][apache-web] server with YUM repositories and other data.
- [x] **gito:** A [`gitolite`][gitolite-web] server with [`R10K`][r10k-web] and Puppet code.
- [x] **cgit:** An `apache` server with a [`cgit`][cgit-web] frontend to `gitolite`.
- [x] **regi:** A python [`docker registry`][registry-web] to distribute docker images.
- [ ] **ntpd:** A `ntpd` server to provide clock synchronization.

## The target platform

This is the platform that `booddies` will help you deploy.

<p align="center">
<img src="https://www.lucidchart.com/publicSegments/view/553bbb69-0dd8-46be-b8b3-76570a009639/image.png" />
</p>

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
        └── sbin <------------------ Per container pre-run, run and post-run logic.
            ├── runctl-boot
            ├── runctl-cgit
            ├── runctl-data
            ├── runctl-gito
            └── runctl-regi
```

And of course you also get the docker images:

| Docker Image             | Status                          | ID     | Config file                | Systemd unit                | Run logic                 |
| ------------------------ | ------------------------------- |:------:| -------------------------- | --------------------------- | ------------------------- |
| [h0tbird/boot][boot-web] | [![boot][boot-image]][boot-web] | boot01 | [*boot.conf*][boot-config] | [*boot.service*][boot-unit] | [*runctl-boot*][boot-run] |
| [h0tbird/data][data-web] | [![data][data-image]][data-web] | data01 | [*data.conf*][data-config] | [*data.service*][data-unit] | [*runctl-data*][data-run] |
| [h0tbird/gito][gito-web] | [![gito][gito-image]][gito-web] | gito01 | [*gito.conf*][gito-config] | [*gito.service*][gito-unit] | [*runctl-gito*][gito-run] |
| [h0tbird/cgit][cgit-web] | [![cgit][cgit-image]][cgit-web] | cgit01 | [*cgit.conf*][cgit-config] | [*cgit.service*][cgit-unit] | [*runctl-cgit*][cgit-run] |
| [h0tbird/regi][regi-web] | [![regi][regi-image]][regi-web] | regi01 | [*regi.conf*][regi-config] | [*regi.service*][regi-unit] | [*runctl-regi*][regi-run] |

## Prerequisites
* Start Docker with `--insecure-registry=regi01:5000`.
* Bridge your physical interface to the `br0` bridge interface.
* Also make sure you have about 20GB of free space in `/data`.

## Step one: Install
##### 1. Clone and install
A recursive git clone is needed in order to pull all git submodules:
```
git clone --recursive https://github.com/h0tbird/booddies.git
```
This command will provide the file and directory structure previously detailed:
```
cd booddies && sudo ./bin/install
```
##### 2. Configure
Chances are, you want to edit this files:
* [`/etc/booddies/boot.conf`][boot-config]
* [`/etc/booddies/gito.conf`][gito-config]

##### 3. Start the services
The first time you start the services all docker images will be downloaded from docker hub:
```
sudo systemctl start boot data gito cgit regi
```

## Step two: Synchronize
Downloading all this data allows `booddies` to be self-contained making it possible to bootstrap the target platform totally offline. You can tail the `/tmp/booddies.log` file for a more detailed progress log.

##### 1. Populate the YUM repositories
About 15GB of data will be downloaded, check [`feed-data`][feed-data-code] and [`datasync`][datasync-code] for more details.
```
./bin/feed-data
```

##### 2. Kernel and initrd
Kernel and ramdisk used by `PXELinux.0`, check [`feed-boot`][feed-boot-code] and [`bootsync`][bootsync-code] for more details.
```
./bin/feed-boot
```

##### 3. Populate the private docker registry

Pull and push from public to private registry, check [`feed-regi`][feed-regi-code] for more details.
```
./bin/feed-regi
```

##### 4. Populate the gitolite repositories

Clone external git repos, check [`feed-gito`][feed-gito-code] and [`gitosync`][gitosync-code] for more details.
```
./bin/feed-gito
```

## Step three: Setup

Populate your [`pxelinux`](https://github.com/h0tbird/pxelinux) files and your [`kickstart`](https://github.com/h0tbird/kickstart) files:
```bash
# ll -d /data/{boot/pxelinux,data/kickstarts}
drwxr-xr-x 2 root root 4.0K Apr 20 19:59 /data/boot/pxelinux/
drwxr-xr-x 3 root root 4.0K Apr 12 11:36 /data/data/kickstarts/
```

You might want to add some DHCP static definitions:
```bash
# cat /data/boot/dnsmasq/dhcp_hosts 
a4:ba:db:1d:1f:aa,kvm01,infinite
84:2b:2b:57:c0:fb,kvm02,infinite
```

## Devel:
##### Switch git repos to RW mode:
First the parent:
```
git remote set-url origin `git config --get remote.origin.url | \
sed s/github/h0tbird@github/`
```

Now the submodules:
```
git submodule foreach git checkout master
```

```
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

##### Add a new user to gitolite:
```
cat << EOF > ~/myssh
#!/bin/bash
ssh -i ~/.ssh/gitolite.key \$@
EOF

chmod +x ~/myssh
GIT_SSH=~/myssh git clone git@gito01.demo.lan:gitolite-admin
cd gitolite-admin
cp ~/.ssh/id_rsa.pub keydir/marc.pub
vim conf/gitolite.conf
git add conf/ keydir/
git commit -am "Added user marc"
GIT_SSH=~/myssh git push
```

##### Push local changes to GitHub:
```
docker exec -it gito01 su git -c '
for i in ~/repositories/*; do
  pushd $i
  target=$(git config --get gitolite.mirror.simple)
  [ -z "$target" ] || git push --mirror $target
  popd
done'
```

##### Fetch changes from GitHub:
```
docker exec -it gito01 su git -c "
for i in ~/repositories/*; do
  pushd \${i}
  git remote | grep -q origin && \
  git fetch origin '+*:*'
  popd
done"
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
[docker-web]: https://www.docker.com
[mesos-web]: http://mesos.apache.org
[coreos-web]: https://coreos.com
[kvm-web]: http://www.linux-kvm.org
[dnsmasq-web]: http://www.thekelleys.org.uk/dnsmasq/doc.html
[apache-web]: http://httpd.apache.org
[gitolite-web]: http://gitolite.com
[cgit-web]: http://git.zx2c4.com/cgit/about
[r10k-web]: https://github.com/puppetlabs/r10k
[registry-web]: https://github.com/docker/docker-registry

[feed-data-code]: https://github.com/h0tbird/booddies/blob/master/bin/feed-data
[datasync-code]: https://github.com/h0tbird/docker-data/blob/master/rootfs/usr/sbin/datasync
[feed-boot-code]: https://github.com/h0tbird/booddies/blob/master/bin/feed-boot
[bootsync-code]: https://github.com/h0tbird/docker-boot/blob/master/rootfs/usr/sbin/bootsync
[feed-regi-code]: https://github.com/h0tbird/booddies/blob/master/bin/feed-regi
[feed-gito-code]: https://github.com/h0tbird/booddies/blob/master/bin/feed-gito
[gitosync-code]: https://github.com/h0tbird/docker-gito/blob/master/rootfs/usr/sbin/gitosync

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
