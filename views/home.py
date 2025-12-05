"""
GameVerse Home Page
Featured games and special offers
"""

import streamlit as st
from utils.helpers import render_game_card, format_price
from data.games_data import get_featured_games, get_free_games


def render(games_df):
    """Render the home page"""
    st.markdown("## Featured Games")
    
    # Get featured games
    featured = get_featured_games(games_df, n=3)
    
    # Display featured games in columns
    cols = st.columns(3)
    for idx, (_, game) in enumerate(featured.iterrows()):
        with cols[idx]:
            render_game_card(game.to_dict(), context="home")
    
    # Special offers section
    st.markdown("---")
    st.markdown("## Special Offers")
    
    free_games = get_free_games(games_df)
    if not free_games.empty:
        cols = st.columns(len(free_games))
        for idx, (_, game) in enumerate(free_games.iterrows()):
            with cols[idx]:
                st.info(f"**{game['title']}** - FREE!")
                if st.button(f"Get Now", key=f"free_{game['id']}"):
                    from utils.helpers import add_to_cart
                    if add_to_cart(game.to_dict()):
                        st.success("Added to cart!")
                    else:
                        st.info("Already in cart!")
    
    # Welcome message and quick actions
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3 style="color: #c7d2fe; margin-bottom: 1rem;">Welcome to GameVerse</h3>
            <p style="color: #94a3b8;">
                Discover thousands of games, from indie gems to AAA blockbusters.
                Get personalized recommendations from our AI assistant.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h3 style="color: #c7d2fe; margin-bottom: 1rem;">Quick Actions</h3>
            <p style="color: #94a3b8;">
                Browse our catalog, chat with our AI assistant for recommendations,
                or check out today's deals and discounts.
            </p>
        </div>
        """, unsafe_allow_html=True)