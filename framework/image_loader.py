# framework/image_loader.py

import base64
import os
from typing import List
from pathlib import Path
from PIL import Image  # From Pillow library


class ImageLoader:
    """
    Loads images from disk and converts them to base64 for the Ollama API.

    Why base64? The Ollama API is a REST API. REST APIs send data as JSON.
    JSON is text. Images are binary. Base64 converts binary to text.
    The server decodes it back to an image.
    """

    def __init__(self, image_dir: str = "test_images"):
        """
        images_dir: folder where your test images live
        """
        self.image_dir = Path(image_dir).resolve()
        # Validate directory exists
        if not self.image_dir.exists():
            raise FileNotFoundError(f"images directory not found: {self.image_dir.absolute()}")



    def list_all(self) -> List[str]:
        #Lists all images in the directory
        valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
        files = []
        for filename in os.listdir(self.image_dir):
            _, ext = os.path.splitext(filename)
            if ext.lower() in valid_extensions:
                files.append(filename)
        return sorted(files)


    def exists(self, filename) -> bool:
        full_path = os.path.join(self.image_dir, filename)
        return os.path.isfile(full_path)


    def compress_image(self, filename) -> str:
        # Open the image to process it
        full_path = os.path.join(self.image_dir, filename)
        img = Image.open(full_path)

        # inspect image channels like RGBA and LA

        if img.mode in ("LA", "RGBA") or (img.mode == 'P' and 'transparency' in img.info):
            # Create a solid white canvas layer matching identical dimensions
            background = Image.new("RGB", img.size, (255, 255, 255))

            # If the image uses an indexed palette (P), upgrade it to RGBA to read its alpha transparency mask
            if img.mode == 'P':
                img = img.convert('RGBA')

            # Paste the asset onto the white backdrop, using the image itself as its own transparency mask
            background.paste(img, (0, 0), img)
            img = background
        else:
            # If it's already an opaque format, guarantee standard 3-channel RGB mode for JPEG safety
            img = img.convert("RGB")

        # Split the path cleanly using the Path object attributes

        name, ext = os.path.splitext(filename)

        # Create the full absolute destination path string
        output_image = str(self.image_dir / f"compressed_{name}{ext}")

        # Save with compression using the correct dynamic output_image variable
        if ext.upper() == "PNG":
            img.save(output_image, "PNG", optimize=True)
        else:
            img.save(output_image, optimize=True, quality=20,  format="JPEG")
        print()
        return output_image

    def load(self, filename: str) -> str:
        """
        Load image file, return as base64-encoded string.

        Args:
            filename: e.g., "cat.jpg" or "dog.png"

        Returns:
            base64 string ready for Ollama API
        """

        # Check exists before trying to open
        if not self.exists(filename):
            raise FileNotFoundError(
                f"Image not found: {os.path.join(self.image_dir, filename)}\n"
                f"Available images: {self.list_all()}"
            )

        full_path = os.path.join(self.image_dir, filename)

        # Open image with Pillow first (validates it's a real image)
        try:
            with Image.open(full_path) as img:
                img.verify()  # Verifies file is not corrupted
        except Exception as e:
            raise ValueError(f"Invalid image file {filename}: {e}")

        # 1. Compress image and get the correct temporary string path
        # Fixed: Added 'self.' prefix to call the class method
        compressed_file_path = self.compress_image(filename)

        # 2. Read raw bytes from the newly created compressed file
        with open(compressed_file_path, "rb") as f:
            raw_bytes = f.read()

        # 3. Clean up disk immediately after reading bytes so you don't clutter your folder
        if os.path.exists(compressed_file_path):
            os.remove(compressed_file_path)

        # Convert bytes to Python base64 string
        base64_string = base64.b64encode(raw_bytes).decode("utf-8")

        return base64_string

"""
# Usage
loader = ImageLoader(".../image-testing-framework/test_images/")
print("Available:", loader.list_all())

cat_b64 = loader.load("cat.jpg")
print(f"Loaded image: {len(cat_b64)} characters (base64)")
"""