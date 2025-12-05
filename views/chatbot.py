"""
GameVerse AI Chatbot - ROBUST STATE VERSION
Uses a dictionary-based history cache to prevent message loss during reruns.
"""

import streamlit as st
from utils.botpress_client import BotpressClient 


def render(games_df):
    """Render the chatbot page with dictionary-based state management."""
    st.markdown("## AI Game Assistant")
    st.markdown("Ask me anything about games, get recommendations, or browse our catalog!")
    
    # 1. Initialize Client
    client = get_or_create_client()
    if client is None:
        st.error("⚠️ Chatbot not configured. Please set up your Botpress credentials.")
        return
    
    # 2. Authenticate User
    try:
        user = client.get_user()
        if "error" in user:
            st.error(f"Failed to authenticate: {user['error']}")
            return
        user_id = user["user"]["id"]
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return
    
    # 3. Initialize Global State (Conversations & History Cache)
    initialize_global_state(client)
    
    # 4. Render Selector (Updates active_conversation)
    render_conversation_selector(client)
    
    st.markdown("---")
    
    # 5. Get Current Conversation ID
    conversation_id = st.session_state.active_conversation
    
    # 6. Ensure History is Loaded for THIS Conversation
    # We checks if this specific ID exists in our cache. If not, we fetch from API.
    # If it DOES exist (even if empty list), we rely on the cache.
    if conversation_id not in st.session_state.conversation_history:
        with st.spinner("Loading history..."):
            messages = fetch_messages_from_api(client, conversation_id, user_id)
            st.session_state.conversation_history[conversation_id] = messages
            
    # 7. Display Messages from Cache
    current_messages = st.session_state.conversation_history[conversation_id]
    
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 8. Handle Input
    handle_chat_input(client, conversation_id)


@st.cache_resource
def get_or_create_client():
    """Create and cache Botpress client."""
    try:
        api_id = st.secrets.get("CHAT_API_ID")
        user_key = st.secrets.get("users", [{}])[0].get("key") 
        
        if not api_id or not user_key:
            return None
        
        return BotpressClient(api_id=api_id, user_key=user_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {str(e)}")
        return None


def initialize_global_state(client):
    """Initialize the global dictionary for history and load conversation list."""
    
    # THE CORE FIX: A dictionary mapping conversation_id -> list of messages
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = {}
        
    if "conversations_loaded" not in st.session_state:
        st.session_state.conversations_loaded = False
    
    # Load conversation list once
    if not st.session_state.conversations_loaded:
        conversations_data = client.list_conversations()
        conversations = conversations_data.get("conversations", [])
        
        # Create first conversation if none exist
        if not conversations:
            res = client.create_conversation()
            if "conversation" in res:
                conversations = [res["conversation"]]
        
        st.session_state.conversations = conversations
        st.session_state.conversations_loaded = True
        
        # Set initial active conversation
        if conversations and "active_conversation" not in st.session_state:
            st.session_state.active_conversation = conversations[0]["id"]


def render_conversation_selector(client):
    """Render selector. Does NOT clear history, just changes ID."""
    conversations = st.session_state.get("conversations", [])
    
    if not conversations:
        return
    
    conversation_ids = [conv["id"] for conv in conversations]
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        current_id = st.session_state.get("active_conversation")
        
        # Robust index finding
        try:
            current_index = conversation_ids.index(current_id)
        except (ValueError, IndexError):
            current_index = 0
        
        selected_id = st.selectbox(
            "Select Conversation",
            options=conversation_ids,
            index=current_index,
            format_func=lambda x: f"Conversation {conversation_ids.index(x) + 1}",
            key="conversation_selector"
        )
        
        # If selection changes, just update the ID and rerun to trigger logic in step 6
        if selected_id != current_id:
            st.session_state.active_conversation = selected_id
            st.rerun()
    
    with col2:
        st.markdown("<div style='height: 1.9em'></div>", unsafe_allow_html=True)
        if st.button("➕ New"):
            create_new_conversation(client)


def create_new_conversation(client):
    """Create new conversation and update state."""
    res = client.create_conversation()
    if "conversation" in res:
        new_conv = res["conversation"]
        cid = new_conv["id"]
        
        # Update conversation list
        st.session_state.conversations.append(new_conv)
        
        # Initialize empty history for this new ID immediately
        st.session_state.conversation_history[cid] = []
        
        # Switch to it
        st.session_state.active_conversation = cid
        st.rerun()


def fetch_messages_from_api(client, conversation_id, user_id):
    """Helper to fetch and format messages from API."""
    try:
        messages_data = client.list_messages(conversation_id, limit=50)
        messages = messages_data.get("messages", [])
        
        chat_messages = []
        for message in reversed(messages):
            role = "user" if message.get("userId") == user_id else "assistant"
            text = message.get("payload", {}).get("text", "")
            if text:
                chat_messages.append({"role": role, "content": text})
        
        return chat_messages
    except Exception as e:
        st.error(f"Error loading history: {e}")
        return []


def handle_chat_input(client, conversation_id):
    """Handle input, update DICTIONARY state, and rerun."""
    if prompt := st.chat_input("Ask me about games..."):
        
        # 1. Update LOCAL cache immediately (User message)
        user_msg = {"role": "user", "content": prompt}
        st.session_state.conversation_history[conversation_id].append(user_msg)
        
        # Render immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 2. Send to Botpress
        try:
            client.create_message(prompt, conversation_id=conversation_id)
        except Exception as e:
            st.error(f"Failed to send: {e}")
            return
        
        # 3. Stream Response
        with st.chat_message("assistant"):
            try:
                stream = client.listen_conversation(conversation_id=conversation_id)
                response = st.write_stream(stream)
                
                if response:
                    # 4. Update LOCAL cache immediately (Assistant message)
                    bot_msg = {"role": "assistant", "content": response}
                    st.session_state.conversation_history[conversation_id].append(bot_msg)
                    
                    # Track usage stats
                    if "chatbot_messages" not in st.session_state:
                        st.session_state.chatbot_messages = 0
                    st.session_state.chatbot_messages += 1
                    
                    # 5. Rerun to ensure consistency
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Streaming error: {e}")