#!/bin/bash

# macOS Deployment Script for apple-framework
# Ensure this script is executable: chmod +x deploy_mac.sh

APP_NAME="apple-framework"
DOCKER_IMAGE="$APP_NAME-image"
DOCKER_CONTAINER="$APP_NAME-container"
DEPLOY_DIR="/usr/local/var/www/$APP_NAME"
NGINX_CONF="/usr/local/etc/nginx/servers/$APP_NAME.conf"

echo "Starting deployment process on macOS..."

# Step 1: Install dependencies
echo "Installing npm dependencies..."
npm install --production || { echo "Dependency installation failed. Exiting."; exit 1; }

# Step 2: Build the project
echo "Building the project with TypeScript..."
npx tsc --outDir dist || { echo "Build failed. Exiting."; exit 1; }

# Step 3: Build Docker image
echo "Building Docker image..."
docker build -t $DOCKER_IMAGE . || { echo "Docker build failed. Exiting."; exit 1; }

# Step 4: Stop existing container
if docker ps -q -f name=$DOCKER_CONTAINER > /dev/null; then
    echo "Stopping existing Docker container..."
    docker stop $DOCKER_CONTAINER || { echo "Failed to stop container. Exiting."; exit 1; }
    docker rm $DOCKER_CONTAINER || { echo "Failed to remove container. Exiting."; exit 1; }
fi

# Step 5: Start new Docker container
echo "Starting new Docker container..."
docker run -d -p 3000:3000 --name $DOCKER_CONTAINER $DOCKER_IMAGE || { echo "Failed to start container. Exiting."; exit 1; }

# Step 6: Configure Nginx for macOS
echo "Configuring Nginx..."
sudo mkdir -p /usr/local/etc/nginx/servers
cat <<EOL | sudo tee $NGINX_CONF > /dev/null
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOL

# Reload Nginx to apply the configuration
echo "Reloading Nginx..."
sudo nginx -s reload || { echo "Failed to reload Nginx. Exiting."; exit 1; }

# Step 7: Verify Deployment
echo "Verifying deployment..."
curl -I http://localhost || { echo "Deployment verification failed. Exiting."; exit 1; }

echo "Deployment completed successfully. Visit http://localhost to view the application."
