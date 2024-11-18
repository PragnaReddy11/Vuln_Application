#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Variables
PUBLIC_KEY="/home/student/keys/cosign.pub"
REGISTRY_USERNAME=""
REGISTRY_PASSWORD="tartans@1"
IMAGE_NAME="gr8scope_$IMAGE_TAG"

cosign verify \ 
    --key "$PUBLIC_KEY" \
    docker-registry.local:5000/gr8scope:1.0.3-beta \
    --allow-http-registry=true \
    --insecure-ignore-tlog=true \
    --registry-username='student' \
    --registry-password='tartans@1' > cosign_output.txt 2>&1

if grep -q "The cosign claims were validated" cosign_output.txt && \
   grep -q "The signatures were verified against the specified public key" cosign_output.txt; then
  echo "✅ Check #1 - Verified signatures on registry image: +10 points."
else
  echo "❌ Check #1 - Registry image's signature verification failed: 0 points."
  cat cosign_output.txt
fi

cosign verify \
    --key "$PUBLIC_KEY" \
    --local-image ~/gr8scope_1.0.3-beta/ \
    --registry-username='student' \
    --registry-password='tartans@1' \
    --insecure-ignore-tlog=true > cosign_output.txt 2>&1

# Check if the verification was successful
if grep -q "The cosign claims were validated" cosign_output.txt && \
   grep -q "The signatures were verified against the specified public key" cosign_output.txt; then
  echo "✅ Check #2 - Verified signatures on local image: +10 points."
  exit 0
else
  echo "❌ Check #2 - Local image's signature verification failed: 0 points."
  cat cosign_output.txt
  exit 1
fi
