"""
Botpress Chat API Client - OPTIMIZED VERSION
High-performance streaming with connection pooling and caching
"""

import os
import json
import requests
import sseclient
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Constants
BASE_URI = "https://chat.botpress.cloud"
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

# Connection pool settings
DEFAULT_TIMEOUT = 30  # seconds
STREAM_TIMEOUT = 120  # longer timeout for SSE streams


class BotpressClient:
    def __init__(self, api_id=None, user_key=None):
        self.api_id = api_id or os.getenv("CHAT_API_ID")
        self.user_key = user_key or os.getenv("USER_KEY")
        self.base_url = f"{BASE_URI}/{self.api_id}"
        self.headers = {
            **HEADERS,
            "x-user-key": self.user_key,
        }
        
        # Initialize session with connection pooling and retry strategy
        self.session = self._create_session()
        
        # Cache for reducing redundant API calls
        self._conversation_cache = {}
        self._user_cache = None

    def _create_session(self):
        """Create requests session with connection pooling and retry logic"""
        session = requests.Session()
        
        # Retry strategy for failed requests
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
        )
        
        # Mount adapter with connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    def _request(self, method, path, json_data=None, timeout=DEFAULT_TIMEOUT):
        """Make HTTP request with proper error handling and timeouts"""
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(
                method, 
                url, 
                headers=self.headers, 
                json=json_data,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            return {"error": "Request timed out"}
        except requests.HTTPError as e:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    # --- Core API Methods ---

    def get_user(self):
        """Get current user information with caching"""
        if self._user_cache is None:
            self._user_cache = self._request("GET", "/users/me")
        return self._user_cache

    def create_user(self, name, id):
        """Create a new user"""
        user_data = {"name": name, "id": id}
        result = self._request("POST", "/users", json_data=user_data)
        self._user_cache = None  # Invalidate cache
        return result

    def set_user_key(self, key):
        """Set user key for authentication"""
        self.user_key = key
        self.headers["x-user-key"] = key
        self._user_cache = None  # Invalidate cache

    def create_and_set_user(self, name, id):
        """Create user and set their key"""
        new_user = self.create_user(name, id)
        if "key" in new_user:
            self.set_user_key(new_user["key"])
        return new_user

    def create_conversation(self):
        """Create a new conversation"""
        result = self._request("POST", "/conversations", json_data={"body": {}})
        if "conversation" in result and "id" in result["conversation"]:
            # Clear cache for this conversation
            conv_id = result["conversation"]["id"]
            self._conversation_cache[conv_id] = {"messages": []}
        return result

    def list_conversations(self):
        """List all conversations for current user"""
        return self._request("GET", "/conversations")

    def get_conversation(self, conversation_id):
        """Get specific conversation details with caching"""
        if conversation_id not in self._conversation_cache:
            self._conversation_cache[conversation_id] = self._request(
                "GET", f"/conversations/{conversation_id}"
            )
        return self._conversation_cache[conversation_id]

    def create_message(self, message, conversation_id):
        """Send a message in a conversation"""
        payload = {
            "payload": {"type": "text", "text": message},
            "conversationId": conversation_id,
        }
        result = self._request("POST", "/messages", json_data=payload)
        
        # Invalidate message cache for this conversation
        if conversation_id in self._conversation_cache:
            self._conversation_cache[conversation_id].pop("messages", None)
        
        return result

    def list_messages(self, conversation_id, limit=50):
        """
        List messages in a conversation with pagination
        
        Args:
            conversation_id: The conversation ID
            limit: Maximum number of messages to retrieve (default 50)
        """
        # Check cache first
        cache_key = f"{conversation_id}_messages"
        if cache_key in self._conversation_cache:
            return self._conversation_cache[cache_key]
        
        # Fetch messages with limit
        result = self._request(
            "GET", 
            f"/conversations/{conversation_id}/messages?limit={limit}"
        )
        
        # Cache the result
        self._conversation_cache[cache_key] = result
        return result

    def listen_conversation(self, conversation_id):
        """
        OPTIMIZED: Listen to conversation events using Server-Sent Events
        
        Key improvements:
        1. Reuses session connection pool
        2. Proper timeout handling
        3. Yields only text content (not full message objects)
        4. Better error handling for malformed events
        """
        url = f"{self.base_url}/conversations/{conversation_id}/listen"
        
        try:
            # Use session for connection pooling
            response = self.session.get(
                url, 
                headers=self.headers, 
                stream=True,
                timeout=STREAM_TIMEOUT
            )
            response.raise_for_status()
            
            # Create SSE client
            client = sseclient.SSEClient(response)
            
            for event in client.events():
                # Skip ping events
                if event.data == "ping":
                    continue
                
                try:
                    # Parse event data
                    event_data = json.loads(event.data)
                    
                    # Extract text payload
                    if "data" in event_data:
                        data = event_data["data"]
                        if "payload" in data and "text" in data["payload"]:
                            # Yield only the text content for efficiency
                            yield data["payload"]["text"]
                
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    # Skip malformed events silently
                    continue
                    
        except requests.Timeout:
            yield "[Error: Connection timed out]"
        except requests.RequestException as e:
            yield f"[Error: {str(e)}]"
        except Exception as e:
            yield f"[Error: Unexpected error - {str(e)}]"

    def close(self):
        """Close the session and cleanup resources"""
        if hasattr(self, 'session'):
            self.session.close()
        self._conversation_cache.clear()
        self._user_cache = None

    def __enter__(self):
        """Context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on context exit"""
        self.close()
        return False