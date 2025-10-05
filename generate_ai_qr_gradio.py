# /// script
# requires-python = ">=3.11"
# dependencies = [ "gradio_client" ]
# ///

from gradio_client import Client
from pathlib import Path
import time

url = "https://ninjalevel.github.io/art-sale-2025/"

# Creative prompts for art gallery QR codes
prompts = [
    "abstract watercolor painting, fluid artistic colors",
    "minimalist modern art, clean geometric design",
    "impressionist landscape, soft painterly style",
    "contemporary digital art, vibrant colors",
    "oil painting texture, classical fine art",
    "japanese ink wash, zen minimalist aesthetic",
    "pop art bold colors, graphic design",
    "art nouveau flowing elegant patterns",
    "abstract expressionism, dynamic brushstrokes",
    "cubist geometric artistic forms",
    "surrealist dreamlike artwork",
    "art deco geometric elegance",
    "watercolor botanical flowers",
    "modern 3d sculpture aesthetic",
    "stained glass colorful patterns",
    "japanese woodblock print style",
    "mosaic colorful tiles art",
    "charcoal sketch fine art",
    "pastel abstract soft colors",
    "renaissance classical painting",
]

# Create output directory
output_dir = Path("ai-qr-codes")
output_dir.mkdir(exist_ok=True)

print("Generating AI Artistic QR Codes via Gradio...")
print("=" * 70)

# Connect to HuggingFace Space
client = Client("huggingface-projects/QR-code-AI-art-generator")

generated = 0
for i, prompt in enumerate(prompts, 1):
    try:
        print(f"{i}. Generating: {prompt[:55]}...")

        result = client.predict(
            qr_code_content=url,
            prompt=f"{prompt}, artistic QR code, high quality",
            negative_prompt="ugly, blurry, low quality, disfigured",
            guidance_scale=10,
            controlnet_conditioning_scale=2,
            strength=0.9,
            seed=i*1000,  # Different seed for variety
            init_image=None,
            qrcode_image=None,
            use_qr_code_as_init_image=True,
            sampler="DPM++ Karras SDE",
            api_name="/inference"
        )

        # Result is a file path
        if result and Path(result).exists():
            output_path = output_dir / f"ai-qr-{i:02d}-{prompt.split(',')[0].replace(' ', '-')[:25]}.png"
            # Copy instead of rename to handle cross-drive moves
            import shutil
            shutil.copy2(result, output_path)
            print(f"   [OK] Saved: {output_path.name}")
            generated += 1
        else:
            print(f"   [FAIL] No result returned")

        # Be nice to the API
        time.sleep(3)

    except Exception as e:
        print(f"   [ERROR] {str(e)[:70]}")
        continue

print("\n" + "=" * 70)
print(f"Generated {generated} AI artistic QR codes!")
print(f"Location: {output_dir}/")
print(f"All QR codes link to: {url}")
print("=" * 70)
print("\nIMPORTANT: Test these QR codes with your phone before using!")
print("AI-generated codes may have reduced scannability.")
