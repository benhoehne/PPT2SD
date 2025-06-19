#!/usr/bin/env python3
"""
Test script to convert PPTX files to Google Slides
and export as PDF using a service account
"""

import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from pptx import Presentation
import io
from dotenv import load_dotenv
import time

# Scopes required for the service account
SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive.file'
]

class PPTXToGoogleSlidesConverter:
    """Convert PPTX to Google Slides and export as PDF using service account"""
    
    def __init__(self, pptx_path: Path):
        self.pptx_path = pptx_path
        self.presentation = Presentation(pptx_path)
        self.output_dir = Path("test_files/output")
        self.output_dir.mkdir(exist_ok=True)
        load_dotenv()  # Load environment variables from .env file
        
    def get_service_account_credentials(self):
        """Get credentials from service account key file"""
        try:
            # Get the path to the service account key file from environment variable
            key_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY')
            if not key_path:
                raise ValueError("GOOGLE_SERVICE_ACCOUNT_KEY environment variable not set")
                
            credentials = service_account.Credentials.from_service_account_file(
                key_path,
                scopes=SCOPES
            )
            return credentials
            
        except Exception as e:
            print(f"Error getting service account credentials: {str(e)}")
            print("\nTo set up service account:")
            print("1. Go to Google Cloud Console")
            print("2. Create a new project or select existing one")
            print("3. Enable Google Slides API and Google Drive API")
            print("4. Create a service account and download the JSON key file")
            print("5. Add the key file path to your .env file as GOOGLE_SERVICE_ACCOUNT_KEY=/path/to/key.json")
            return None

    def export_presentation(self, drive_service, file_id):
        """Export the presentation as PDF"""
        print("\n=== Exporting presentation as PDF ===")
        
        try:
            # Export the presentation as PDF
            request = drive_service.files().export_media(
                fileId=file_id,
                mimeType='application/pdf'
            )
            
            # Get the PDF content
            pdf_content = request.execute()
            
            # Stream the file content directly to disk
            output_path = self.output_dir / f"{self.pptx_path.stem}.pdf"
            
            with open(output_path, 'wb') as f:
                f.write(pdf_content)
            
            print(f"  ✓ Successfully exported PDF to {output_path}")
            return output_path
            
        except Exception as e:
            print(f"  ✗ Error exporting PDF: {str(e)}")
            return None

    def convert_to_google_slides(self):
        """Convert PPTX to Google Slides and export as PDF"""
        print("\n=== Converting PPTX to Google Slides ===")
        
        try:
            # Get service account credentials
            creds = self.get_service_account_credentials()
            if not creds:
                return
                
            # Build the services
            slides_service = build('slides', 'v1', credentials=creds)
            drive_service = build('drive', 'v3', credentials=creds)
            
            # Create a new presentation
            presentation_metadata = {
                'name': self.pptx_path.stem + ' (Converted)',
                'mimeType': 'application/vnd.google-apps.presentation'
            }
            
            # Upload the PPTX file to Google Drive first
            print("  Uploading PPTX to Google Drive...")
            
            media = MediaIoBaseUpload(
                io.FileIO(str(self.pptx_path), 'rb'),
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                resumable=True
            )
            
            file = drive_service.files().create(
                body=presentation_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            presentation_id = file.get('id')
            
            if presentation_id:
                print(f"  ✓ Successfully created Google Slides presentation")
                print(f"  View at: https://docs.google.com/presentation/d/{presentation_id}")
                
                # Export the presentation as PDF
                pdf_path = self.export_presentation(drive_service, presentation_id)
                
                # Clean up the Google Slides presentation
                drive_service.files().delete(fileId=presentation_id).execute()
                print("  ✓ Cleaned up Google Slides presentation")
                
                if pdf_path:
                    print(f"\nDone! Your presentation has been converted to PDF: {pdf_path}")
            else:
                print("  ✗ Failed to create Google Slides presentation")
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")

def main():
    """Main function"""
    # Test file path
    test_file = Path("test_files/BI_PV_LU01.pptx")
    
    if not test_file.exists():
        print(f"Error: Test file not found: {test_file}")
        return
        
    converter = PPTXToGoogleSlidesConverter(test_file)
    converter.convert_to_google_slides()

if __name__ == "__main__":
    main() 