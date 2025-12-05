"""
Debug script to test Botpress connection
Run this to diagnose authentication issues
"""

import requests
import json
from pathlib import Path

def load_secrets():
    """Load secrets from secrets.toml"""
    secrets_path = Path(".streamlit") / "secrets.toml"
    
    if not secrets_path.exists():
        print("❌ Error: .streamlit/secrets.toml not found!")
        print(f"   Expected location: {secrets_path.absolute()}")
        return None, None
    
    print(f"✅ Found secrets file at: {secrets_path.absolute()}")
    
    # Parse TOML manually (simple parsing)
    chat_api_id = None
    user_keys = []
    
    with open(secrets_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('CHAT_API_ID'):
                chat_api_id = line.split('=')[1].strip().strip('"').strip("'")
            elif line.startswith('key'):
                user_key = line.split('=')[1].strip().strip('"').strip("'")
                user_keys.append(user_key)
    
    return chat_api_id, user_keys


def test_connection(chat_api_id, user_key):
    """Test connection to Botpress API"""
    base_url = f"https://chat.botpress.cloud/{chat_api_id}"
    
    print(f"\n🔗 Testing connection to: {base_url}")
    print(f"🔑 Using user key: {user_key[:10]}..." if user_key else "❌ No user key provided")
    
    if not chat_api_id:
        print("\n❌ CHAT_API_ID is missing!")
        return False
    
    if not user_key:
        print("\n❌ User key is missing!")
        return False
    
    # Test endpoint
    url = f"{base_url}/users/me"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-user-key": user_key,
    }
    
    print(f"\n📡 Making request to: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! Authentication working!")
            print(f"   User ID: {data.get('user', {}).get('id')}")
            print(f"   User Name: {data.get('user', {}).get('name')}")
            return True
        
        elif response.status_code == 401:
            print("\n❌ Authentication Failed (401 Unauthorized)")
            print("   Possible issues:")
            print("   1. User key is invalid or expired")
            print("   2. User doesn't exist in Botpress")
            print("   3. Chat API ID is incorrect")
            
        elif response.status_code == 404:
            print("\n❌ Not Found (404)")
            print("   Possible issues:")
            print("   1. Chat API ID is incorrect")
            print("   2. Chat API integration not installed in Botpress")
            print("   3. Bot not published")
            
        else:
            print(f"\n❌ Unexpected error: {response.status_code}")
            
        print(f"\n📄 Response body: {response.text}")
        return False
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error!")
        print("   Check your internet connection")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False


def main():
    print("=" * 60)
    print("🔍 BOTPRESS CONNECTION DEBUG TOOL")
    print("=" * 60)
    
    # Load secrets
    chat_api_id, user_keys = load_secrets()
    
    if not chat_api_id:
        print("\n❌ Critical Error: CHAT_API_ID not found in secrets.toml")
        print("\n📝 Your secrets.toml should look like:")
        print('   CHAT_API_ID = "your_api_id_here"')
        print('   [[users]]')
        print('   key = "your_user_key_here"')
        return
    
    print(f"\n✅ CHAT_API_ID found: {chat_api_id}")
    
    if not user_keys:
        print("\n❌ Critical Error: No user keys found in secrets.toml")
        print("\n💡 You need to create a user first!")
        print("   Run: python create_botpress_user.py --name YourName --id user_001 --chat_api_id " + chat_api_id)
        return
    
    print(f"\n✅ Found {len(user_keys)} user key(s)")
    
    # Test connection with first user key
    print("\n" + "=" * 60)
    print("Testing connection with first user...")
    print("=" * 60)
    
    success = test_connection(chat_api_id, user_keys[0])
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour Botpress integration is configured correctly.")
        print("You can now run your Streamlit app.")
    else:
        print("\n" + "=" * 60)
        print("❌ TESTS FAILED")
        print("=" * 60)
        print("\n📋 Next Steps:")
        print("1. Check the error messages above")
        print("2. Verify your CHAT_API_ID in Botpress Studio")
        print("3. Make sure your bot is published")
        print("4. Try creating a new user with the create_botpress_user.py script")


if __name__ == "__main__":
    main()