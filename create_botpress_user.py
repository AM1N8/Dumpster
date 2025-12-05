"""
Create Botpress User Script
Run this to create a new user and save credentials
"""

import argparse
from pathlib import Path
from utils.botpress_client import BotpressClient

secrets_path = Path(".streamlit") / "secrets.toml"

template = """
[[users]]
key = "{}"
"""


def create_user(name, id, chat_api_id, add_to_secrets=True):
    """Create a Botpress user and optionally save to secrets"""
    client = BotpressClient(api_id=chat_api_id)
    res = client.create_user(name, id)
    
    if not add_to_secrets:
        return res
    
    # Create .streamlit directory if it doesn't exist
    secrets_path.parent.mkdir(exist_ok=True)
    secrets_path.touch(exist_ok=True)
    
    # Append user to secrets file
    with open(secrets_path, "a") as f:
        f.write(template.format(res["key"]))
    
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a Botpress user and optionally store secrets."
    )
    parser.add_argument("--name", required=True, help="Display name of the user.")
    parser.add_argument("--id", required=True, help="Unique user ID.")
    parser.add_argument("--chat_api_id", required=True, help="Botpress Chat API ID.")
    parser.add_argument(
        "--no-secrets",
        action="store_true",
        help="Do not append to .streamlit/secrets.toml.",
    )
    
    args = parser.parse_args()
    
    print(f"Creating user: {args.name} (ID: {args.id})")
    result = create_user(
        name=args.name,
        id=args.id,
        chat_api_id=args.chat_api_id,
        add_to_secrets=not args.no_secrets
    )
    
    print("✅ User created successfully:")
    print(f"User ID: {result['user']['id']}")
    print(f"User Key: {result['key']}")
    
    if not args.no_secrets:
        print(f"\n✅ Credentials saved to {secrets_path}")