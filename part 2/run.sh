#!/bin/bash

# Set up directory
rm -rf sonarqube-docker1
mkdir sonarqube-docker1
cd sonarqube-docker1


curl -o docker-compose.yml "https://raw.githubusercontent.com/PutuGdeUKDW/takehome-test/main/part%202/docker-compose.yml"
curl -o .env "https://raw.githubusercontent.com/PutuGdeUKDW/takehome-test/main/part%202/.env"


# Build and start services
echo "Building and starting Docker Compose services..."
docker compose up --build -d

# Wait for SonarQube to initialize
echo "Waiting for SonarQube to initialize (this might take a few minutes)..."
until $(curl --output /dev/null --silent --head --fail http://localhost:9000); do
  printf '.'
  sleep 5
done

echo " SonarQube is up and running on http://localhost:9000"
echo "SonarQube credentials: admin/admin"
echo "Setup complete. Logs can be found using 'docker-compose logs'."
