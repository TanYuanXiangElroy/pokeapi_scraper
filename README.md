# ![pokeball](image.png) Pokedex Data Pipeline (ETL)

A robust data engineering pipeline that fetches, cleans, and normalizes Pokémon data from the PokéAPI.
This script doesn't just download raw data; it transforms it into an "Application Ready" format for Machine Learning and App Development. It pre-calculates type matchups (weaknesses/resistances), creates placeholders for missing data, and generates both JSON and CSV outputs.

## Download the Data
If you don't want to run the code and just want the finished dataset (Gen 1-9), you can download it directly from Kaggle:
https://www.kaggle.com/datasets/elroytan/pokemondata

## Features
- Complete Collection: Fetches all 1025+ Pokémon (Gen 1 to Gen 9).
- Type Math Logic: Automatically calculates the 18-type damage effectiveness (Weakness/Resistance/Immunity) based on dual typing.
- Robust Error Handling: Uses defensive programming (.get(), placeholder text) to ensure the pipeline never crashes, even if API endpoints are missing data.
- Multimedia Integration: Includes direct URLs to official  Sprites and Audio Cries.
- Data Cleaning: Normalizes text (removes \n, \f,'\u00e9') and converts units for consistency.

## How to Run
1. Prerequisites
You need Python installed. It is recommended to use a virtual environment.

```Bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/pokedex-data-pipeline.git
cd pokedex-data-pipeline

# Create virtual environment (Optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install requests

```
2. Execute the Pipeline

Run the main script to generate the JSON database:

```Bash
python API_File.py
```
Note: By default, the script takes about 10-15 minutes to process all 1025 Pokémon due to API rate limiting we set.
3. Convert to CSV (Optional)
If you need a flat CSV file for Excel or Pandas analysis:

```Bash
python json_to_csv.py
```
## Customization
Want different data? Here is how you can tweak the pipeline for your specific needs.

1. Change the range (Testing)
If you only want the first 151 Pokémon (Gen 1), open API_File.py and change the limit at the bottom:

```Python
# api.py
if __name__ == "__main__":
    fetch_all_pokemon(limit=151) # Changed from 1025
```

2. Add specific stats
If you want to grab more specific data (like Egg Groups or Catch Rate), modify the entry dictionary in the main loop:

```Python
# Inside the fetch_all_pokemon loop
entry = {
    "id": data['id'],
    # Add your new field here
    "base_experience": data.get('base_experience'),
    ...
}
```

### 2. Add More Stats (Non-Exhaustive List)
The PokéAPI provides extensive data. While this pipeline fetches the fields I need, you can easily modify the script to include advanced game mechanics.

Here are some popular fields you might want to add:

| Stat Name | API Source | Variable in Script | Description |
| :--- | :--- | :--- | :--- |
| **Base Experience** | Main Data | `data.get('base_experience')` | EXP yield for defeating the Pokemon. |
| **Catch Rate** | Species Data | `species_data.get('capture_rate')` | Integer (1-255) defining capture difficulty. |
| **Growth Rate** | Species Data | `species_data['growth_rate']['name']` | Leveling speed (e.g., "Slow", "Fast"). |
| **Base Happiness** | Species Data | `species_data.get('base_happiness')` | Starting friendship value (usually 70). |
| **Egg Groups** | Species Data | `species_data['egg_groups']` | List of breeding compatibilities. |

**Example Implementation:**
To add **Base Experience** and **Catch Rate**, modify the `fetch_all_pokemon` loop in `API_File.py`:

```python
# 1. Get the data
base_exp = data.get('base_experience')
catch_rate = species_data.get('capture_rate')

# 2. Add to the entry dictionary
entry = {
    "id": data['id'],
    "name": data['name'],
    "base_experience": base_exp,  # <--- New Field
    "capture_rate": catch_rate,   # <--- New Field
    # ... rest of the data
}

## Project Structure

```Text
/pokedex-data-pipeline
  ├── api.py                # The main ETL logic
  ├── json_to_csv.py        # Utility to flatten JSON to CSV
  ├── complete_pokedex.json # The Generated Database (Output)
  ├── pokemon_gen9.csv      # The Generated Spreadsheet(Output)
  ├── .gitignore            # Git configuration
  └── README.md             # Documentation
```

## Acknowledgements
Data sourced from the open-source PokéAPI.
Inspired by the "Pidexter" project by BigRig Creates.