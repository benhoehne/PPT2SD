from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, after_this_request
import os
from werkzeug.utils import secure_filename
from SD_Generator import H5PSlideDeckGenerator
import tempfile
import uuid
import shutil
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

ALLOWED_EXTENSIONS = {'pptx', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_project_name(filename):
    """Extract project name from filename without extension"""
    return os.path.splitext(filename)[0]

def cleanup_project_files(project_name):
    """Clean up all project-related files after download"""
    try:
        # Remove H5P package from uploads folder
        h5p_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{project_name}.h5p")
        if os.path.exists(h5p_file):
            os.remove(h5p_file)
            logger.info(f"Removed H5P package: {h5p_file}")
        
        # Remove project directory from 00_Output
        project_dir = os.path.join('00_Output', project_name)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
            logger.info(f"Removed project directory: {project_dir}")
            
        logger.info(f"Cleaned up files for project: {project_name}")
    except Exception as e:
        logger.error(f"Error cleaning up files: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    pdf_file = request.files['pdf']
    pptx_file = request.files.get('pptx')
    project_title = request.form.get('title', '')

    if pdf_file.filename == '':
        return jsonify({'error': 'No selected PDF file'}), 400
    
    if not allowed_file(pdf_file.filename):
        return jsonify({'error': 'Invalid PDF file type'}), 400
    
    if pptx_file and pptx_file.filename != '' and not allowed_file(pptx_file.filename):
        return jsonify({'error': 'Invalid PPTX file type'}), 400

    try:
        # Create a temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            pdf_path = os.path.join(temp_dir, secure_filename(pdf_file.filename))
            pdf_file.save(pdf_path)
            
            pptx_path = None
            if pptx_file and pptx_file.filename != '':
                pptx_path = os.path.join(temp_dir, secure_filename(pptx_file.filename))
                pptx_file.save(pptx_path)

            # Get project name from PDF filename
            project_name = get_project_name(pdf_file.filename)
            if not project_title:
                project_title = project_name

            # Initialize generator
            generator = H5PSlideDeckGenerator(project_name=project_name)
            generator.project_title = project_title
            generator.source_pdf = Path(pdf_path)
            
            # Process files
            success = generator.split_pdf_into_slides()
            if not success:
                return jsonify({'error': 'Failed to process PDF'}), 500

            # Extract audio and notes from PPTX if provided
            slide_notes = {}
            if pptx_path:
                success, slide_notes = generator.extract_audio_from_pptx(pptx_path)
                if not success:
                    return jsonify({'error': 'Failed to extract audio and notes from PPTX'}), 500

            # Generate the H5P package
            output_filename = f"{project_name}.h5p"
            if not generator.build_h5p_package(output_filename, slide_notes):
                return jsonify({'error': 'Failed to generate H5P package'}), 500

            # Move the generated file to uploads folder
            source_path = generator.output_path
            target_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            # Remove target file if it exists
            if os.path.exists(target_path):
                os.remove(target_path)
            
            # Use shutil.move instead of os.rename for cross-device compatibility
            shutil.move(str(source_path), target_path)

            # Redirect to download page
            return redirect(url_for('download', 
                                  filename=output_filename,
                                  project_name=project_name,
                                  project_title=project_title))

    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        return jsonify({'error': 'An error occurred during processing'}), 500

@app.route('/download/<filename>')
def download(filename):
    project_name = request.args.get('project_name', '')
    project_title = request.args.get('project_title', project_name)
    return render_template('download.html', 
                         filename=filename,
                         project_name=project_name,
                         project_title=project_title)

@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return "File not found", 404
            
        @after_this_request
        def cleanup(response):
            # Extract project name from filename
            project_name = get_project_name(filename)
            cleanup_project_files(project_name)
            return response
            
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True) 