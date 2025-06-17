import os
from pathlib import Path


# Project configuration
PROJECT_NAME = "BI_PV_LU01"
PROJECT_TITLE = "Solar Power Systems"

# Derive common paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, '00_Output', PROJECT_NAME)
VO_DIR = os.path.join(OUTPUT_DIR, 'VO')
PNG_DIR = os.path.join(OUTPUT_DIR, 'png')
NOTES_DOCX = os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}_NOTES.docx")
PDF_DOC = os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}.pdf")


def create_directories():
    """Create all necessary directories"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(VO_DIR, exist_ok=True)

# Create directories on import
create_directories()