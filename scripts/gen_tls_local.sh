#!/usr/bin/env bash
set -e

CERT_DIR="nginx/certs"
DAYS=365

echo "🔐 Génération des certificats TLS locaux..."

mkdir -p $CERT_DIR

openssl req -x509 -nodes -days $DAYS \
  -newkey rsa:2048 \
  -keyout $CERT_DIR/key.pem \
  -out $CERT_DIR/cert.pem \
  -subj "/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

echo "✅ Certificats générés dans $CERT_DIR"
