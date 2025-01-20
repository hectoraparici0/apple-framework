#!/bin/bash

# Deployment Automation Script for apple-framework
# Usage: ./deploy_production.sh

APP_NAME="apple-framework"
DOCKER_IMAGE="$APP_NAME-image"
DOCKER_CONTAINER="$APP_NAME-container"
NGINX_CONF="/etc/nginx/sites-available/$APP_NAME"
NGINX_LINK="/etc/nginx/sites-enabled/$APP_NAME"
DEPLOY_DIR="/var/www/$APP_NAME"

# 1. Build the Project
echo "Building the project..."
npm install --production
npm run build || { echo "Build failed. Exiting."; exit 1; }
echo "Build completed successfully."

# 2. Build the Docker Image
echo "Building the Docker image..."
docker build -t $DOCKER_IMAGE . || { echo "Docker build failed. Exiting."; exit 1; }
echo "Docker image built successfully."

# 3. Stop and Remove Existing Docker Container
if docker ps -q -f name=$DOCKER_CONTAINER > /dev/null; then
    echo "Stopping existing container..."
    docker stop $DOCKER_CONTAINER || { echo "Failed to stop container. Exiting."; exit 1; }
fi
if docker ps -a -q -f name=$DOCKER_CONTAINER > /dev/null; then
    echo "Removing existing container..."
    docker rm $DOCKER_CONTAINER || { echo "Failed to remove container. Exiting."; exit 1; }
fi

# 4. Start a New Docker Container
echo "Starting a new container..."
docker run -d -p 3000:3000 --name $DOCKER_CONTAINER $DOCKER_IMAGE || { echo "Failed to start container. Exiting."; exit 1; }
echo "Container started successfully."

# 5. Configure Nginx
echo "Configuring Nginx..."
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

# Link the Nginx configuration
sudo ln -sf $NGINX_CONF $NGINX_LINK

# Reload Nginx
sudo systemctl reload nginx || { echo "Failed to reload Nginx. Exiting."; exit 1; }
echo "Nginx configured successfully."

# 6. Verify Deployment
echo "Verifying deployment..."
curl -I http://localhost || { echo "Deployment verification failed. Exiting."; exit 1; }
echo "Deployment verified successfully. Your application is live at http://localhost"
