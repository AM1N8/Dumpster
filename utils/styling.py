"""
GameVerse Styling Module
Custom CSS for dark cyberpunk aesthetic
"""

import streamlit as st


def load_custom_css():
    """Load custom CSS for the application with enhanced dark theme"""
    st.markdown("""
    <style>
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
        text-align: center;
        animation: fadeIn 0.8s ease-in;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: #e0e7ff;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }
    
    /* Game card styling */
    .game-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.4);
        border-color: rgba(99, 102, 241, 0.6);
    }
    
    .game-title {
        color: #e0e7ff;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .game-price {
        color: #10b981;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .game-tag {
        background: rgba(99, 102, 241, 0.2);
        color: #c7d2fe;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.9rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 23, 42, 0.8);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Stats card */
    .stat-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #c7d2fe;
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Featured game banner */
    .featured-banner {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
        border: 2px solid rgba(99, 102, 241, 0.5);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    /* Input fields enhancement */
    .stTextInput>div>div>input {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: rgba(99, 102, 241, 0.6);
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }
    
    /* Selectbox enhancement */
    .stSelectbox>div>div>select {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: white;
        border-radius: 8px;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background: rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(139, 92, 246, 0.15);
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .stat-number {
            font-size: 2rem;
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.8);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #8b5cf6 0%, #6366f1 100%);
    }
    </style>
    """, unsafe_allow_html=True)