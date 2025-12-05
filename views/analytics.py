"""
GameVerse Analytics Dashboard
Platform statistics and performance metrics
"""

import streamlit as st
import pandas as pd
import numpy as np


def render(games_df):
    """Render the analytics dashboard"""
    st.markdown("## Analytics Dashboard")
    
    # Top-level metrics
    render_key_metrics()
    
    st.markdown("---")
    
    # Performance charts
    render_performance_charts()
    
    st.markdown("---")
    
    # Game statistics
    render_game_statistics(games_df)


def render_key_metrics():
    """Render key performance metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">1,247</div>
            <div class="stat-label">Total Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.chatbot_messages}</div>
            <div class="stat-label">Chatbot Queries</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">8.4k</div>
            <div class="stat-label">Games Sold</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">$142k</div>
            <div class="stat-label">Revenue</div>
        </div>
        """, unsafe_allow_html=True)


def render_performance_charts():
    """Render performance charts"""
    st.markdown("### Performance Metrics")
    
    # Generate sample data
    dates = pd.date_range('2024-01-01', periods=30)
    chart_data = pd.DataFrame({
        'Date': dates,
        'Queries': np.random.randint(20, 100, 30),
        'Sales': np.random.randint(10, 50, 30),
        'Revenue': np.random.randint(500, 2000, 30)
    })
    
    tab1, tab2, tab3 = st.tabs(["Chatbot Activity", "Sales", "Revenue"])
    
    with tab1:
        st.markdown("#### Chatbot Queries Over Time")
        st.line_chart(chart_data.set_index('Date')['Queries'])
    
    with tab2:
        st.markdown("#### Daily Sales")
        st.area_chart(chart_data.set_index('Date')['Sales'])
    
    with tab3:
        st.markdown("#### Revenue Trend")
        st.bar_chart(chart_data.set_index('Date')['Revenue'])


def render_game_statistics(games_df):
    """Render game catalog statistics"""
    st.markdown("### Game Catalog Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Games by Category")
        category_counts = games_df['category'].value_counts()
        st.bar_chart(category_counts)
    
    with col2:
        st.markdown("#### Price Distribution")
        price_ranges = pd.cut(
            games_df['price'],
            bins=[0, 0.01, 20, 40, 100],
            labels=['Free', 'Under $20', '$20-$40', '$40+']
        )
        price_dist = price_ranges.value_counts()
        st.bar_chart(price_dist)
    
    # Top rated games
    st.markdown("---")
    st.markdown("### Top Rated Games")
    
    top_games = games_df.nlargest(5, 'rating')[['title', 'rating', 'category', 'price']]
    st.dataframe(
        top_games,
        use_container_width=True,
        hide_index=True
    )