"""
GameVerse Helper Functions
Session state management and UI components
"""

import streamlit as st


def init_session_state():
    """Initialize session state variables"""
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'wishlist' not in st.session_state:
        st.session_state.wishlist = []
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'chatbot_messages' not in st.session_state:
        st.session_state.chatbot_messages = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []


def render_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>GAMEVERSE</h1>
        <p>Your Ultimate Digital Game Store - Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)


def render_navigation():
    """
    Render sidebar navigation and return selected page
    
    Returns:
        str: The key of the selected page
    """
    st.sidebar.title("Navigation")
    
    pages = {
        "Home": "home",
        "Browse Games": "browse",
        "My Cart": "cart",
        "Wishlist": "wishlist",
        "Profile": "profile",
        "Analytics": "analytics",
        "AI Chatbot": "chatbot"
    }
    
    selected_page = st.sidebar.radio("Go to:", list(pages.keys()))
    
    # Quick stats section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Cart Items", len(st.session_state.cart))
    st.sidebar.metric("Wishlist", len(st.session_state.wishlist))
    st.sidebar.metric("Chatbot Queries", st.session_state.chatbot_messages)
    
    return pages[selected_page]


def add_to_cart(game):
    """Add a game to the shopping cart"""
    # Check if game already in cart
    game_ids = [g['id'] for g in st.session_state.cart]
    if game['id'] not in game_ids:
        st.session_state.cart.append(game)
        return True
    return False


def add_to_wishlist(game):
    """Add a game to the wishlist"""
    # Check if game already in wishlist
    game_ids = [g['id'] for g in st.session_state.wishlist]
    if game['id'] not in game_ids:
        st.session_state.wishlist.append(game)
        return True
    return False


def remove_from_cart(index):
    """Remove a game from cart by index"""
    if 0 <= index < len(st.session_state.cart):
        st.session_state.cart.pop(index)
        return True
    return False


def remove_from_wishlist(index):
    """Remove a game from wishlist by index"""
    if 0 <= index < len(st.session_state.wishlist):
        st.session_state.wishlist.pop(index)
        return True
    return False


def calculate_cart_total():
    """Calculate total price of items in cart"""
    return sum(game['price'] for game in st.session_state.cart)


def format_price(price):
    """Format price for display"""
    return "FREE" if price == 0 else f"${price:.2f}"


def render_game_card(game, context="home"):
    """
    Render a styled game card
    
    Args:
        game: Game dictionary
        context: Context for unique button keys
    """
    st.markdown(f"""
    <div class="game-card">
        <div class="game-title">{game['title']}</div>
        <div class="game-price">{format_price(game['price'])}</div>
        <p style="color: #94a3b8;">{game['description'][:100]}...</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Add to Cart", key=f"cart_{context}_{game['id']}"):
            if add_to_cart(game):
                st.success("Added to cart!")
            else:
                st.info("Already in cart!")
    
    with col2:
        if st.button(f"Wishlist", key=f"wish_{context}_{game['id']}"):
            if add_to_wishlist(game):
                st.success("Added to wishlist!")
            else:
                st.info("Already in wishlist!")