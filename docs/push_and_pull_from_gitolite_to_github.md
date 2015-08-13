##### Push local changes to GitHub:

This will push from gitolite to GitHub.

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

This will fetch from GitHub to gitolite.

```
docker exec -it gito01 su git -c "
for i in ~/repositories/*; do
  pushd \${i}
  git remote | grep -q origin && \
  git fetch origin '+*:*'
  popd
done"
```
