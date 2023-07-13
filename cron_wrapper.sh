#!/bin/bash

cd /home/$USER/Desktop/OptiTest

# Run the main.py script and capture the output
output=$(python3 main.py)

# Define the file path and name for the HTML output
output_dir="/home/$USER/Desktop/OptiTest/outputlogs"
output_file="$output_dir/output_$(date '+%Y-%m-%d').html"

# Write the output to the HTML file
echo "$output" > "$output_file"


chmod 644 "$output_file"
