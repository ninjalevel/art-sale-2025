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
    SquareModuleDrawer
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

url = "https://ninjalevel.github.io/art-sale-2025/"

# Create output directory
os.makedirs("modern-qr", exist_ok=True)

print("Generating MODERN QR codes...")
print("=" * 60)

# 1. Sleek Circles with Gradient
print("\n1. Circular dots with radial gradient...")
qr1 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr1.add_data(url)
qr1.make()
img1 = qr1.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=RadialGradiantColorMask(
        back_color=(255, 255, 255),
        center_color=(88, 86, 214),  # Purple
        edge_color=(33, 150, 243)    # Blue
    )
)
img1.save("modern-qr/1-circular-gradient.png")

# 2. Rounded modules with vertical gradient
print("2. Rounded squares with vertical gradient...")
qr2 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr2.add_data(url)
qr2.make()
img2 = qr2.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=VerticalGradiantColorMask(
        back_color=(255, 255, 255),
        top_color=(26, 26, 26),
        bottom_color=(100, 100, 100)
    )
)
img2.save("modern-qr/2-rounded-gradient.png")

# 3. Gapped squares - ultra minimal
print("3. Gapped squares - minimal design...")
qr3 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr3.add_data(url)
qr3.make()
img3 = qr3.make_image(
    image_factory=StyledPilImage,
    module_drawer=GappedSquareModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(255, 255, 255),
        front_color=(26, 26, 26)
    )
)
img3.save("modern-qr/3-gapped-minimal.png")

# 4. Circles with horizontal gradient - sleek
print("4. Circles with horizontal gradient...")
qr4 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr4.add_data(url)
qr4.make()
img4 = qr4.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=HorizontalGradiantColorMask(
        back_color=(250, 250, 250),
        left_color=(41, 128, 185),   # Blue
        right_color=(142, 68, 173)   # Purple
    )
)
img4.save("modern-qr/4-horizontal-gradient.png")

# 5. Rounded with square gradient - modern art style
print("5. Rounded modules with square gradient...")
qr5 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr5.add_data(url)
qr5.make()
img5 = qr5.make_image(
    image_factory=StyledPilImage,
    module_drawer=RoundedModuleDrawer(),
    color_mask=SquareGradiantColorMask(
        back_color=(255, 255, 255),
        center_color=(231, 76, 60),   # Red
        edge_color=(44, 62, 80)       # Dark blue
    )
)
img5.save("modern-qr/5-square-gradient.png")

# 6. Super minimal - monochrome circles
print("6. Monochrome circular - ultra clean...")
qr6 = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr6.add_data(url)
qr6.make()
img6 = qr6.make_image(
    image_factory=StyledPilImage,
    module_drawer=CircleModuleDrawer(),
    color_mask=SolidFillColorMask(
        back_color=(255, 255, 255),
        front_color=(0, 0, 0)
    )
)
img6.save("modern-qr/6-monochrome-circles.png")

print("\n" + "=" * 60)
print("MODERN QR CODES GENERATED in 'modern-qr/' folder:")
print("  1. circular-gradient.png      - Circular dots, radial gradient")
print("  2. rounded-gradient.png       - Rounded squares, vertical fade")
print("  3. gapped-minimal.png         - Minimal gapped squares")
print("  4. horizontal-gradient.png    - Circles, horizontal gradient")
print("  5. square-gradient.png        - Rounded, artistic center gradient")
print("  6. monochrome-circles.png     - Ultra clean B&W circles")
print("=" * 60)
print(f"\nAll link to: {url}")
print("\nThese use modern design trends: custom shapes, gradients, and")
print("minimal aesthetics while maintaining perfect scannability!")
