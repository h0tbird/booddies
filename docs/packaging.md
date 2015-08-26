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
