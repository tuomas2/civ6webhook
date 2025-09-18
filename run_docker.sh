#!/bin/bash

# Build the Docker image
docker build -t civ6notifier .

# Run the Docker container with the environment variables
docker run -d --restart=always -p 5000:5000 \
  --env-file ~/secret/civ6notifier.secret \
  --name civ6notifier civ6notifier