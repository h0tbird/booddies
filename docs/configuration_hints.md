##### Set whether to force docker images pull or not:

Set FORCE_PULL_IMAGE to `true`:
```
sudo sed -i -e '/FORCE_PULL_IMAGE/ s/false/true/' /etc/booddies/*.conf
```

Set FORCE_PULL_IMAGE to `false`:
```
sudo sed -i -e '/FORCE_PULL_IMAGE/ s/true/false/' /etc/booddies/*.conf
```
