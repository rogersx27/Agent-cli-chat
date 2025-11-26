import sys
import os

# Add src to sys.path so we can import chat_cli as a package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    try:
        from chat_cli.main import app
        app()
    except ImportError as e:
        print(f"Error importing application: {e}")
        sys.exit(1)
