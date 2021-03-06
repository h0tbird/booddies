##### Self signed certificate with subject alternate names and wildcards:

Edit the configuration file to meet your needs:

```
cat << EOF > ssl.conf
[ req ]
prompt             = no
distinguished_name = req_subj
x509_extensions    = x509_ext

[ req_subj ]
C  = ES
L  = Barcelona
O  = Mesos
CN = Company

[ x509_ext ]
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
basicConstraints       = CA:true
subjectAltName         = @alternate_names

[ alternate_names ]
DNS.1 = *.marathon
DNS.2 = *.marathon.cell-1.dc-1.mesos
DNS.3 = *.cell-1.dc-1.mesos
DNS.4 = *.cell-1.dc-1.demo.lan
DNS.5 = localhost
IP.1  = 127.0.0.1
EOF
```

Create a self signed certificate:
```
mkdir certs && openssl req -config ssl.conf \
-new -x509 -nodes -sha256 -days 365 -newkey rsa:4096 \
-keyout certs/server-key.pem -out certs/server-crt.pem
```

Verify the result:
```
openssl x509 -in certs/server-crt.pem -text -noout
openssl verify -CAfile certs/server-crt.pem certs/server-crt.pem
```
