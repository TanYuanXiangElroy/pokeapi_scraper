# config.py

# Which data source to use?
# Options: "pokeapi", "tcg", "smogon", "pokeapi_game"
DATA_SOURCE = "pokeapi_game"

# --- 1. Standard Poke API ---
# their doc https://pokeapi.co/docs/v2
POKE_API_BASE_URL = "https://pokeapi.co/api/v2"

# --- 2. Pokemon TCG API ---
# https://docs.pokemontcg.io/
TCG_API_BASE_URL = "https://api.pokemontcg.io/v2"

# --- 3. Smogon / Pokemon Showdown Data ---
# https://play.pokemonshowdown.com/data/
SMOGON_DATA_URL = "https://play.pokemonshowdown.com/data/pokedex.json"

# --- 4. Game Specific Poke API ---
# If using DATA_SOURCE = "pokeapi_game", which game version?
# e.g., "red", "crystal", "emerald", "scarlet"
GAME_VERSION = "red"
