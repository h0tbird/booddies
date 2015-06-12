Name:      booddies
Version:   0.1.0
Release:   2%{?dist}
Summary:   The bootstrapping fellowship
Group:     Applications/Internet
License:   Apache-2
URL:       https://github.com/h0tbird/booddies/blob/master/README.md
Source0:   %{name}-%{version}.tar.gz
Packager:  Marc Villacorta Morera <marc.villacorta@gmail.com>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires:  docker

%description
Boot buddies or booddies is a set of Docker containers used to bootstrapp a
Mesos cluster using containers on top of CoreOS on top of KVM on top of bare
metal. Although it can be used to boot any PXE compliant system, it is not
intended to be a general purpose bootstrapping system.

%prep
%setup -q

%install
%{__install} -p -D -m 0644 containers/docker-boot/boot.service %{buildroot}%{_sysconfdir}/systemd/system/boot.service
%{__install} -p -D -m 0644 containers/docker-cgit/cgit.service %{buildroot}%{_sysconfdir}/systemd/system/cgit.service
%{__install} -p -D -m 0644 containers/docker-data/data.service %{buildroot}%{_sysconfdir}/systemd/system/data.service
%{__install} -p -D -m 0644 containers/docker-gito/gito.service %{buildroot}%{_sysconfdir}/systemd/system/gito.service
%{__install} -p -D -m 0644 containers/docker-regi/regi.service %{buildroot}%{_sysconfdir}/systemd/system/regi.service
%{__install} -p -D -m 0755 containers/docker-boot/bin/runctl %{buildroot}/usr/local/sbin/runctl-boot
%{__install} -p -D -m 0755 containers/docker-cgit/bin/runctl %{buildroot}/usr/local/sbin/runctl-cgit
%{__install} -p -D -m 0755 containers/docker-data/bin/runctl %{buildroot}/usr/local/sbin/runctl-data
%{__install} -p -D -m 0755 containers/docker-gito/bin/runctl %{buildroot}/usr/local/sbin/runctl-gito
%{__install} -p -D -m 0755 containers/docker-regi/bin/runctl %{buildroot}/usr/local/sbin/runctl-regi
%{__install} -p -D -m 0644 containers/docker-boot/boot.conf %{buildroot}%{_sysconfdir}/booddies/boot.conf
%{__install} -p -D -m 0644 containers/docker-cgit/cgit.conf %{buildroot}%{_sysconfdir}/booddies/cgit.conf
%{__install} -p -D -m 0644 containers/docker-data/data.conf %{buildroot}%{_sysconfdir}/booddies/data.conf
%{__install} -p -D -m 0644 containers/docker-gito/gito.conf %{buildroot}%{_sysconfdir}/booddies/gito.conf
%{__install} -p -D -m 0644 containers/docker-regi/regi.conf %{buildroot}%{_sysconfdir}/booddies/regi.conf
%{__install} -p -D -m 0755 bin/feed-boot %{buildroot}/usr/local/sbin/feed-boot
%{__install} -p -D -m 0755 bin/feed-data %{buildroot}/usr/local/sbin/feed-data
%{__install} -p -D -m 0755 bin/feed-gito %{buildroot}/usr/local/sbin/feed-gito
%{__install} -p -D -m 0755 bin/feed-regi %{buildroot}/usr/local/sbin/feed-regi

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf "${RPM_BUILD_ROOT}"

%post
systemctl daemon-reload

%files
%{_sysconfdir}/systemd/system/*.service
/usr/local/sbin/runctl-*
/usr/local/sbin/feed-*
%config(noreplace) %{_sysconfdir}/booddies/*.conf

%changelog
* Thu Jun 11 2015 Marc Villacorta Morera <marc.villacorta@gmail.com> - 0.1.0-2
- Added feed-x scripts.
* Thu Jun  4 2015 Marc Villacorta Morera <marc.villacorta@gmail.com> - 0.1.0-1
- Initial package.
