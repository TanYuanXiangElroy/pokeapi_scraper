import requests
import json
import time
import config

# --- HELPER: Pre-fetch Type Rules ---
def get_type_chart():
    print("--- Pre-loading Type Chart (Doing the math logic) ---")
    type_chart = {}
    
    for i in range(1, 19): 
        url = f"{config.POKE_API_BASE_URL}/type/{i}"
        data = requests.get(url).json()
        type_name = data['name']
        type_chart[type_name] = data['damage_relations']
        
    print("--- Type Chart Loaded! ---")
    return type_chart

# --- HELPER: Calculate Weaknesses ---
def calculate_weaknesses(pokemon_types, type_chart):
    weaknesses = {
        "normal": 1.0, "fire": 1.0, "water": 1.0, "electric": 1.0, "grass": 1.0, 
        "ice": 1.0, "fighting": 1.0, "poison": 1.0, "ground": 1.0, "flying": 1.0, 
        "psychic": 1.0, "bug": 1.0, "rock": 1.0, "ghost": 1.0, "dragon": 1.0, 
        "steel": 1.0, "dark": 1.0, "fairy": 1.0
    }
    
    for p_type in pokemon_types:
        relations = type_chart.get(p_type)
        if not relations: continue
            
        for t in relations['double_damage_from']:
            t_name = t['name']
            if t_name in weaknesses: weaknesses[t_name] *= 2.0
            
        for t in relations['half_damage_from']:
            t_name = t['name']
            if t_name in weaknesses: weaknesses[t_name] *= 0.5
            
        for t in relations['no_damage_from']:
            t_name = t['name']
            if t_name in weaknesses: weaknesses[t_name] *= 0.0
            
    return weaknesses

def fetch_pokeapi(limit=1025):
    all_pokemon  = []
    type_chart = get_type_chart()
    
    print(f"Starting download of {limit} Pokemon from standard PokeAPI...")
    
    for i in range(1, limit + 1):
        try:
            url = f"{config.POKE_API_BASE_URL}/pokemon/{i}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to get data for Pokemon ID {i}, status code: {response.status_code}")
                continue
            
            data = response.json()
            
            species_url = data['species']['url']
            species_response = requests.get(species_url)
            current_types = [t['type']['name'] for t in data['types']]

            description = "No description available."
            category = "Unknown Category"      
            habitat = "Unknown Habitat"
            evolves_from = "None"
            generation = "Unknown Generation"
            is_legendary = False
            is_mythical = False
            stats = {}
            damage_taken = {}
            
            if species_response.status_code == 200:
                species_data = species_response.json()
                for entry in species_data.get('flavor_text_entries', []):
                    if entry['language']['name'] == 'en':
                        description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').replace('\u00e9', 'e')
                        break
                for genus in species_data.get('genera', []):
                    if genus['language']['name'] == 'en':
                        category = genus['genus'].replace('\u00e9', 'e')
                        break
                if species_data.get('habitat'):
                    habitat = species_data['habitat']['name'].capitalize()
                if species_data.get('evolves_from_species'):
                        evolves_from = species_data['evolves_from_species']['name'].capitalize()
                if species_data.get('generation'):
                    generation = species_data['generation']['name'].capitalize()
                is_legendary = species_data.get('is_legendary', False)
                is_mythical = species_data.get('is_mythical', False)

                cry_url = data['cries'].get('latest', None)
                abilities = []
                for ab in data['abilities']:
                    name = ab['ability']['name'].replace('-', ' ').capitalize()
                    if ab['is_hidden']: name += " (Hidden)"
                    abilities.append(name)

                stats = {}
                for stat_item in data['stats']:
                    stat_name = stat_item['stat']['name']
                    stat_value = stat_item['base_stat']
                    stats[stat_name] = stat_value

                damage_taken = calculate_weaknesses(current_types, type_chart)

            entry = {
                "id": data['id'],
                "name": data['name'],
                "category": category,
                "generation": generation,         
                "is_legendary": is_legendary,     
                "is_mythical": is_mythical,       
                "types": [t['type']['name'] for t in data['types']],
                "height": data['height'] / 10,
                "weight": data['weight'] / 10,
                "habitat": habitat,               
                "evolves_from": evolves_from,   
                "description": description,  
                 "stats": {
                    "hp": stats.get('hp', 0),
                    "attack": stats.get('attack', 0),
                    "defense": stats.get('defense', 0),
                    "special_attack": stats.get('special-attack', 0), 
                    "special_defense": stats.get('special-defense', 0),
                    "speed": stats.get('speed', 0)
                },
                "damage_taken": damage_taken,
                "abilities": abilities,
                "cry_url": cry_url,
                "shiny_sprite_url": data['sprites']['front_shiny'],
                "sprite_url": data['sprites']['front_default']
            }
            all_pokemon.append(entry)
            print(f"Got #{i}: {data['name']}")
            time.sleep(0.1) 
        except Exception as e:
            print(f"Error fetching #{i}: {e}")

    with open('complete_pokedex.json', 'w') as f:
        json.dump(all_pokemon , f, indent=4)
    print("Done! Data saved to complete_pokedex.json")

def fetch_tcg(limit=100):
    print(f"Starting download of {limit} Pokemon cards from TCG API...")
    all_cards = []
    page = 1
    fetched = 0

    while fetched < limit:
        try:
            url = f"{config.TCG_API_BASE_URL}/cards?page={page}&pageSize=50"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to get TCG data, status code: {response.status_code}")
                break

            data = response.json().get('data', [])
            if not data:
                break

            for card in data:
                if fetched >= limit:
                    break
                entry = {
                    "id": card.get('id'),
                    "name": card.get('name'),
                    "supertype": card.get('supertype'),
                    "subtypes": card.get('subtypes', []),
                    "hp": card.get('hp'),
                    "types": card.get('types', []),
                    "evolvesFrom": card.get('evolvesFrom'),
                    "rules": card.get('rules', []),
                    "attacks": [{"name": a.get('name'), "cost": a.get('cost'), "damage": a.get('damage'), "text": a.get('text')} for a in card.get('attacks', [])],
                    "weaknesses": [{"type": w.get('type'), "value": w.get('value')} for w in card.get('weaknesses', [])],
                    "retreatCost": card.get('retreatCost', []),
                    "set_id": card.get('set', {}).get('id'),
                    "set_name": card.get('set', {}).get('name'),
                    "rarity": card.get('rarity'),
                    "flavorText": card.get('flavorText'),
                    "image_small": card.get('images', {}).get('small'),
                    "image_large": card.get('images', {}).get('large')
                }
                all_cards.append(entry)
                print(f"Got TCG Card: {entry['name']} ({entry['id']})")
                fetched += 1

            page += 1
            time.sleep(0.5)

        except Exception as e:
            print(f"Error fetching TCG page {page}: {e}")
            break

    with open('tcg_pokedex.json', 'w') as f:
        json.dump(all_cards, f, indent=4)
    print("Done! Data saved to tcg_pokedex.json")

def fetch_smogon():
    print(f"Starting download of Smogon competitive Pokemon data...")
    try:
        response = requests.get(config.SMOGON_DATA_URL)
        if response.status_code != 200:
            print(f"Failed to get Smogon data, status code: {response.status_code}")
            return

        data = response.json()
        all_pokemon = []

        for key, mon in data.items():
            entry = {
                "id": mon.get('num'),
                "name": mon.get('name'),
                "types": mon.get('types', []),
                "baseStats": mon.get('baseStats', {}),
                "abilities": mon.get('abilities', {}),
                "heightm": mon.get('heightm'),
                "weightkg": mon.get('weightkg'),
                "color": mon.get('color'),
                "evos": mon.get('evos', []),
                "prevo": mon.get('prevo'),
                "eggGroups": mon.get('eggGroups', []),
                "tier": mon.get('tier')
            }
            all_pokemon.append(entry)
            print(f"Got Smogon Pokemon: {entry['name']}")

        with open('smogon_pokedex.json', 'w') as f:
            json.dump(all_pokemon, f, indent=4)
        print("Done! Data saved to smogon_pokedex.json")

    except Exception as e:
        print(f"Error fetching Smogon data: {e}")

def fetch_pokeapi_game_specific(limit=1025, game_version="red"):
    print(f"Starting download of {limit} Pokemon from PokeAPI for game version: {game_version}...")
    all_pokemon = []

    for i in range(1, limit + 1):
        try:
            url = f"{config.POKE_API_BASE_URL}/pokemon/{i}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to get data for Pokemon ID {i}, status code: {response.status_code}")
                continue

            data = response.json()

            # Filter for specific game indices
            game_index = None
            for gi in data.get('game_indices', []):
                if gi['version']['name'] == game_version:
                    game_index = gi['game_index']
                    break

            entry = {
                "id": data['id'],
                "name": data['name'],
                "game_version": game_version,
                "game_index": game_index,
                "types": [t['type']['name'] for t in data['types']],
                "height": data['height'] / 10,
                "weight": data['weight'] / 10,
                "sprite_url": data['sprites']['front_default']
            }
            all_pokemon.append(entry)
            print(f"Got #{i} for {game_version}: {data['name']}")
            time.sleep(0.1)

        except Exception as e:
            print(f"Error fetching #{i} for game version {game_version}: {e}")

    with open(f'pokeapi_{game_version}_pokedex.json', 'w') as f:
        json.dump(all_pokemon, f, indent=4)
    print(f"Done! Data saved to pokeapi_{game_version}_pokedex.json")

if __name__ == "__main__":
    print(f"Current DATA_SOURCE: {config.DATA_SOURCE}")
    if config.DATA_SOURCE == "pokeapi":
        fetch_pokeapi(limit=1025) # Defaulting to 151 for faster tests, user can change to 1025
    elif config.DATA_SOURCE == "tcg":
        fetch_tcg(limit=100) # Defaulting to 100 cards
    elif config.DATA_SOURCE == "smogon":
        fetch_smogon()
    elif config.DATA_SOURCE == "pokeapi_game":
        fetch_pokeapi_game_specific(limit=1025, game_version=config.GAME_VERSION)
    else:
        print(f"Unknown DATA_SOURCE: {config.DATA_SOURCE}")
