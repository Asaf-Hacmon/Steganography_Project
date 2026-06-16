"""
LSB Steganography Embedder
Usage: python embed.py <cover_image> <payload_file> <output_image>

Encodes payload bytes into the least significant bit of each RGB channel.
Layout: [32-bit big-endian payload length][payload bytes]
"""

import sys
import struct
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PIL import Image


def embed(image_path: str, payload_path: str, output_path: str) -> None:
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())
    capacity_bits = len(pixels) * 3  # 1 bit per channel

    with open(payload_path, "rb") as f:
        payload = f.read()

    # 4-byte header stores payload length
    data = struct.pack(">I", len(payload)) + payload
    total_bits = len(data) * 8

    if total_bits > capacity_bits:
        raise ValueError(
            f"Payload too large: need {total_bits} bits, image holds {capacity_bits} bits"
        )

    # Flatten payload bytes into a bit stream
    bits = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)

    # Write bits into LSB of each channel
    new_pixels = []
    bit_idx = 0
    for r, g, b in pixels:
        if bit_idx < len(bits):
            r = (r & 0xFE) | bits[bit_idx]
            bit_idx += 1
        if bit_idx < len(bits):
            g = (g & 0xFE) | bits[bit_idx]
            bit_idx += 1
        if bit_idx < len(bits):
            b = (b & 0xFE) | bits[bit_idx]
            bit_idx += 1
        new_pixels.append((r, g, b))

    out = Image.new("RGB", img.size)
    out.putdata(new_pixels)
    out.save(output_path, "PNG")

    print(f"[+] Payload size : {len(payload)} bytes")
    print(f"[+] Image capacity: {capacity_bits // 8} bytes")
    print(f"[+] Stego image saved to: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python embed.py <cover_image> <payload_file> <output_image>")
        sys.exit(1)
    embed(sys.argv[1], sys.argv[2], sys.argv[3])
