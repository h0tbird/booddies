##### Self signed certificate with subject alternate names and wildcards:

Edit the configuration file to meet your needs:

```
cat << EOF > ssl.conf
[ req ]
default_bits       = 2048
default_keyfile    = server-key.pem
distinguished_name = subject
req_extensions     = req_ext
x509_extensions    = x509_ext
string_mask        = utf8only

[ subject ]

[ x509_ext ]
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
basicConstraints       = CA:FALSE
keyUsage               = digitalSignature, keyEncipherment
subjectAltName         = @alternate_names
nsComment              = "OpenSSL Generated Certificate"

[ req_ext ]
subjectKeyIdentifier = hash
basicConstraints     = CA:FALSE
keyUsage             = digitalSignature, keyEncipherment
subjectAltName       = @alternate_names
nsComment            = "OpenSSL Generated Certificate"

[ alternate_names ]
DNS.1 = *.cell-1.dc-1.mesos
DNS.2 = *.*.cell-1.dc-1.mesos
DNS.3 = *.cell-1.dc-1.demo.lan
DNS.4 = localhost
DNS.5 = 127.0.0.1
EOF
```

Create a self signed certificate:
```
openssl req \
-config ssl.conf -new -x509 -nodes -sha256 -days 365 -newkey rsa:4096 \
-subj '/C=ES/ST=CAT/L=Barcelona/O=Demo/CN=Company/emailAddress=sysadmin@company.com' \
-keyout server-key.pem -out server-crt.pem
```

Verify the result:
```
openssl x509 -in server-crt.pem -text -noout
```
