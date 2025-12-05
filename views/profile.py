"""
GameVerse User Profile Page
User authentication and profile management
"""

import streamlit as st


def render(games_df):
    """Render the user profile page"""
    st.markdown("## User Profile")
    
    if st.session_state.user is None:
        render_login_form()
    else:
        render_user_dashboard()


def render_login_form():
    """Render login/registration form"""
    st.info("Demo Mode - Login functionality for demonstration purposes")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", value="DemoUser123", key="login_username")
        
        with col2:
            email = st.text_input("Email", value="demo@gameverse.com", key="login_email")
        
        password = st.text_input("Password", type="password", value="demo123", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            st.session_state.user = {
                "username": username,
                "email": email,
                "joined_date": "2024-01-15",
                "games_owned": 12,
                "total_spent": 347.85
            }
            st.success(f"Welcome back, {username}!")
            st.rerun()
    
    with tab2:
        st.markdown("### Create New Account")
        
        new_username = st.text_input("Username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", type="primary", use_container_width=True):
            if new_password == confirm_password:
                st.session_state.user = {
                    "username": new_username,
                    "email": new_email,
                    "joined_date": "2024-12-04",
                    "games_owned": 0,
                    "total_spent": 0.0
                }
                st.success(f"Welcome to GameVerse, {new_username}!")
                st.rerun()
            else:
                st.error("Passwords do not match!")


def render_user_dashboard():
    """Render logged-in user dashboard"""
    user = st.session_state.user
    
    st.success(f"Logged in as: **{user['username']}**")
    
    # User stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{user.get('games_owned', 0)}</div>
            <div class="stat-label">Games Owned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">${user.get('total_spent', 0):.2f}</div>
            <div class="stat-label">Total Spent</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(st.session_state.wishlist)}</div>
            <div class="stat-label">Wishlist Items</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Profile information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Account Information")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Member Since:** {user.get('joined_date', 'N/A')}")
    
    with col2:
        st.markdown("### Quick Actions")
        if st.button("View Purchase History"):
            st.info("Purchase history feature coming soon!")
        
        if st.button("Edit Profile"):
            st.info("Profile editing feature coming soon!")
        
        if st.button("Logout", type="secondary"):
            st.session_state.user = None
            st.rerun()