# /// script
# requires-python = ">=3.11"
# dependencies = [ "qrcode[pil]" ]
# ///

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import (
    CircleModuleDrawer,
    RoundedModuleDrawer,
    GappedSquareModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    SquareGradiantColorMask,
    RadialGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask
)
from PIL import Image
import os
import glob
import random

url = "https://ninjalevel.github.io/art-sale-2025/"

# Create output directory
os.makedirs("qr-variations", exist_ok=True)

# Get all painting images
paintings = glob.glob("images/*/*.jpg")
random.shuffle(paintings)

print("Generating 40 CREATIVE QR code variations...")
print("=" * 70)

# Color palettes - modern, artistic, vibrant
palettes = [
    # Vibrant gradients
    {"name": "Purple-Blue", "c1": (88, 86, 214), "c2": (33, 150, 243)},
    {"name": "Sunset", "c1": (255, 94, 77), "c2": (255, 175, 64)},
    {"name": "Ocean", "c1": (0, 119, 182), "c2": (0, 180, 216)},
    {"name": "Forest", "c1": (39, 174, 96), "c2": (22, 160, 133)},
    {"name": "Pink-Purple", "c1": (253, 29, 29), "c2": (131, 58, 180)},
    {"name": "Gold-Orange", "c1": (242, 153, 74), "c2": (242, 201, 76)},
    {"name": "Teal-Green", "c1": (26, 188, 156), "c2": (142, 68, 173)},
    {"name": "Red-Pink", "c1": (235, 77, 75), "c2": (255, 118, 117)},
    {"name": "Deep-Purple", "c1": (106, 27, 154), "c2": (74, 35, 90)},
    {"name": "Sky-Blue", "c1": (52, 152, 219), "c2": (155, 89, 182)},
    # Monochrome variations
    {"name": "Black", "c1": (0, 0, 0), "c2": (50, 50, 50)},
    {"name": "Dark-Gray", "c1": (44, 62, 80), "c2": (52, 73, 94)},
    {"name": "Navy", "c1": (25, 42, 86), "c2": (41, 128, 185)},
    {"name": "Charcoal", "c1": (23, 32, 42), "c2": (69, 90, 100)},
]

# Module drawers
drawers = [
    ("Circle", CircleModuleDrawer()),
    ("Rounded", RoundedModuleDrawer()),
    ("Gapped", GappedSquareModuleDrawer()),
    ("Square", SquareModuleDrawer()),
    ("VBars", VerticalBarsDrawer()),
    ("HBars", HorizontalBarsDrawer()),
]

# Gradient types
gradients = [
    ("Radial", RadialGradiantColorMask),
    ("Vertical", VerticalGradiantColorMask),
    ("Horizontal", HorizontalGradiantColorMask),
    ("Square", SquareGradiantColorMask),
]

count = 1

# Generate 25 gradient variations
print("\nGenerating gradient QR codes (1-25)...")
for i in range(25):
    drawer_name, drawer = random.choice(drawers)
    grad_name, GradClass = random.choice(gradients)
    palette = random.choice(palettes)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(url)
    qr.make()

    # Create gradient based on type
    if grad_name == "Radial":
        mask = GradClass(
            back_color=(255, 255, 255),
            center_color=palette["c1"],
            edge_color=palette["c2"]
        )
    elif grad_name == "Square":
        mask = GradClass(
            back_color=(255, 255, 255),
            center_color=palette["c1"],
            edge_color=palette["c2"]
        )
    elif grad_name == "Vertical":
        mask = GradClass(
            back_color=(255, 255, 255),
            top_color=palette["c1"],
            bottom_color=palette["c2"]
        )
    else:  # Horizontal
        mask = GradClass(
            back_color=(255, 255, 255),
            left_color=palette["c1"],
            right_color=palette["c2"]
        )

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=drawer,
        color_mask=mask
    )

    filename = f"{count:02d}-{drawer_name}-{grad_name}-{palette['name']}.png"
    img.save(f"qr-variations/{filename}")
    print(f"  {count}. {drawer_name} + {grad_name} + {palette['name']}")
    count += 1

# Generate 15 with embedded images
print(f"\nGenerating QR codes with embedded images (26-40)...")
for i in range(15):
    if i < len(paintings):
        painting = paintings[i]
        drawer_name, drawer = random.choice(drawers)
        palette = random.choice(palettes)

        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(url)
        qr.make()

        # Random gradient type
        grad_name, GradClass = random.choice(gradients)

        if grad_name == "Radial":
            mask = GradClass(
                back_color=(255, 255, 255),
                center_color=palette["c1"],
                edge_color=palette["c2"]
            )
        elif grad_name == "Square":
            mask = GradClass(
                back_color=(255, 255, 255),
                center_color=palette["c1"],
                edge_color=palette["c2"]
            )
        elif grad_name == "Vertical":
            mask = GradClass(
                back_color=(255, 255, 255),
                top_color=palette["c1"],
                bottom_color=palette["c2"]
            )
        else:
            mask = GradClass(
                back_color=(255, 255, 255),
                left_color=palette["c1"],
                right_color=palette["c2"]
            )

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=drawer,
            color_mask=mask,
            embeded_image_path=painting
        )

        painting_name = os.path.basename(painting).replace('.jpg', '')
        filename = f"{count:02d}-{drawer_name}-Embedded-{painting_name[:10]}.png"
        img.save(f"qr-variations/{filename}")
        print(f"  {count}. {drawer_name} + Embedded '{os.path.basename(painting)}'")
        count += 1

print("\n" + "=" * 70)
print(f"SUCCESS! Generated {count-1} unique QR code variations!")
print(f"Location: modern-qr/")
print(f"All QR codes link to: {url}")
print("\nBrowse through them and pick your favorites!")
print("=" * 70)
