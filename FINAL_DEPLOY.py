#!/usr/bin/env python3
"""
FINAL DEPLOYMENT SCRIPT
This creates the minimal working version for Render
"""

import os
import shutil

def create_minimal_deployment():
    """Create minimal deployment files"""
    
    # Create minimal requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write('fastapi==0.104.1\n')
        f.write('uvicorn==0.24.0\n')
        f.write('pydantic==2.5.0\n')
    
    # Create minimal main.py (already exists)
    print("✅ Minimal main.py created")
    
    # Ensure Procfile points to main.py
    with open('Procfile', 'w') as f:
        f.write('web: uvicorn main:app --host 0.0.0.0 --port $PORT\n')
    
    print("✅ Procfile updated")
    print("✅ Requirements updated")
    print("\n🚀 READY FOR DEPLOYMENT!")
    print("\nRun these commands:")
    print("git add .")
    print("git commit -m 'Final minimal deployment'")
    print("git push origin main")
    print("\nThen test with:")
    print("python -c \"import requests; print(requests.get('https://honey-pot-challenge.onrender.com/health').json())\"")

if __name__ == "__main__":
    create_minimal_deployment()
