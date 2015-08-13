##### Add a new user to gitolite:

This is used to add a new user to the gitolite-admin repository.

```
cat << EOF > ~/myssh
#!/bin/bash
ssh -i ~/.ssh/gitolite.key \$@
EOF

chmod +x ~/myssh
GIT_SSH=~/myssh git clone git@gito01:gitolite-admin
cd gitolite-admin
cp ~/.ssh/id_rsa.pub keydir/marc.pub
vim conf/gitolite.conf
git add conf/ keydir/
git commit -am "Added user marc"
GIT_SSH=~/myssh git push
```
