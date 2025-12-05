"""
Check and display current secrets configuration
"""

from pathlib import Path

secrets_path = Path(".streamlit") / "secrets.toml"

print("Current secrets.toml content:")
print("=" * 60)

if secrets_path.exists():
    with open(secrets_path, 'r') as f:
        content = f.read()
        print(content)
else:
    print("❌ File not found!")

print("=" * 60)