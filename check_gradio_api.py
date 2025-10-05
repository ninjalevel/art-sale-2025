# /// script
# requires-python = ">=3.11"
# dependencies = [ "gradio_client" ]
# ///

from gradio_client import Client

client = Client("huggingface-projects/QR-code-AI-art-generator")
print(client.view_api())
