#!/bin/bash

cd "$(dirname "$0")/.." || exit

api_key=$(LC_ALL=C tr -dc 'A-Za-z0-9$' </dev/urandom | head -c 20 ; echo)
credentials=$(echo "admin=${api_key}" | base64)
export API_KEY=${credentials}
echo "The API key for this session is: ${credentials}"

#export TLS_KEY_PATH=serverKey.pem
#export TLS_CERT_PATH=serverCert.pem

python -W ignore -m app.main
