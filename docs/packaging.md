##### Package booddies-release-x-y.noarch.rpm

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
