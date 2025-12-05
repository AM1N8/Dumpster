"""
GameVerse Game Database
Manages game data and provides data access functions
"""

import streamlit as st
import pandas as pd


@st.cache_data
def load_games():
    """
    Load game database and return as DataFrame
    
    Returns:
        pd.DataFrame: DataFrame containing all game data
    """
    games = [
        {
            "id": 1,
            "title": "Cyber Nexus 2077",
            "price": 59.99,
            "category": "Action",
            "tags": ["Open World", "RPG", "Cyberpunk"],
            "description": "Dive into a neon-lit dystopian future where your choices shape the city.",
            "rating": 4.5,
            "release_date": "2024-03-15",
            "developer": "NeonDream Studios",
            "image_url": "images/CyberNexus2077.png"
        },
        {
            "id": 2,
            "title": "Mystic Legends",
            "price": 39.99,
            "category": "RPG",
            "tags": ["Fantasy", "Story-Rich", "Magic"],
            "description": "Embark on an epic quest through magical realms filled with ancient secrets.",
            "rating": 4.8,
            "release_date": "2024-01-20",
            "developer": "Arcane Games",
            "image_url": "images/MysticLegends.png"
        },
        {
            "id": 3,
            "title": "Velocity Racer X",
            "price": 29.99,
            "category": "Racing",
            "tags": ["Fast-Paced", "Multiplayer", "Competitive"],
            "description": "Experience high-octane racing with gravity-defying tracks and insane speeds.",
            "rating": 4.3,
            "release_date": "2024-02-10",
            "developer": "SpeedForce Interactive",
            "image_url": "images/VelocityRacerX.png"
        },
        {
            "id": 4,
            "title": "Starbound Odyssey",
            "price": 49.99,
            "category": "Adventure",
            "tags": ["Space", "Exploration", "Sci-Fi"],
            "description": "Explore infinite galaxies, discover alien civilizations, and build your empire.",
            "rating": 4.7,
            "release_date": "2023-11-05",
            "developer": "Cosmic Studios",
            "image_url": "images/StarboundOdyssy.png"
        },
        {
            "id": 5,
            "title": "Shadow Assassin",
            "price": 44.99,
            "category": "Action",
            "tags": ["Stealth", "Ninja", "Dark"],
            "description": "Master the art of silent takedowns in this noir stealth-action masterpiece.",
            "rating": 4.6,
            "release_date": "2024-04-01",
            "developer": "ShadowBlade Games",
            "image_url": "./images/ShadowAssassin.png"
        },
        {
            "id": 6,
            "title": "Kingdom Builders",
            "price": 34.99,
            "category": "Strategy",
            "tags": ["Medieval", "City-Building", "Management"],
            "description": "Build your kingdom from scratch and lead your people to prosperity.",
            "rating": 4.4,
            "release_date": "2023-12-15",
            "developer": "Empire Interactive",
            "image_url": "images/KingdomBuilders.png"
        },
        {
            "id": 7,
            "title": "Pixel Dungeon Quest",
            "price": 14.99,
            "category": "Indie",
            "tags": ["Roguelike", "Pixel Art", "Dungeon Crawler"],
            "description": "A charming pixel-art roguelike with endless dungeons and procedural generation.",
            "rating": 4.2,
            "release_date": "2024-01-08",
            "developer": "RetroPixel Studios",
            "image_url": "images/PixelDungeonQuest.png"
        },
        {
            "id": 8,
            "title": "Eternal Warfare",
            "price": 0.00,
            "category": "Action",
            "tags": ["FPS", "Multiplayer", "Free-to-Play"],
            "description": "Join millions in this intense free-to-play tactical shooter.",
            "rating": 4.1,
            "release_date": "2023-10-20",
            "developer": "WarZone Studios",
            "image_url": "images/EternalWarfare.png"
        }
    ]
    
    return pd.DataFrame(games)


def get_game_by_id(games_df, game_id):
    """
    Get a specific game by ID
    
    Args:
        games_df: DataFrame containing games
        game_id: ID of the game to retrieve
        
    Returns:
        dict or None: Game dictionary if found, None otherwise
    """
    result = games_df[games_df['id'] == game_id]
    if not result.empty:
        return result.iloc[0].to_dict()
    return None


def filter_games(games_df, search="", category="All", price_range="All"):
    """
    Filter games based on search criteria
    
    Args:
        games_df: DataFrame containing games
        search: Search string for title
        category: Category filter
        price_range: Price range filter
        
    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    filtered_df = games_df.copy()
    
    # Apply search filter
    if search:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search, case=False)
        ]
    
    # Apply category filter
    if category != "All":
        filtered_df = filtered_df[filtered_df['category'] == category]
    
    # Apply price range filter
    if price_range == "Free":
        filtered_df = filtered_df[filtered_df['price'] == 0]
    elif price_range == "Under $20":
        filtered_df = filtered_df[filtered_df['price'] < 20]
    elif price_range == "$20-$40":
        filtered_df = filtered_df[
            (filtered_df['price'] >= 20) & (filtered_df['price'] <= 40)
        ]
    elif price_range == "$40+":
        filtered_df = filtered_df[filtered_df['price'] > 40]
    
    return filtered_df


def get_categories(games_df):
    """
    Get list of all categories
    
    Args:
        games_df: DataFrame containing games
        
    Returns:
        list: Sorted list of categories
    """
    return sorted(games_df['category'].unique().tolist())


def get_featured_games(games_df, n=3):
    """
    Get top-rated featured games
    
    Args:
        games_df: DataFrame containing games
        n: Number of games to return
        
    Returns:
        pd.DataFrame: Top-rated games
    """
    return games_df.nlargest(n, 'rating')


def get_free_games(games_df):
    """
    Get all free games
    
    Args:
        games_df: DataFrame containing games
        
    Returns:
        pd.DataFrame: Free games
    """
    return games_df[games_df['price'] == 0]