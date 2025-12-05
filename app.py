"""
GameVerse - Digital Game Store
Main Application Entry Point
"""

import streamlit as st
from pathlib import Path

# Import utilities
from utils.styling import load_custom_css
from utils.helpers import init_session_state, render_header, render_navigation
from data.games_data import load_games

# --- CHANGED: Import from 'views' instead of 'pages' ---
# Make sure you have renamed the physical folder 'pages' to 'views'
from views import home, browse, cart, wishlist, profile, analytics, chatbot

# Base directory
BASE_DIR = Path(__file__).parent

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="GameVerse - Your Digital Game Store",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page routing dictionary
PAGES = {
    "home": home.render,
    "browse": browse.render,
    "cart": cart.render,
    "wishlist": wishlist.render,
    "profile": profile.render,
    "analytics": analytics.render,
    "chatbot": chatbot.render
}


def main():
    """Main application flow"""
    # Load custom styling
    load_custom_css()
    
    # Initialize session state
    init_session_state()
    
    # Load game data
    games_df = load_games()
    
    # Render header
    render_header()
    
    # Render navigation and get selected page
    current_page = render_navigation()
    
    # Route to appropriate page
    page_render_func = PAGES.get(current_page)
    if page_render_func:
        page_render_func(games_df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 2rem;'>
        <p>GameVerse - Powered by Streamlit & AI</p>
        <p>© 2025 GameVerse. All rights reserved. | 
        <a href='#' style='color: #6366f1;'>Privacy Policy</a> | 
        <a href='#' style='color: #6366f1;'>Terms of Service</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()