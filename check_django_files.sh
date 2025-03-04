# instructions to make script executable.
# chmod +x check_django_files.sh
# ./check_django_files.sh

#!/bin/bash
# List of directories to check (modify as needed)
DIRECTORIES=("credit_service" "users" "credits" "dictionary" "payments" "plans" "reports") 

# List of required files in each directory
REQUIRED_FILES=("models.py" "views.py" "serializers.py" "urls.py" "permissions.py")

# Loop through each directory in the list
for dir in "${DIRECTORIES[@]}"; do
        # Ensure the directory exists before checking for files
        if [ ! -d "$dir" ]; then
            echo "Creating missing directory: $dir"
            mkdir -p "$dir"
        fi

        # Loop through required files
        for file in "${REQUIRED_FILES[@]}"; do
            if [ ! -f "$dir/$file" ]; then
                echo "Creating missing file: $dir/$file"
                case "$file" in
                    "models.py") echo "from django.db import models" > "$dir/$file" ;;
                    "views.py") echo "from rest_framework.views import APIView" > "$dir/$file" ;;
                    "serializers.py") echo "from rest_framework import serializers" > "$dir/$file" ;;
                    "urls.py") echo "from django.urls import path" > "$dir/$file" ;;
                    "permissions.py") echo "from rest_framework.permissions import BasePermission" > "$dir/$file" ;;
                esac
            fi
        done
done

echo "Check completed!"
