import json
import csv

def convert_to_csv():
    # 1. Load the JSON data
    try:
        with open('complete_pokedex.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: complete_pokedex.json not found!")
        return

    # 2. Open a new CSV file
    with open('pokemon_gen9.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # 3. Create the Headers (The top row)
        # We list the basic columns, then manually add the stats and damage types
        headers = [
            "id", "name", "category", "generation", "is_legendary", "is_mythical",
            "types", "height", "weight", "abilities", "habitat", "evolves_from", 
            "description", 
            # Flattened Stats
            "hp", "attack", "defense", "special_attack", "special_defense", "speed",
            # Flattened Damage Taken
            "against_normal", "against_fire", "against_water", "against_electric", "against_grass", 
            "against_ice", "against_fighting", "against_poison", "against_ground", "against_flying", 
            "against_psychic", "against_bug", "against_rock", "against_ghost", "against_dragon", 
            "against_steel", "against_dark", "against_fairy",
            # Media
            "cry_url", "sprite_url", "shiny_sprite_url"
        ]
        writer.writerow(headers)

        # 4. Loop through Pokemon and extract data
        for p in data:
            # Flatten Lists: Convert ['Fire', 'Flying'] to "Fire, Flying"
            types_str = ", ".join(p['types'])
            abilities_str = ", ".join(p['abilities'])
        
            
            row = [
                p['id'],
                p['name'],
                p['category'],
                p['generation'],
                p['is_legendary'], 
                p['is_mythical'],
                types_str,
                p['height'], 
                p['weight'], 
                abilities_str,
                p['habitat'],
                p['evolves_from'],
                p['description'],
                
                # Stats
                p['stats']['hp'],
                p['stats']['attack'],
                p['stats']['defense'],
                p['stats']['special_attack'],
                p['stats']['special_defense'],
                p['stats']['speed'],
                
                # Damage Taken (18 Types)
                p['damage_taken']['normal'],
                p['damage_taken']['fire'],
                p['damage_taken']['water'],
                p['damage_taken']['electric'],
                p['damage_taken']['grass'],
                p['damage_taken']['ice'],
                p['damage_taken']['fighting'],
                p['damage_taken']['poison'],
                p['damage_taken']['ground'],
                p['damage_taken']['flying'],
                p['damage_taken']['psychic'],
                p['damage_taken']['bug'],
                p['damage_taken']['rock'],
                p['damage_taken']['ghost'],
                p['damage_taken']['dragon'],
                p['damage_taken']['steel'],
                p['damage_taken']['dark'],
                p['damage_taken']['fairy'],
                
                p['cry_url'],
                p['sprite_url'],
                p['shiny_sprite_url']
            ]
            
            writer.writerow(row)

    print("Success! Converted to pokemon_gen9.csv")

if __name__ == "__main__":
    convert_to_csv()