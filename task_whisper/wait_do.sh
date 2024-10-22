#!/bin/bash

# Duration is 10000 seconds
duration=9000

echo "Starting 10000 seconds countdown..."

while [ $duration -gt 0 ]; do
    # Calculate hours, minutes and seconds from duration
    hours=$((duration / 3600))
    mins=$((duration % 3600 / 60))
    secs=$((duration % 60))
    
    # Clear the line and move the cursor to the beginning of the line
    echo -ne "\rWaiting: ${hours}h ${mins}m ${secs}s left"

    # Decrement the duration by one second and sleep
    ((duration--))
    sleep 1
done

echo -e "\nTime's up!"

# Place the code you want to execute after the countdown below
echo "Executing the command..."

# Run the command

python train.py >> small.log