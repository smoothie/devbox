#!/bin/bash

# Log messages in custom format (Log4j Pattern Layout)
log_message() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local level="$1"
    local message="$2"
    local script_name="${0##*/}"  # Get the script name without the path

    local log_format="$timestamp [$level] $script_name - $message"

    echo "$log_format" >&2

#    echo "$timestamp [$level] $script_name - $message"
}
