#!/bin/bash

# Ask for gzip encoding option
read -p "Do you want to encode in gzip? (yes/NO): " gzip_option
gzip_option=$(echo "$gzip_option" | tr '[:upper:]' '[:lower:]')

# Ask for base64 encoding option
read -p "Do you want to encode in base64? (yes/NO): " b64_option
b64_option=$(echo "$b64_option" | tr '[:upper:]' '[:lower:]')

# Ask if user wants to test with Burp Collaborator or define a payload
read -p "Do you want to test with Burp Collaborator or define a payload? (1 for test, 2 to define): " option
option=$(echo "$option" | tr '[:upper:]' '[:lower:]')

if [ "$option" == "1" ]; then
    # Prepare the Docker command with options
    echo " " > /tmp/docker_output.log
    command="docker run -it --rm b3xal/ysoserial-cannon"

    if [ "$b64_option" == "yes" ] || [ "$b64_option" == "y" ] || [ "$b64_option" == "s" ] || [ "$b64_option" == "si" ]; then
        command="$command -b64"
    fi

    if [ "$gzip_option" == "yes" ] || [ "$gzip_option" == "y" ] || [ "$gzip_option" == "s" ] || [ "$gzip_option" == "si" ]; then
        command="$command -gzip"
    fi

    # Run the Docker container interactively and log the output to a file
    script -q -c "$command" /tmp/docker_output.log

    # Extract the payloads from the log file and copy to clipboard
    payloads=$(grep -Ei "(^rO0|^H4)" /tmp/docker_output.log)
    if [ -n "$payloads" ]; then
        echo "$payloads" | xclip -selection clipboard
        echo "The payloads have been copied to the clipboard."
    else
        echo "No payloads were generated."
    fi

elif [ "$option" == "2" ]; then
    # If user chooses to define a custom payload right away
    read -p "Enter the custom payload command: " custom_command
    echo "Preparing payload with custom command: $custom_command"
    command="docker run -it --rm b3xal/ysoserial-cannon -c \"$custom_command\""
    
    if [ "$b64_option" == "yes" ] || [ "$b64_option" == "y" ] || [ "$b64_option" == "s" ] || [ "$b64_option" == "si" ]; then
        command="$command -b64"
    fi

    if [ "$gzip_option" == "yes" ] || [ "$gzip_option" == "y" ] || [ "$gzip_option" == "s" ] || [ "$gzip_option" == "si" ]; then
        command="$command -gzip"
    fi

    # Run the Docker container interactively and log the output to a file
    script -q -c "$command" /tmp/docker_output.log

    # Extract the payloads from the log file and copy to clipboard
    payloads=$(grep -Ei "(^rO0|^H4)" /tmp/docker_output.log)
    if [ -n "$payloads" ]; then
        echo "$payloads" | xclip -selection clipboard
        echo "The payloads have been copied to the clipboard."
    else
        echo "No payloads were generated."
    fi

else
    echo "Invalid option."
fi
