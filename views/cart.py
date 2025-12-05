"""
GameVerse Shopping Cart Page
Manage cart items and checkout
"""

import streamlit as st
from utils.helpers import calculate_cart_total, format_price


def render(games_df):
    """Render the shopping cart page"""
    st.markdown("## Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Browse games to add items!")
        
        if st.button("Browse Games"):
            st.session_state.current_page = "browse"
            st.rerun()
        return
    
    # Display cart items
    for idx, game in enumerate(st.session_state.cart):
        render_cart_item(game, idx)
    
    # Cart summary
    st.markdown("---")
    render_cart_summary()


def render_cart_item(game, idx):
    """Render a single cart item"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"**{game['title']}**")
        st.caption(f"{game['category']} | {game['developer']}")
    
    with col2:
        price = game['price']
        st.markdown(f"**{format_price(price)}**")
    
    with col3:
        if st.button("Remove", key=f"remove_{idx}"):
            st.session_state.cart.pop(idx)
            st.rerun()
    
    st.markdown("---")


def render_cart_summary():
    """Render cart summary and checkout"""
    total = calculate_cart_total()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### Total: {format_price(total)}")
        st.caption(f"{len(st.session_state.cart)} item(s) in cart")
    
    with col2:
        if st.button("Proceed to Checkout", type="primary", use_container_width=True):
            handle_checkout()


def handle_checkout():
    """Handle checkout process"""
    total = calculate_cart_total()
    
    st.balloons()
    st.success(f"Order placed successfully! Total: {format_price(total)}")
    
    # Show order summary
    with st.expander("Order Summary", expanded=True):
        st.markdown("**Items Purchased:**")
        for game in st.session_state.cart:
            st.markdown(f"- {game['title']} - {format_price(game['price'])}")
        st.markdown(f"\n**Total: {format_price(total)}**")
        st.info("This is a demo. No actual payment was processed.")
    
    # Clear cart
    st.session_state.cart = []