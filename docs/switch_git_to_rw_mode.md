##### Switch git repos to RW mode:

First the parent:

```
git remote set-url origin $(git config --get remote.origin.url | sed s/github/h0tbird@github/)
```

Now the submodules:

```
git submodule foreach git checkout master
```

```
for i in containers data; do
  for j in $(ls $i); do
    pushd ${i}/${j}
    git remote set-url origin $(git config --get remote.origin.url | sed s/github/h0tbird@github/)
    popd
  done
done
```

Verify:
```
git submodule foreach git config --get remote.origin.url
```
