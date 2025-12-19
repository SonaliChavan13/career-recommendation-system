import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Add your API keys here
API_KEYS = {
    'ADZUNA_APP_ID': '5dac6c1e',
    'ADZUNA_APP_KEY': 'c1a3bb7b4137b225a064f37819d0c1ca',
    'YOUTUBE_API_KEY': 'AIzaSyCxvofQ_py17s9pZ4-vzi7YH8geKrn24eU',
}

# Create .env file
env_content = """
# External API Keys
ADZUNA_APP_ID={ADZUNA_APP_ID}
ADZUNA_APP_KEY={ADZUNA_APP_KEY}
YOUTUBE_API_KEY={YOUTUBE_API_KEY}

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
""".format(**API_KEYS)

with open('.env', 'w') as f:
    f.write(env_content)

print("✅ .env file created with API keys")
print("📋 Available APIs:")
print("  1. Adzuna - Job market data")
print("  2. YouTube - Educational content")
print("  3. Coursera - Course catalog (no API key needed)")
print("\n🔑 Get your API keys from:")
print("  - Adzuna: https://developer.adzuna.com/")
print("  - YouTube: https://console.cloud.google.com/apis/credentials")