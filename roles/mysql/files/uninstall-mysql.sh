#!/bin/bash

# Check that helper function directory exists
DIRECTORY_CURRENT_SKRIPT="$(dirname "$0")"
DIRECTORY_HELPER="$DIRECTORY_CURRENT_SKRIPT/../../../files"

import_helper_function() {
    local helper_file="$1"
    if [ -d "$DIRECTORY_HELPER" ] && [ -f "$DIRECTORY_HELPER/$helper_file" ]; then
        source "$DIRECTORY_HELPER/$helper_file"
    else
        echo "ERROR: Helper function '$helper_file' not found."
    fi
}

import_helper_function "log_message.sh"
import_helper_function "display_warning.sh"

display_warning "This action removes MySQL packages, databases and data. Are you sure to continue?" "$@"

# Are we root?
if [ "$EUID" -ne 0 ]; then
    log_message "ERROR" "Insufficient permissions to remove MySQL configuration and data."

    exit 1
fi

# Uninstall all MySQL-related packages
if dpkg -l | grep -q '^ii.*mysql-'; then
    apt-get remove --purge -y '^mysql-'
    apt-get autoremove -y
else
    log_message "INFO" "No MySQL-related packages found."
fi

# Remove MySQL configuration and data
if [ -d /etc/mysql ] || [ -d /var/lib/mysql ]; then
    # Check for permissions before removing files
    if [ -w /etc/mysql ] && [ -w /var/lib/mysql ]; then
        rm -r /etc/mysql /var/lib/mysql
        log_message "INFO" "MySQL configuration and data have been removed."
    else
        log_message "WARNING" "Insufficient permissions to remove MySQL configuration and data."
    fi
else
    log_message "INFO" "MySQL configuration and data directories not found."
fi

log_message "INFO" "Uninstallation process completed on $(date)."

# Note: that this script does not not purge log files, future references
