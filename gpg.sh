#!/bin/bash

# Variables
GPG_KEY_NAME="Test User"
GPG_EMAIL="sreepragnamachupalli@gmail.com"
CODE_PACKAGE="vulnerable_code.tar.gz"

# Step 1: Generate GPG Key Pair
echo "Generating GPG key pair..."

# Generate a GPG key pair (if one doesn't exist)
gpg_key_script=$(cat <<EOF
Key-Type: RSA
Key-Length: 2048
Name-Real: $GPG_KEY_NAME
Name-Email: $GPG_EMAIL
Expire-Date: 1y
%no-protection
%commit
EOF
)

# Run the command to generate the key
echo "$gpg_key_script" | gpg --batch --gen-key

# Fetch the generated GPG key fingerprint
GPG_KEY=$(gpg --list-keys --with-colons | grep fpr | head -n 1 | cut -d':' -f10)

if [ -z "$GPG_KEY" ]; then
    echo "Failed to generate GPG key."
    exit 1
fi

# Step 2: Show the fingerprint to the user and ask them to copy it
echo "Generated GPG key with fingerprint: $GPG_KEY"
echo "Please copy the GPG key fingerprint."

# Step 3: Prompt the user to paste the GPG key fingerprint
read -p "Paste the GPG key fingerprint you copied: " USER_INPUT_KEY

# Step 4: Compare the user input with the actual GPG key
if [ "$USER_INPUT_KEY" != "$GPG_KEY" ]; then
    echo "Error: The pasted fingerprint does not match the generated fingerprint."
    echo "Exiting the script without signing or verifying."
    exit 1
else
    echo "GPG key fingerprint matches. Proceeding with signing..."
fi

# Step 5: Sign the code/package
echo "Signing the package: $CODE_PACKAGE..."
gpg --armor --detach-sign --local-user "$GPG_KEY" "$CODE_PACKAGE"

if [ $? -eq 0 ]; then
    echo "Successfully signed the code package: $CODE_PACKAGE.asc"
else
    echo "Failed to sign the code package."
    exit 1
fi

# Step 6: Export the public key
echo "Exporting the public key..."
gpg --armor --export "$GPG_EMAIL" > public_key.asc

if [ $? -eq 0 ]; then
    echo "Public key exported: public_key.asc"
else
    echo "Failed to export the public key."
    exit 1
fi

# Step 7: Prompt the user to paste the GPG key fingerprint again for verification
read -p "Paste the GPG key fingerprint again to verify: " VERIFY_KEY

if [ "$VERIFY_KEY" != "$GPG_KEY" ]; then
    echo "Error: The verification fingerprint does not match."
    echo "Exiting the script without verifying."
    exit 1
else
    echo "Verification key matches. Proceeding with signature verification..."
fi

# Step 8: Verify the signed code
echo "Verifying the signature..."
gpg --import public_key.asc
gpg --verify "$CODE_PACKAGE.asc" "$CODE_PACKAGE"

if [ $? -eq 0 ]; then
    echo "Signature verification successful."
else
    echo "Signature verification failed."
    exit 1
fi

