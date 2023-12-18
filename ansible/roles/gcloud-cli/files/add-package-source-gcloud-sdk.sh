#!/bin/bash

# It has recently updated its packages
#apt-get update

# It has apt-transport-https and curl installed
#apt-get install apt-transport-https ca-certificates gnupg curl sudo

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

# Add the gcloud CLI distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

## Update and install the gcloud CLI
#apt-get update
#apt-get install google-cloud-cli
