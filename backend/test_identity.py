import google.auth
from google.auth.transport.requests import Request

def check_identity():
    try:
        # Use explicit scopes here. Without this, the 'refresh' often fails 
        # because the server doesn't know which 'door' you're trying to open.
        scopes = ['https://www.googleapis.com/auth/cloud-platform']
        
        credentials, project = google.auth.default(scopes=scopes)
        
        # This is where the 'handshake' happens
        credentials.refresh(Request())
        
        print("-" * 30)
        print(f"CONNECTED AS: {getattr(credentials, 'service_account_email', 'User Account')}")
        print(f"PROJECT: {project}")
        print(f"SCOPES VERIFIED: {credentials.scopes}")
        print("-" * 30)
        print("SUCCESS: Your environment is now correctly authenticated.")

    except Exception as e:
        print(f"\nDETAILED ERROR: {e}")
        print("\nPossible reason: Your JSON key is found, but the 'Cloud Resource Manager API' ")
        print("might need to be enabled, or the Service Account lacks the 'Token Creator' role.")

if __name__ == "__main__":
    check_identity()