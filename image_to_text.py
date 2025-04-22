import os
import base64
import requests
from io import BytesIO
import gradio as gr
from PIL import Image
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env
# NVIDIA Integrate API key and endpoint
API_KEY = os.getenv("NV_IMAGE2TEXT_API_KEY")
API_URL = os.getenv("NV_IMAGE2TEXT_API_URL")
MAX_B64_SIZE = 180_000  # 最大 base64 字元長度


# Helper: encode image to base64 (JPEG) with adjustable quality
def encode_img(image: Image.Image, quality: int = 85) -> str:
    buf = BytesIO()
    image.save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


# Function to call the NVIDIA image-to-text API
def image_to_text(image: Image.Image) -> str:
    # Ensure RGB
    image = image.convert("RGB")
    # First attempt: JPEG at default quality
    img_b64 = encode_img(image)

    # If too large, try downscaling dimensions and reducing quality
    quality = 85
    while len(img_b64) >= MAX_B64_SIZE and quality >= 20:
        # Reduce quality
        quality -= 15
        img_b64 = encode_img(image, quality)

    if len(img_b64) >= MAX_B64_SIZE:
        # Attempt resizing by half
        new_size = (image.width // 2, image.height // 2)
        image = image.resize(new_size, Image.ANTIALIAS)
        img_b64 = encode_img(image, quality)

    if len(img_b64) >= MAX_B64_SIZE:
        raise gr.Error("影像經過壓縮後仍超出大小限制，請使用更小的影像。")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "google/gemma-3-27b-it",
        "messages": [
            {"role": "system", "content": "請用 繁體中文 回答以下問題。"},
            {
                "role": "user",
                "content": f'請描述此圖片：<img src="data:image/jpeg;base64,{img_b64}" />',
            },
        ],
        "max_tokens": 512,
        "temperature": 0.20,
        "top_p": 0.70,
        "stream": False,
    }

    # Send request
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        detail = response.text
        try:
            detail = response.json().get("detail", detail)
        except ValueError:
            pass
        raise gr.Error(f"API Error {response.status_code}: {detail}")

    data = response.json()
    # Extract assistant reply
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        raise gr.Error(f"Unexpected response format: {data}")


# Build Gradio interface
iface = gr.Interface(
    fn=image_to_text,
    inputs=gr.Image(type="pil", label="上傳影像 (Upload an image)"),
    outputs=gr.Textbox(label="影像描述 (Description)"),
    title="NVIDIA Image-to-Text (繁體中文輸出)",
    description="上傳一張圖片，以 NVIDIA Integrate API 生成繁體中文描述。",
)

if __name__ == "__main__":
    iface.launch(share=True)
