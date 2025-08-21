import requests
import json

headers = {
    'User-Agent': 'SCRYMAGE/1.0',  
    'Accept': 'application/json;q=0.9,*/*;q=0.8' # default from scryfall docs
}

response = requests.get('https://api.scryfall.com/bulk-data', headers=headers)
if response.status_code != 200:
    print(f"Error: {response.status_code} - {response.text}")
    exit(1)

print(json.dumps(response.json(), indent=2))

download_uri = response.json()['data'][0]['download_uri']
updated_at = response.json()['data'][0]['updated_at'].replace(":", "-")

print(f"Download URI: {download_uri}")

# Download the file from download_uri
download_response = requests.get(download_uri, headers=headers)
with open(f'{updated_at}_scryfall_bulk_data.json', 'wb') as f:
    f.write(download_response.content)
print(f"Downloaded bulk data to {updated_at}_scryfall_bulk_data.json")



"""
def function_name(parameters):
    # function body
    return value  # optional
"""