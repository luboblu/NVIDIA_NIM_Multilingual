import os
import base64
import requests
from io import BytesIO
from PIL import Image
import gradio as gr

# NVIDIA Nim API key (provided by user) and endpoint
# You can also set NVIDIA_NIM_API_KEY in your environment to override\
nAPI_KEY = (
    os.getenv("NVIDIA_NIM_API_KEY")
    or "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"
)
API_URL = (
    os.getenv("NVIDIA_NIM_API_URL")
    or "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"
)


# Function to call the NVIDIA Nim text-to-image API
def generate_image(prompt: str) -> Image.Image:
    try:
        headers = {
            "Authorization": f"Bearer {nAPI_KEY}",
            "Accept": "application/json",
        }
        payload = {
            "prompt": prompt,
            "mode": "base",
            "cfg_scale": 3.5,
            "width": 1024,
            "height": 1024,
            "seed": 0,
            "steps": 50,
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        # HTTP status check
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            err_json = None
            try:
                err_json = response.json()
            except ValueError:
                pass
            detail = err_json.get("detail") if err_json else response.text
            raise ValueError(f"API Error {response.status_code}: {detail}")

        data = response.json()
        artifacts = data.get("artifacts")
        if not artifacts:
            raise ValueError(f"No artifacts in response: {data}")
        artifact = artifacts[0]
        b64_image = (
            artifact.get("binary") or artifact.get("base64") or artifact.get("data")
        )
        if not b64_image:
            raise ValueError(f"No image data in artifact: {artifact}")

        img_data = base64.b64decode(b64_image)
        return Image.open(BytesIO(img_data))

    except Exception as e:
        raise gr.Error(f"Image generation failed: {e}")


# Build the Gradio interface
def main():
    iface = gr.Interface(
        fn=generate_image,
        inputs=gr.Textbox(lines=2, placeholder="Enter a prompt..."),
        outputs=gr.Image(type="pil"),
        title="NVIDIA Nim Text-to-Image",
        description="Enter a text prompt to generate an image via NVIDIA Nim API",
    )
    iface.launch(share=True)


if __name__ == "__main__":
    main()
