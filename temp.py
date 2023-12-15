import json
import os
x = """
{"instance_id": {"sensitive": false,"type": "string","value": "i-02cb6e3762cdfdba2"},"public_ip": {"sensitive": false,"type": "string","value": "34.228.159.118"},"region": {"sensitive": false,"type": "string","value": "us-east-1"}}::debug::Terraform exited with code 0.::debug::stdout: {%0A  "instance_id": {%0A    "sensitive": false,%0A    "type": "string",%0A    "value": "i-02cb6e3762cdfdba2"%0A  },%0A  "public_ip": {%0A    "sensitive": false,%0A    "type": "string",%0A    "value": "34.228.159.118"%0A  },%0A  "region": {%0A    "sensitive": false,%0A    "type": "string",%0A    "value": "us-east-1"%0A  }%0A}%0A::debug::stderr:::debug::exitcode: 0::set-output name=stdout::{%0A  "instance_id": {%0A    "sensitive": false,%0A    "type": "string",%0A    "value": "i-02cb6e3762cdfdba2"%0A  },%0A  "public_ip": {%0A    "sensitive": false,%0A    "type": "string",%0A    "value": "34.228.159.118"%0A  },%0A  "region": {%0A    "sensitive": false,%0A    "type": "string",%0A    "value": "us-east-1"%0A  }%0A}"""
json_sata = """ [command]/home/runner/work/_temp/cc123a87-1cfd-4991-92f0-cd75e352f8af/terraform-bin output -json
{
  "instance_id": {
    "sensitive": false,
    "type": "string",
    "value": "i-033bb1f8e4abcb7df"
  },
  "public_ip": {
    "sensitive": false,
    "type": "string",
    "value": "3.84.46.217"
  },
  "region": {
    "sensitive": false,
    "type": "string",
    "value": "us-east-1"
  }
}"""

print("Terraform output:", json_sata)
json_start = json_sata.find('{')
json_end = json_sata.rfind('}') + 1
json_data = json_sata[json_start:json_end]
print(json_data)
with open("a.txt", 'w') as output_file:
    output_file.write(json_data)

with open("a.txt", 'r') as input_file:
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