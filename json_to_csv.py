import json
import csv
import sys
import glob

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # If the list is all strings or numbers, we join it.
            if all(isinstance(i, (str, int, float)) for i in v):
                items.append((new_key, ", ".join(map(str, v))))
            else:
                # For complex objects (like TCG attacks), convert to string representation
                items.append((new_key, json.dumps(v)))
        else:
            items.append((new_key, v))
    return dict(items)

def convert_to_csv(json_filename, csv_filename):
    try:
        with open(json_filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_filename} not found!")
        return

    if not data:
        print("Error: JSON file is empty!")
        return

    flattened_data = [flatten_dict(item) for item in data]

    # Collect all unique keys across all items to use as headers
    headers = set()
    for item in flattened_data:
        headers.update(item.keys())

    # Sort headers so ID and Name appear first, if they exist
    headers = sorted(list(headers))
    if 'name' in headers:
        headers.remove('name')
        headers.insert(0, 'name')
    if 'id' in headers:
        headers.remove('id')
        headers.insert(0, 'id')

    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        for item in flattened_data:
            writer.writerow(item)

    print(f"Success! Converted {json_filename} to {csv_filename}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        convert_to_csv(sys.argv[1], sys.argv[2])
    else:
        # Default behavior: Find all JSON files and convert them automatically
        json_files = glob.glob('*pokedex*.json')
        if not json_files:
            print("No JSON pokedex files found to convert.")
        else:
            for json_file in json_files:
                csv_file = json_file.replace('.json', '.csv')
                convert_to_csv(json_file, csv_file)
