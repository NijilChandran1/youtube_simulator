import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    import numpy
    print(f"✅ NumPy imported successfully: {numpy.__version__}")
except ImportError as e:
    print(f"❌ NumPy import failed: {e}")

try:
    import cv2
    print(f"✅ OpenCV imported successfully: {cv2.__version__}")
except ImportError as e:
    print(f"❌ OpenCV import failed: {e}")

try:
    from google import genai
    print("✅ Google GenAI imported successfully")
except ImportError as e:
    print(f"❌ Google GenAI import failed: {e}")
