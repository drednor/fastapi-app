import json
import os

file = "temp.txt"

with open(file, 'r') as input_file:
    temp = ""
    for line in input_file:
        temp += line.strip()

try:
    output_json = json.loads(temp)
    print("Extracted JSON data:", output_json)
except json.decoder.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit(1)

print("this is the output = ",output_json)