import typer
from chat_cli.network.server import run_server
from chat_cli.network.client import run_client

app = typer.Typer()

@app.command()
def start_server():
    """Starts the chat server."""
    run_server()

@app.command()
def connect(username: str):
    """Connects to the chat server."""
    run_client(username)

if __name__ == "__main__":
    app()
