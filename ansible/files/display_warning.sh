#!/bin/bash

# Function to display a warning message and ask for confirmation
warning_with_confirmation() {
    local warning_message="WARNING: $1"
    echo "$warning_message"
    echo "Are you sure you want to continue? (yes/no)"

    read confirmation

    # Convert the input to lowercase using parameter expansion
    confirmation="${confirmation,,}"
    case "$confirmation" in
        y|yes)
            # Proceed with the action
            ;;
        *)
            echo "Action canceled."
            exit 1
            ;;
    esac
}

display_warning() {
    local force="$1"
    shift
    while getopts ":f" opt; do
        case "$opt" in
            f) force=1 ;;
            \?) echo "Invalid option: -$OPTARG" >&2
                exit 1
                ;;
        esac
    done


    # Shift the processed options so that $1 refers to the first non-option argument
    shift $((OPTIND-1))

    if [ "$force" = 1 ]; then
        echo "Force option detected. Skipping warning and proceeding with the action..."
    else
        warning_with_confirmation "$force"

        echo "Continuing with the action..."
    fi
}
