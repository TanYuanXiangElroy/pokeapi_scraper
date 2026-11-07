# <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Pok%C3%A9_Ball_icon.svg" width="40" align="center" /> Pokedex Data Pipeline
A robust data engineering pipeline that fetches, cleans, and normalizes Pokémon data from various APIs into an "Application Ready" format for Machine Learning and App Development.

## 🌟 New Features!
- **Multiple Environments:** Easily swap data sources! You can now pull data from **four** different sources:
  1. Standard PokéAPI (Default stats & lore).
  2. Pokémon TCG API (Trading Card Game stats, HP, and set data).
  3. Smogon / Pokemon Showdown (Competitive tiers and usage).
  4. Game-Specific PokéAPI (Stats and sprites specific to games like Red, Crystal, or Emerald).
- **Docker Support:** Run the pipeline in a container without installing Python dependencies.
- **Google Colab Notebook:** Run the pipeline entirely in the cloud, straight from your browser.
- **Dynamic CSV Converter:** The `json_to_csv.py` file dynamically reads any JSON structure you output and flattens it automatically.

## How to Run

### Method 1: Google Colab (Zero Setup)
If you don't want to install anything on your computer, you can run this script directly in the cloud:
1. Upload the `Pokemon_Scraper_Colab.ipynb` file to [Google Colab](https://colab.research.google.com/).
2. Run the cells to choose your data source, execute the pipeline, and automatically download the JSON & CSV files directly to your computer!

### Method 2: Docker & Docker Compose (Recommended for Local)
Ensure you have Docker installed on your machine.
1. Clone the repo: `git clone https://github.com/TanYuanXiangElroy/pokeapi_scraper.git`
2. Run the scraper:
```bash
docker-compose up --build
```
This automatically installs all dependencies, runs the scraper, converts the data to CSV, and saves the `.json` and `.csv` files safely into the local `data/` folder on your computer.

### Method 3: Standard Python Execution
1. Clone the repo and install dependencies:
```bash
pip install -r requirements.txt
```
2. Edit `config.py` to select your `DATA_SOURCE`. Options include `"pokeapi"`, `"tcg"`, `"smogon"`, or `"pokeapi_game"`.
3. Run the API scraper:
```bash
python api.py
```
4. Convert the generated JSON to CSV:
```bash
python json_to_csv.py
```

## Customization
Want different data? Open `config.py` and modify the `DATA_SOURCE` variable:
```python
# config.py
DATA_SOURCE = "tcg"  # Will now scrape from the Pokémon TCG API!
```

## Project Structure
```Text
/pokedex-data-pipeline
  ├── api.py                      # The main ETL logic
  ├── config.py                   # Swappable Environment Configs
  ├── json_to_csv.py              # Dynamic Utility to flatten JSON to CSV
  ├── Dockerfile                  # Docker build instructions
  ├── docker-compose.yml          # Easy Docker execution & volume mapping
  ├── Pokemon_Scraper_Colab.ipynb # Cloud-ready Jupyter Notebook
  ├── requirements.txt            # Python dependencies
  └── README.md                   # Documentation
```

## Acknowledgements
- Data sourced from the open-source [PokéAPI](https://pokeapi.co/docs/v2#google_vignette).
- Card Data sourced from [Pokémon TCG API](https://docs.pokemontcg.io/).
- Competitive Data sourced from [Pokémon Showdown](https://play.pokemonshowdown.com/data/).
- Inspired by the "Pidexter" project by BigRig Creates.
