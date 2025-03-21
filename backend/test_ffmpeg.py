import subprocess
import os

print("Checking PATH in Python...")
print(os.environ["PATH"])

print("\nTrying to run ffmpeg...")
try:
    result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    print("ffmpeg found! Output:")
    print(result.stdout)
except FileNotFoundError as e:
    print(f"ffmpeg not found: {e}")