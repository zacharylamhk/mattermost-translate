#!/bin/bash

SERVICE_NAME="qb_translate"

# Check if the service is running
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "Service $SERVICE_NAME is running."
else
    echo "Service $SERVICE_NAME is stopped. Starting..."
    systemctl start $SERVICE_NAME

    # Check if the service started successfully
    if [ $? -eq 0 ]; then
        echo "Service $SERVICE_NAME started successfully."
    else
        echo "Failed to start $SERVICE_NAME. Check the logs for more information."
        exit 1
    fi
fi