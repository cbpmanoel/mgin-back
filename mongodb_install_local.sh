#!/bin/bash

set -e  # Exit on error

# Default values
DEFAULT_USER="root"
DEFAULT_PASS="example"
MONGO_VERSION="8.0"
MONGO_PORT=27017

# Functions for colored output using tput
red() {
    tput setaf 1
    echo "$1"
    tput sgr0
}
green_title() {
    tput bold
    tput setaf 2
    echo
    echo "$1"
    tput sgr0
}

green_title "---- MongoDB Setup Script ----"

# Check if the script is running with root permissions
if ! sudo -v && [[ $EUID -ne 0 ]]; then
    red "This script must be run with root permissions. Exiting."
    exit 1
fi

# Usage function
usage() {
    echo "Usage: $0 [-u username] [-p password] [-d database_name]"
    echo "  -u  Root username (default: root)"
    echo "  -p  Root password (default: root)"
    echo "  -v  MongoDB version (default: 8.0)"
    exit 1
}

# Parse command-line arguments
while getopts ":u:p:v:" opt; do
    case "${opt}" in
        u) ADMIN_USER=${OPTARG} ;;
        p) ADMIN_PASS=${OPTARG} ;;
        v) MONGO_VERSION=${OPTARG} ;;
        *) usage ;;
    esac
done

# Set defaults if not provided
ADMIN_USER=${ADMIN_USER:-$DEFAULT_USER}
ADMIN_PASS=${ADMIN_PASS:-$DEFAULT_PASS}

green_title "Starting MongoDB installation and configuration..."
echo "Root user: $ADMIN_USER"
echo "Root password: $ADMIN_PASS"

# Detect Operating System
OS_NAME=$(lsb_release -is)
OS_VERSION=$(lsb_release -rs)

# Check if MongoDB is already installed
if command -v mongod &>/dev/null; then
    red "MongoDB is already installed. Exiting."
    exit 1
fi

# Check if the script is running on Ubuntu
if [[ "$OS_NAME" != "Ubuntu" ]]; then
    red "This script is designed for Ubuntu. Detected OS: $OS_NAME. Exiting."
    exit 1
fi

# Check if there's any MongoDB related packages installed
if dpkg -l | grep -q "mongo"; then
    red "Existing MongoDB packages found. Please uninstall them before running this script. Exiting."
    exit 1
fi

# Check if there are any old MongoDB data files
shopt -s nullglob
files=(/var/lib/mongodb/*)
if [ ${#files[@]} -gt 0 ]; then
    red "Existing ${#files[@]} MongoDB data files found. Please backup and remove them before running this script. Exiting."
    exit 1
fi

if lsof -i :$MONGO_PORT > /dev/null 2>&1; then
    red "Port $MONGO_PORT is already in use. MongoDB may already be running or another service is using the port."
    red "Please stop the service using this port or configure MongoDB to use a different port. Exiting."
    exit 1
fi

# Set MongoDB repository based on Ubuntu version
case "$OS_VERSION" in
    "20.04")
        UBUNTU_CODENAME="focal"
        ;;
    "22.04")
        UBUNTU_CODENAME="jammy"
        ;;
    "24.04")
        UBUNTU_CODENAME="noble"
        ;;
    *)
        red "Unsupported Ubuntu version: $OS_VERSION. Exiting."
        exit 1
        ;;
esac

green_title "Detected Ubuntu version: $OS_NAME $OS_VERSION ($UBUNTU_CODENAME)"

# Import MongoDB GPG Key
green_title "Importing MongoDB GPG key..."
wget -qO - https://www.mongodb.org/static/pgp/server-$MONGO_VERSION.asc | sudo gpg --yes -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor

# Add MongoDB Repository
green_title "Adding MongoDB repository for $UBUNTU_CODENAME..."
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-$MONGO_VERSION.gpg ] https://repo.mongodb.org/apt/ubuntu $UBUNTU_CODENAME/mongodb-org/$MONGO_VERSION multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-$MONGO_VERSION.list

# Update Package List
green_title "Updating package list..."
sudo apt -q update

# Install MongoDB
green_title "Installing MongoDB v$MONGO_VERSION..."
sudo apt -qq -y install mongodb-org

# Start MongoDB Service
green_title "Starting MongoDB service..."
sudo systemctl start mongod

# Enable MongoDB to Start on Boot
green_title "Enabling MongoDB to start on boot..."
sudo systemctl enable mongod

# Verify MongoDB Installation
green_title "Verifying MongoDB installation..."
mongod --version

# Wait for MongoDB to be fully ready
green_title "Waiting for MongoDB to start..."
timeout 30 bash -c 'until mongosh --eval "printjson(db.adminCommand('"'ping'"'))" &>/dev/null; do sleep 1; done' || { red "MongoDB failed to start. Exiting."; exit 1; }

# Create Root User (BEFORE enabling authentication)
green_title "Creating root user in MongoDB..."
mongosh <<EOF
use admin
db.createUser({
  user: "$ADMIN_USER",
  pwd: "$ADMIN_PASS",
  roles: [{ role: "root", db: "admin" }]
})
EOF

# Configure MongoDB Authentication
green_title "Configuring MongoDB for authentication..."
sudo sed -i '/^#security:/a security:\n  authorization: "enabled"' /etc/mongod.conf

# Restart MongoDB to Apply Changes
green_title "Restarting MongoDB service..."
sudo systemctl restart mongod

# Wait for MongoDB to Restart with timeout
green_title "Waiting for MongoDB to restart..."
timeout 30 bash -c 'until mongosh --eval "printjson(db.adminCommand('"'ping'"'))" &>/dev/null; do sleep 1; done' || { red "MongoDB failed to restart. Exiting."; exit 1; }

# Output Admin Credentials
green_title "MongoDB installation and configuration complete!"
echo "Root User Credentials:"
echo "  Username: $ADMIN_USER"
echo "  Password: $ADMIN_PASS"
echo "You can now connect to MongoDB using authentication."
