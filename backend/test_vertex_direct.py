"""
Alternative test using Vertex AI SDK directly (not google-genai package)
This helps diagnose if the issue is with the google-genai package
"""

import vertexai
from vertexai.generative_models import GenerativeModel
from app.config import settings

def test_vertex_ai_direct():
    print("=" * 60)
    print("Vertex AI Direct SDK Test")
    print("=" * 60)
    
    print(f"\n📋 Configuration:")
    print(f"   Project: {settings.GOOGLE_CLOUD_PROJECT}")
    print(f"   Location: {settings.GOOGLE_CLOUD_LOCATION}")
    print(f"   Credentials: {settings.GOOGLE_APPLICATION_CREDENTIALS}")
    
    try:
        # Initialize Vertex AI
        print(f"\n🔌 Initializing Vertex AI...")
        vertexai.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION
        )
        print("   ✅ Vertex AI initialized")
        
        # Create model instance
        print(f"\n🤖 Loading model 'gemini-2.0-flash-exp'...")
        model = GenerativeModel("gemini-2.0-flash-exp")
        print("   ✅ Model loaded")
        
        # Test generation
        print(f"\n🧪 Testing generation...")
        response = model.generate_content("Say hello in 5 words")
        print(f"   ✅ Generation successful!")
        print(f"\n💬 Response: {response.text}")
        
        print(f"\n" + "=" * 60)
        print("✅ SUCCESS! Vertex AI SDK works correctly.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        
        if "404" in str(e):
            print(f"\n💡 Model 'gemini-2.0-flash-exp' not found in {settings.GOOGLE_CLOUD_LOCATION}")
            print(f"   Try: gemini-1.5-flash or gemini-1.5-pro")
        
        return False

if __name__ == "__main__":
    test_vertex_ai_direct()
