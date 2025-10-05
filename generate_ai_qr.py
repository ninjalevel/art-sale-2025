# /// script
# requires-python = ">=3.11"
# dependencies = [ "requests", "pillow" ]
# ///

import requests
import time
import os
from pathlib import Path

# Hugging Face Inference API (FREE!)
API_URL = "https://api-inference.huggingface.co/models/monster-labs/control_v1p_sd15_qrcode_monster"
HF_TOKEN = os.getenv("HF_TOKEN", "")  # Optional: set HF_TOKEN env var for higher rate limits

url = "https://ninjalevel.github.io/art-sale-2025/"

# Creative prompts for art gallery QR codes
prompts = [
    "abstract watercolor painting, fluid colors, artistic, gallery art, high quality",
    "minimalist modern art, clean lines, geometric shapes, contemporary gallery",
    "impressionist landscape, painterly, soft colors, museum quality",
    "contemporary digital art, vibrant colors, modern gallery aesthetic",
    "oil painting texture, classical art style, rich colors, fine art gallery",
    "japanese ink wash painting, minimalist, zen aesthetic, art gallery",
    "pop art style, bold colors, graphic design, modern art museum",
    "art nouveau design, flowing lines, elegant patterns, gallery poster",
    "abstract expressionism, bold brushstrokes, dynamic colors, contemporary art",
    "cubist painting, geometric forms, artistic composition, modern gallery",
    "surrealist artwork, dreamlike, artistic, gallery exhibition quality",
    "art deco design, geometric elegance, sophisticated, gallery aesthetic",
    "watercolor flowers, delicate, artistic, botanical art gallery style",
    "modern sculpture aesthetic, 3d forms, contemporary art museum",
    "stained glass art, colorful, artistic patterns, gallery installation",
    "woodblock print style, japanese art, traditional gallery aesthetic",
    "mosaic art, colorful tiles, artistic pattern, gallery installation",
    "charcoal sketch aesthetic, artistic, fine art drawing, gallery quality",
    "pastel colors abstract, soft artistic, contemporary gallery style",
    "renaissance painting style, classical art, museum masterpiece quality",
]

# Create output directory
output_dir = Path("ai-qr-codes")
output_dir.mkdir(exist_ok=True)

print("Generating AI Artistic QR Codes using Hugging Face (FREE API)...")
print("=" * 70)
print(f"Using model: monster-labs/control_v1p_sd15_qrcode_monster")
print("=" * 70)

headers = {}
if HF_TOKEN:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    print("\nUsing HF token for higher rate limits...")
else:
    print("\nNo HF_TOKEN set - using free tier with rate limits")
    print("To get higher limits: export HF_TOKEN='your_token_here'")
    print("Get token at: https://huggingface.co/settings/tokens")

print("\n")

generated = 0
for i, prompt in enumerate(prompts, 1):
    try:
        print(f"{i}. Generating: {prompt[:60]}...")

        payload = {
            "inputs": f"{prompt}, QR code, scannable",
            "parameters": {
                "qr_code_content": url,
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "controlnet_conditioning_scale": 1.5
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            image_path = output_dir / f"qr-{i:02d}-{prompt.split(',')[0].replace(' ', '-')[:30]}.png"
            with open(image_path, "wb") as f:
                f.write(response.content)
            print(f"   [OK] Saved: {image_path.name}")
            generated += 1
        elif response.status_code == 503:
            print(f"   [WAIT] Model loading, waiting 20s...")
            time.sleep(20)
            # Retry once
            response = requests.post(API_URL, headers=headers, json=payload)
            if response.status_code == 200:
                image_path = output_dir / f"qr-{i:02d}-{prompt.split(',')[0].replace(' ', '-')[:30]}.png"
                with open(image_path, "wb") as f:
                    f.write(response.content)
                print(f"   [OK] Saved: {image_path.name}")
                generated += 1
            else:
                print(f"   [FAIL] Failed: {response.status_code}")
        elif response.status_code == 429:
            print(f"   [RATE] Rate limited! Waiting 60s...")
            time.sleep(60)
        else:
            print(f"   [ERROR] Error: {response.status_code} - {response.text[:100]}")

        # Be nice to the free API
        time.sleep(2)

    except Exception as e:
        print(f"   [ERROR] Exception: {e}")
        continue

print("\n" + "=" * 70)
print(f"Generated {generated} AI artistic QR codes!")
print(f"Location: {output_dir}/")
print(f"All QR codes link to: {url}")
print("=" * 70)
print("\nNote: Test these QR codes before using - AI generation may affect")
print("scannability. Pick the ones that scan reliably!")
