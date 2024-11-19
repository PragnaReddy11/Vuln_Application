#!/bin/bash

# Variables
PUBLIC_KEY="/home/student/keys/cosign.pub"

cosign verify \
    --key "$PUBLIC_KEY" \
    docker-registry.local:5000/gr8scope:1.0.4-beta \
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

cosign verify-attestation \
    --key "$PUBLIC_KEY" \
    --type spdxjson \
    --allow-http-registry=true \
    --insecure-ignore-tlog=true \
    --registry-username='student' \
    --registry-password='tartans@1' \
    docker-registry.local:5000/gr8scope:1.0.4-beta > cosign_output.txt 2>&1

if grep -q "The cosign claims were validated" cosign_output.txt && \
   grep -q "The signatures were verified against the specified public key" cosign_output.txt; then
  echo "✅ Check #2 - Verified signatures on SBOM Attestation: +10 points."
else
  echo "❌ Check #1 - SBOM Attestation's signature verification failed: 0 points."
  cat cosign_output.txt
fi
