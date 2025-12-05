"""
GameVerse Wishlist Page
Manage wishlisted games
"""

import streamlit as st
from utils.helpers import add_to_cart, format_price


def render(games_df):
    """Render the wishlist page"""
    st.markdown("## My Wishlist")
    
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty. Add games you're interested in!")
        
        if st.button("Browse Games"):
            st.session_state.current_page = "browse"
            st.rerun()
        return
    
    # Display wishlist items
    for idx, game in enumerate(st.session_state.wishlist):
        render_wishlist_item(game, idx)


def render_wishlist_item(game, idx):
    """Render a single wishlist item"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"### {game['title']}")
        st.caption(f"{game['category']} | {format_price(game['price'])}")
        st.markdown(f"*{game['description'][:150]}...*")
        
        # Action buttons
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"Add to Cart", key=f"cart_wish_{idx}_{game['id']}"):
                if add_to_cart(game):
                    st.success("Added to cart!")
                else:
                    st.info("Already in cart!")
        
        with col_b:
            if st.button(f"Remove", key=f"remove_wish_{idx}_{game['id']}"):
                st.session_state.wishlist.pop(idx)
                st.rerun()
    
    with col2:
        try:
            st.image(game['image_url'], use_container_width=True)
        except:
            st.markdown("""
            <div style="background: rgba(99, 102, 241, 0.2); 
                        padding: 2rem; 
                        border-radius: 8px; 
                        text-align: center;
                        color: #94a3b8;">
                No Image
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")