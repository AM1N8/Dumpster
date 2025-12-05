"""
GameVerse Browse Page
Browse and filter games catalog
"""

import streamlit as st
from utils.helpers import add_to_cart, add_to_wishlist, format_price
from data.games_data import filter_games, get_categories


def render(games_df):
    """Render the browse page with filters"""
    st.markdown("## Browse All Games")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search = st.text_input("Search games", "", placeholder="Enter game title...")
    
    with col2:
        categories = ["All"] + get_categories(games_df)
        selected_category = st.selectbox("Category", categories)
    
    with col3:
        price_range = st.selectbox(
            "Price Range",
            ["All", "Free", "Under $20", "$20-$40", "$40+"]
        )
    
    # Apply filters
    filtered_df = filter_games(
        games_df,
        search=search,
        category=selected_category,
        price_range=price_range
    )
    
    # Display result count
    st.markdown(f"**Found {len(filtered_df)} games**")
    st.markdown("---")
    
    # Display filtered games
    if filtered_df.empty:
        st.info("No games found matching your criteria. Try adjusting the filters.")
    else:
        for _, game in filtered_df.iterrows():
            render_game_detail(game.to_dict())
            st.markdown("---")


def render_game_detail(game):
    """Render detailed game information"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        try:
            st.image(game['image_url'], use_container_width=True)
        except:
            st.markdown("""
            <div style="background: rgba(99, 102, 241, 0.2); 
                        padding: 3rem; 
                        border-radius: 8px; 
                        text-align: center;
                        color: #94a3b8;">
                No Image
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Title and price
        st.markdown(f"### {game['title']}")
        price_text = format_price(game['price'])
        st.markdown(f"**Price:** {price_text}")
        
        # Rating and category
        stars = "⭐" * int(game['rating'])
        st.markdown(f"**Category:** {game['category']} | **Rating:** {stars} ({game['rating']})")
        
        # Developer and release date
        st.markdown(f"**Developer:** {game['developer']} | **Release:** {game['release_date']}")
        
        # Description
        st.markdown(f"{game['description']}")
        
        # Tags
        tags_html = " ".join([
            f"<span class='game-tag'>{tag}</span>" 
            for tag in game['tags']
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("")  # Spacing
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("Add to Cart", key=f"cart_browse_{game['id']}"):
                if add_to_cart(game):
                    st.success("Added to cart!")
                else:
                    st.info("Already in cart!")
        
        with col_b:
            if st.button("Wishlist", key=f"wish_browse_{game['id']}"):
                if add_to_wishlist(game):
                    st.success("Wishlisted!")
                else:
                    st.info("Already in wishlist!")
        
        with col_c:
            if st.button("Details", key=f"details_{game['id']}"):
                with st.expander("Game Details", expanded=True):
                    st.markdown(f"""
                    **Full Description:** {game['description']}
                    
                    **Game Information:**
                    - Category: {game['category']}
                    - Developer: {game['developer']}
                    - Release Date: {game['release_date']}
                    - Rating: {game['rating']}/5.0
                    
                    **Tags:** {', '.join(game['tags'])}
                    """)