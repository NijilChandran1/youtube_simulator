"""
Test script to verify Vertex AI connection to Gemini model.
Run this to check if your authentication and project setup is working correctly.
"""

from google import genai
from app.config import settings
import sys

def test_vertex_ai_connection():
    """Test connection to Vertex AI Gemini model"""
    
    print("=" * 60)
    print("Vertex AI Connection Test")
    print("=" * 60)
    
    # Display configuration
    print(f"\n📋 Configuration:")
    print(f"   Project ID: {settings.GOOGLE_CLOUD_PROJECT}")
    print(f"   Location: {settings.GOOGLE_CLOUD_LOCATION}")
    if settings.GOOGLE_APPLICATION_CREDENTIALS:
        print(f"   Service Account: {settings.GOOGLE_APPLICATION_CREDENTIALS}")
    else:
        print(f"   Auth Method: Application Default Credentials")
    
    try:
        # Initialize Vertex AI client
        print(f"\n🔌 Initializing Vertex AI client...")
        client = genai.Client(
            vertexai=True,
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.GOOGLE_CLOUD_LOCATION
        )
        print("   ✅ Client initialized successfully")
        
        # List available models
        print(f"\n📋 Listing available models...")
        try:
            models = client.models.list()
            print(f"\n   Available Models:")
            print(f"   " + "-" * 56)
            
            gemini_models = []
            for model in models:
                model_name = model.name
                # Extract just the model ID from the full resource name
                if '/' in model_name:
                    model_id = model_name.split('/')[-1]
                else:
                    model_id = model_name
                
                # Filter for Gemini models
                if 'gemini' in model_id.lower():
                    gemini_models.append(model_id)
                    print(f"   ✓ {model_id}")
            
            if not gemini_models:
                print(f"   ⚠️  No Gemini models found")
                print(f"   Note: This might be normal depending on your region")
            
            print(f"   " + "-" * 56)
            print(f"   Total Gemini models: {len(gemini_models)}")
            
        except Exception as list_error:
            print(f"   ⚠️  Could not list models: {list_error}")
            print(f"   Continuing with connection test...")
        
        # Test with a simple prompt
        print(f"\n🧪 Testing model 'gemini-2.0-flash' with simple prompt...")
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Say 'Hello from Vertex AI!' in exactly 5 words."
        )
        
        print(f"   ✅ Model responded successfully!")
        print(f"\n💬 Response:")
        print(f"   {response.text}")
        
        print(f"\n" + "=" * 60)
        print("✅ SUCCESS! Vertex AI connection is working correctly.")
        print("=" * 60)
        print("\nYou can now use the video analysis API!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Connection failed")
        print(f"\n🔍 Error details:")
        print(f"   Type: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        
        print(f"\n" + "=" * 60)
        print("💡 Troubleshooting Tips:")
        print("=" * 60)
        
        if "invalid_scope" in str(e).lower() or "oauth" in str(e).lower():
            print("\n1. Re-authenticate with correct scopes:")
            print("   gcloud auth application-default login \\")
            print("     --scopes=https://www.googleapis.com/auth/cloud-platform")
            print("\n   OR use a service account key:")
            print("   Set GOOGLE_APPLICATION_CREDENTIALS in .env file")
            
        elif "permission" in str(e).lower() or "forbidden" in str(e).lower():
            print("\n1. Check IAM permissions:")
            print("   Your account/service account needs 'Vertex AI User' role")
            print("   gcloud projects add-iam-policy-binding \\")
            print(f"     {settings.GOOGLE_CLOUD_PROJECT} \\")
            print("     --member='serviceAccount:YOUR_SA@project.iam.gserviceaccount.com' \\")
            print("     --role='roles/aiplatform.user'")
            
        elif "not enabled" in str(e).lower() or "api" in str(e).lower():
            print("\n1. Enable Vertex AI API:")
            print("   gcloud services enable aiplatform.googleapis.com")
            
        elif "not found" in str(e).lower() and "model" in str(e).lower():
            print("\n1. The model 'gemini-2.0-flash' might not be available in your region")
            print("   Try a different model like 'gemini-1.5-flash' or 'gemini-1.5-pro'")
            print("   Update the model_id in gemini_analyzer.py and vertex_ai_service.py")
            
        else:
            print("\n1. Verify your project ID is correct in .env file")
            print("2. Ensure you're authenticated:")
            if settings.GOOGLE_APPLICATION_CREDENTIALS:
                print(f"   Check service account key file exists:")
                print(f"   {settings.GOOGLE_APPLICATION_CREDENTIALS}")
            else:
                print("   gcloud auth application-default login")
            print("3. Check if Vertex AI API is enabled:")
            print("   gcloud services list --enabled | findstr aiplatform")
        
        print("\n" + "=" * 60)
        
        return False

if __name__ == "__main__":
    try:
        success = test_vertex_ai_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
