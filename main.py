import random
import requests
import json


def download_scryfall_bulk_data():
    headers = {
        'User-Agent': 'SCRYMAGE/1.0',  
        'Accept': 'application/json;q=0.9,*/*;q=0.8' # default from scryfall docs
    }

    response = requests.get('https://api.scryfall.com/bulk-data', headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return False

    print(json.dumps(response.json(), indent=2))

    download_uri = response.json()['data'][0]['download_uri']
    updated_at = response.json()['data'][0]['updated_at'].replace(":", "-")

    print(f"Download URI: {download_uri}")

    # Download the file from download_uri
    download_response = requests.get(download_uri, headers=headers)
    with open(f'{updated_at}_scryfall_bulk_data.json', 'wb') as f:
        f.write(download_response.content)
    print(f"Downloaded bulk data to {updated_at}_scryfall_bulk_data.json")
    return True


def simulate_booster_opening(config_path, scryfall_data_path, save_to=None):
    """
    Simulates a booster opening based on the config and Scryfall data.
    Args:
        config_path (str): Path to the booster config JSON file.
        scryfall_data_path (str): Path to the Scryfall bulk data JSON file.
        save_to (str, optional): If provided, save the output to this file as JSON.
    Returns:
        list: List of card dicts representing the opened booster.
    """
    filter_fields = [
        'id', 'tcgplayer_id', 'name', 'mana_cost', 'type_line', 'oracle_text',
        'power', 'toughness', 'colors', 'keywords', 'finishes', 'set', 'flavor_text', 'prices'
    ]
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    with open(scryfall_data_path, 'r', encoding='utf-8') as f:
        scryfall_data = json.load(f)
        if isinstance(scryfall_data, dict) and 'data' in scryfall_data:
            cards = scryfall_data['data']
        else:
            cards = scryfall_data

    booster = []
    for slot in config['slots']:
        for _ in range(slot['count']):
            options = slot['options']
            # Weighted random choice based on 'probability'
            weights = [opt.get('probability', 1) for opt in options]
            chosen_option = random.choices(options, weights=weights, k=1)[0]
            # Very basic query filter: only supports set code for now
            set_code = chosen_option.get('set')
            filtered = [c for c in cards if c.get('set') == set_code] if set_code else cards
            # Copilot says "TODO: Implement full query parsing for more accurate filtering"
            if filtered:
                card = random.choice(filtered)
                booster.append(card)

    booster = [
        {k: card.get(k) for k in filter_fields if k in card}
        for card in booster
    ]

    if save_to:
        with open(save_to, 'w', encoding='utf-8') as f:
            f.write(json.dumps(booster, indent=2))

    return booster

# from main import simulate_booster_opening; import json
booster = simulate_booster_opening(
    r'booster_configs\\ff_play_booster.json',
    r'2025-08-20T21-06-53.357+00-00_scryfall_bulk_data.json',
    save_to='booster_output.txt'
)
#print(json.dumps(booster, indent=2))