##### Package booddies-release-x-y.noarch.rpm

This will generate the `booddies` release RPM which gives you access to the booddies YUM repository.

```
docker run -it --rm \
-v ${PWD}/newrpm:/root/rpmbuild/RPMS/noarch \
-v ${HOME}/.gnupg:/root/.gnupg \
h0tbird/rpmbuild:latest /bin/bash -c "
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
gpg2 --output ~/RPM-GPG-KEY-booddies --armor --export marc.villacorta@gmail.com
cat << EOF > ~/booddies.repo
[booddies]
name=Boot buddies. The bootstrapping fellowship.
baseurl=http://yum-repositories.s3-website-eu-west-1.amazonaws.com/booddies
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-booddies
gpgcheck=1
enabled=1
EOF
cat << EOF > ~/rpmbuild/SPECS/booddies-release.spec
Name: booddies-release
Version: 1
Release: 1
License: Apache-2
Summary: Boot buddies. The bootstrapping fellowship.
Group: System Environment/Base
BuildArch: noarch
BuildRoot: %{_topdir}/%{name}-%{version}%{release}-root

%description
Boot buddies or booddies is a set of Docker containers used to bootstrapp
a Mesos cluster using containers on top of CoreOS on top of KVM on top
of bare metal. Although it can be used to boot any PXE compliant system,
it is not intended to be a general purpose bootstrapping system.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d/
mkdir -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg/
cp -p ~/booddies.repo %{buildroot}%{_sysconfdir}/yum.repos.d/
cp -p ~/RPM-GPG-KEY-booddies %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

%files
%defattr(-,root,root,-)
/etc/yum.repos.d/booddies.repo
/etc/pki/rpm-gpg/RPM-GPG-KEY-booddies

%changelog
* Thu Jun 11 2015 Marc Villacorta <marc.villacorta@gmail.com>
- First release.
EOF
rpmbuild -ba ~/rpmbuild/SPECS/booddies-release.spec"
```

##### Package booddies-x-y.el7.noarch.rpm:

This will generate the `booddies` RPM which is used to install `booddies` in the target system.

```
docker run -it --rm -e VERSION='0.1.0' \
-v ${PWD}/newrpm:/root/rpmbuild/RPMS/noarch \
-v ${HOME}/.gnupg:/root/.gnupg \
h0tbird/rpmbuild:latest /bin/bash -c "
cat << EOF > ~/.rpmmacros
%_signature gpg
%_gpg_path \${HOME}/.gnupg
%_gpg_name Marc Villacorta Morera <marc.villacorta@gmail.com>
%_gpgbin /usr/bin/gpg
%packager Marc Villacorta Morera <marc.villacorta@gmail.com>
%_topdir \${HOME}/rpmbuild
%dist .el7
EOF
git clone --recursive \
https://github.com/h0tbird/booddies.git booddies-\${VERSION}
tar czf booddies-\${VERSION}.tar.gz booddies-\${VERSION}
rpmbuild -ta --sign booddies-\${VERSION}.tar.gz"
```

##### Package rubygem-r10k-2.0.1-1.noarch.rpm

This will generate the `rubygem-r10k` RPM and all its dependencies.

```
docker run -it --rm -e GEM=r10k \
-v ${PWD}/newrpm:/newrpm \
-v ${HOME}/.gnupg:/root/.gnupg \
h0tbird/rpmbuild:latest bash -c "
cat << EOF > ~/.rpmmacros
%_signature gpg
%_gpg_path ~/.gnupg
%_gpg_name Marc Villacorta Morera <marc.villacorta@gmail.com>
%_gpgbin /usr/bin/gpg
%_topdir ~/rpmbuild
EOF
mkdir /tmp/gems
gem install --no-document --verbose --install-dir /tmp/gems \$GEM
cd /newrpm
find /tmp/gems -name '*.gem' | \
xargs -rn1 \
fpm \
--rpm-ignore-iteration-in-dependencies \
--maintainer 'Marc Villacorta Morera <marc.villacorta@gmail.com>' \
-d ruby \
-d rubygems \
--force \
--rpm-sign \
--prefix /usr/share/gems \
-s gem -t rpm"
```

##### Package prometheus-node-exporter-0.11.0-1.x86_64.rpm

This will generate the Prometheus node exporter package.

```
docker run -it --rm \
--env PACKAGE='github.com/prometheus/node_exporter' \
--env VERSION='0.11.0' \
--volume ${PWD}/newrpm:/root/rpmbuild/RPMS/x86_64 \
--volume ${HOME}/.gnupg:/root/.gnupg \
centos:7 /bin/bash -c "
yum install -y git golang mercurial rpm-build rpm-sign
cd && mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cat << EOF > ~/.rpmmacros
%_signature gpg
%_gpg_path ~/.gnupg
%_gpg_name Marc Villacorta Morera <marc.villacorta@gmail.com>
%_gpgbin /usr/bin/gpg
%_topdir /root/rpmbuild
EOF
cat << EOF > /tmp/node_exporter.service
[Unit]
Description=Prometheus exporter for machine metrics
Wants=basic.target
After=basic.target network.target

[Service]
ExecStart=/usr/bin/node_exporter
KillMode=process

[Install]
WantedBy=multi-user.target
EOF
export GOPATH=\${HOME}/go
export PATH=\${PATH}:\${GOPATH}/bin
go get -d \${PACKAGE}
cd \${GOPATH}/src/\${PACKAGE}
git checkout tags/\${VERSION}
go install
cat << EOF > ~/rpmbuild/SPECS/prometheus_node_exporter.spec
Name: prometheus-node-exporter
Version: \${VERSION}
Release: 1
License: Apache-2
Summary: Prometheus exporter for machine metrics.
Packager: %{_gpg_name}
Group: System Environment/Base
BuildArch: x86_64
BuildRoot: %{_topdir}/%{name}-%{version}%{release}-root
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Prometheus exporter for machine metrics.
Written in Go with pluggable metric collectors.

%install
%{__rm} -rf %{buildroot}
%{__install} -p -D -m 0755 \${GOPATH}/bin/node_exporter %{buildroot}/%{_bindir}/node_exporter
%{__install} -p -D -m 0644 /tmp/node_exporter.service %{buildroot}/%{_unitdir}/node_exporter.service

%post
%systemd_post node_exporter.service

%preun
%systemd_preun node_exporter.service

%postun
%systemd_postun_with_restart node_exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/node_exporter
%{_unitdir}/node_exporter.service

%changelog
* Tue Aug 25 2015 Marc Villacorta <marc.villacorta@gmail.com>
- First release.
EOF
rpmbuild -ba --sign ~/rpmbuild/SPECS/prometheus_node_exporter.spec"
```

##### Create the repository metadata

This is used to generate the repository metadata.

```
docker exec -it data01 /bin/bash -c "
DOCROOT='/var/www/data'
createrepo -c \${DOCROOT}/booddies/cachedir --update \${DOCROOT}/booddies
repoview -t misc \${DOCROOT}/booddies"
```

##### Push to S3 bucket

Once the repository is created it can be pushed to S3.

```
s3cmd -P sync /var/lib/booddies/data/booddies/ s3://yum-repositories/booddies/ --delete-removed
```
