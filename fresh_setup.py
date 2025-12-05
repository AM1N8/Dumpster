"""
Fresh Botpress User Setup
This will create a new user and properly configure secrets
"""

import requests
import json
from pathlib import Path

# Configuration
CHAT_API_ID = "67b799ef-8272-426c-9882-baf7e368845c"
USER_NAME = "GameVerseUser"
USER_ID = "gameverse_user_001"  # Unique ID

print("=" * 60)
print("🚀 FRESH BOTPRESS USER SETUP")
print("=" * 60)

# Step 1: Create user via API
url = f"https://chat.botpress.cloud/{CHAT_API_ID}/users"
headers = {
    "Content-Type": "application/json",
    "accept": "application/json"
}
data = {
    "name": USER_NAME,
    "id": USER_ID
}

print(f"\n📡 Creating user at: {url}")
print(f"   User Name: {USER_NAME}")
print(f"   User ID: {USER_ID}")

try:
    response = requests.post(url, headers=headers, json=data)
    
    print(f"\n📊 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        user_key = result['key']
        
        print("\n✅ User created successfully!")
        print(f"   User ID: {result['user']['id']}")
        print(f"   User Name: {result['user']['name']}")
        print(f"   User Key: {user_key[:20]}...")
        
        # Step 2: Create secrets file
        secrets_path = Path(".streamlit") / "secrets.toml"
        secrets_path.parent.mkdir(exist_ok=True)
        
        # Create fresh secrets file (overwrite old one)
        secrets_content = f'''CHAT_API_ID = "{CHAT_API_ID}"

[[users]]
key = "{user_key}"
'''
        
        with open(secrets_path, 'w') as f:
            f.write(secrets_content)
        
        print(f"\n✅ Secrets saved to: {secrets_path.absolute()}")
        
        # Step 3: Verify the setup
        print("\n" + "=" * 60)
        print("🔍 VERIFYING SETUP")
        print("=" * 60)
        
        verify_url = f"https://chat.botpress.cloud/{CHAT_API_ID}/users/me"
        verify_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-user-key": user_key,
        }
        
        verify_response = requests.get(verify_url, headers=verify_headers)
        
        if verify_response.status_code == 200:
            verify_data = verify_response.json()
            print("\n✅ VERIFICATION SUCCESSFUL!")
            print(f"   Authenticated as: {verify_data['user']['name']}")
            print(f"   User ID: {verify_data['user']['id']}")
            
            print("\n" + "=" * 60)
            print("🎉 SETUP COMPLETE!")
            print("=" * 60)
            print("\nYou can now run your Streamlit app:")
            print("   streamlit run app.py")
            
        else:
            print(f"\n❌ Verification failed: {verify_response.status_code}")
            print(f"   Response: {verify_response.text}")
            
    elif response.status_code == 409:
        print("\n⚠️  User already exists!")
        print("   This user ID is already registered.")
        print("\n💡 Solutions:")
        print("   1. Use a different user ID")
        print("   2. Or retrieve the existing user's key from Botpress Studio")
        
    else:
        print(f"\n❌ Failed to create user: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 404:
            print("\n💡 Possible issues:")
            print("   1. Check your CHAT_API_ID is correct")
            print("   2. Make sure Chat integration is installed in Botpress")
            print("   3. Verify your bot is published")

except requests.exceptions.ConnectionError:
    print("\n❌ Connection Error!")
    print("   Check your internet connection")
    
except Exception as e:
    print(f"\n❌ Unexpected error: {str(e)}")

print("\n" + "=" * 60)