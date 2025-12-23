import requests
import json
import time
import config

# --- HELPER: Pre-fetch Type Rules ---
def get_type_chart():
    print("--- Pre-loading Type Chart (Doing the math logic) ---")
    type_chart = {}
    
    # There are 18 main types
    # We fetch them once so we don't have to call the API 1000 times later
    for i in range(1, 19): 
        url = f"{config.POKE_API_BASE_URL}/type/{i}"
        data = requests.get(url).json()
        type_name = data['name']
        
        # Store the damage relations
        type_chart[type_name] = data['damage_relations']
        
    print("--- Type Chart Loaded! ---")
    return type_chart

# --- HELPER: Calculate Weaknesses ---
def calculate_weaknesses(pokemon_types, type_chart):
    # 1. Start with neutral (1.0) for all 18 types
    weaknesses = {
        "normal": 1.0, "fire": 1.0, "water": 1.0, "electric": 1.0, "grass": 1.0, 
        "ice": 1.0, "fighting": 1.0, "poison": 1.0, "ground": 1.0, "flying": 1.0, 
        "psychic": 1.0, "bug": 1.0, "rock": 1.0, "ghost": 1.0, "dragon": 1.0, 
        "steel": 1.0, "dark": 1.0, "fairy": 1.0
    }
    
    # 2. Loop through the Pokemon's types (e.g., ['fire', 'flying'])
    for p_type in pokemon_types:
        relations = type_chart.get(p_type)
        if not relations: continue
            
        # 3. Apply Multipliers
        # Double Damage From (Weakness) -> x2
        for t in relations['double_damage_from']:
            t_name = t['name']
            if t_name in weaknesses: weaknesses[t_name] *= 2.0
            
        # Half Damage From (Resistance) -> x0.5
        for t in relations['half_damage_from']:
            t_name = t['name']
            if t_name in weaknesses: weaknesses[t_name] *= 0.5
            
        # No Damage From (Immunity) -> x0
        for t in relations['no_damage_from']:
            t_name = t['name']
            if t_name in weaknesses: weaknesses[t_name] *= 0.0
            
    return weaknesses

def fetch_all_pokemon(limit=1025): # As of Gen 9, there are about 1025 mons
    all_pokemon  = []
    type_chart = get_type_chart()
    
    print(f"Starting download of {limit} Pokemon...")
    
    for i in range(1, limit + 1):
        try:
            #call the main poke data
            url = f"{config.POKE_API_BASE_URL}/pokemon/{i}"
            response = requests.get(url)
            if response.status_code != 200: #fail
                print(f"Failed to get data for Pokemon ID {i}, status code: {response.status_code}")
                continue
            
            data = response.json()
            
            # Species Data
            species_url = data['species']['url']
            species_response = requests.get(species_url)
            current_types = [t['type']['name'] for t in data['types']]

            #place holder text
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

                # Find English description
                for entry in species_data.get('flavor_text_entries', []):
                    if entry['language']['name'] == 'en':
                        # Clean up text (remove newlines like \n and \f)
                        description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').replace('\u00e9', 'e')
                        break

                #clasification
                for genus in species_data.get('genera', []):
                    if genus['language']['name'] == 'en':
                        category = genus['genus'].replace('\u00e9', 'e')
                        break

                #habitat
                if species_data.get('habitat'):
                    habitat = species_data['habitat']['name'].capitalize()

                #evolution chain, who is the child
                if species_data.get('evolves_from_species'):
                        evolves_from = species_data['evolves_from_species']['name'].capitalize()

                 # Generation 
                if species_data.get('generation'):
                    generation = species_data['generation']['name'].capitalize()

                # Legendary/Mythical 
                # These are Boolean (True/False)
                is_legendary = species_data.get('is_legendary', False)
                is_mythical = species_data.get('is_mythical', False)

                cry_url = data['cries'].get('latest', None) # Get the sound file

                abilities = []
                for ab in data['abilities']:
                    name = ab['ability']['name'].replace('-', ' ').capitalize()
                    if ab['is_hidden']: name += " (Hidden)"
                    abilities.append(name)


                # The API returns a list, so we convert it to a dictionary for easier use
                stats = {}
                for stat_item in data['stats']:
                    stat_name = stat_item['stat']['name']
                    stat_value = stat_item['base_stat']
                    stats[stat_name] = stat_value

                # Pre-fetch type chart
                damage_taken = calculate_weaknesses(current_types, type_chart)

            # Build the clean entry
            entry = {
                "id": data['id'],
                "name": data['name'],
                "category": category,
                "generation": generation,         
                "is_legendary": is_legendary,     
                "is_mythical": is_mythical,       
                "types": [t['type']['name'] for t in data['types']],
                #(Converts to Meters and KG)
                "height": data['height'] / 10,  # 3 becomes 0.3m
                "weight": data['weight'] / 10,  # 29 becomes 2.9kg
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
                "damage_taken": damage_taken, # the 18 weaknesses/resistances/immunities
                "abilities": abilities,
                "cry_url": cry_url,
                "shiny_sprite_url": data['sprites']['front_shiny'],
                "sprite_url": data['sprites']['front_default']
                
            }
            
            all_pokemon .append(entry)
            print(f"Got #{i}: {data['name']}")
                
            # Be nice to the API, don't spam it too fast
            time.sleep(0.1) 
            
        except Exception as e:
            print(f"Error fetching #{i}: {e}")

    # Save to JSON for Kaggle
    with open('complete_pokedex.json', 'w') as f:
        json.dump(all_pokemon , f, indent=4)
    
    print("Done! Data saved to complete_pokedex.json")

# Run it
fetch_all_pokemon(limit=1025) # Change this to 1025 when you are ready for the full download