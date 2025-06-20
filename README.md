# PPT2SD - PowerPoint to H5P SlideDeck Converter

A modern web application that converts PowerPoint presentations (PPTX) to H5P SlideDeck format with automatic PDF conversion, audio extraction, and slide notes preservation. Built with Flask, Google Slides API, and modern web technologies.

## ✨ Features

- **🔄 PPTX to H5P Conversion**: One-click conversion from PowerPoint to H5P SlideDeck format
- **📄 Google Slides API Integration**: High-quality PDF conversion using Google Slides API
- **🎵 Audio Extraction**: Automatically extracts embedded audio files from PPTX presentations
- **📝 Notes Preservation**: Extracts and preserves slide notes from PowerPoint speaker notes
- **🌐 Modern Web Interface**: Clean, responsive drag-and-drop interface
- **🗂️ Automatic Organization**: Smart slide numbering and audio-slide matching
- **🧹 Auto Cleanup**: Temporary files are automatically cleaned up after processing
- **⚡ Real-time Processing**: Live feedback during conversion process

## 🔧 Prerequisites

- **Python 3.13** (with venv support)
- **Node.js and npm** (for Tailwind CSS compilation)
- **Google Cloud Project** with Google Slides and Drive APIs enabled
- **Service Account Key** for Google API authentication

## 🚀 Setup Instructions

### 1. Repository Setup
```bash
git clone https://github.com/benhoehne/PPT2SD.git
cd PPT2SD
```

### 2. Python Environment Setup
```bash
# Create and activate virtual environment (following user rules for Python 3.13)
python3.13 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Node.js Dependencies
```bash
npm install
```

### 4. Google API Configuration

#### Create Google Cloud Project and Service Account:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Slides API
   - Google Drive API
4. Create a Service Account:
   - Go to IAM & Admin > Service Accounts
   - Create a new service account
   - Download the JSON key file
5. Save the key file as `google_key.json` in the project root

#### Set Environment Variables:
```bash
# Create a .env file or set environment variable
export GOOGLE_SERVICE_ACCOUNT_KEY="./google_key.json"
```

### 5. Build CSS and Start Development Server

#### Option 1: Development with auto-reload (Recommended)
```bash
# Starts both Flask app and Tailwind CSS watcher
npm run dev
```

#### Option 2: Manual setup
```bash
# Terminal 1: Start Tailwind CSS watcher
npm run css-watch

# Terminal 2: Start Flask application
python app.py
```

The application will be available at `http://localhost:5000`

## 🔄 How It Works

### Conversion Process Flow:
1. **Upload**: User uploads a PPTX file via the web interface
2. **Google Slides Conversion**: PPTX is uploaded to Google Slides and converted to high-quality PDF
3. **PDF Processing**: PDF is split into individual slide images
4. **Audio Extraction**: Embedded audio files are extracted from the original PPTX
5. **Notes Extraction**: Speaker notes are extracted from PowerPoint slides
6. **H5P Assembly**: All components are assembled into a complete H5P SlideDeck package
7. **Download**: User receives a ready-to-use .h5p file

### Technical Architecture:
- **Frontend**: Modern HTML5 with Tailwind CSS for responsive design
- **Backend**: Flask application with modular conversion pipeline
- **PDF Processing**: PyPDF2 for PDF manipulation
- **PPTX Processing**: python-pptx for PowerPoint file handling
- **Google API**: Official Google API client for Slides and Drive services
- **H5P Generation**: Custom H5P package builder following H5P specifications

## 📁 Project Structure

```
PPT2SD/
├── 📄 app.py                    # Flask web application
├── 🔧 SD_Generator.py           # Core conversion engine with Google API integration
├── ⚙️ config.py                 # Project configuration
├── 🔑 google_key.json           # Google Service Account credentials (not in repo)
├── 📦 requirements.txt          # Python dependencies
├── 📦 package.json              # Node.js dependencies for Tailwind CSS
├── ⚙️ tailwind.config.js        # Tailwind CSS configuration
├── 🎨 src/css/input.css         # Tailwind CSS source
├── 📁 static/
│   ├── 🎨 css/output.css        # Compiled Tailwind CSS
│   ├── 🖼️ img/                  # Static images
│   └── 📜 js/                   # Client-side JavaScript
├── 📄 templates/
│   ├── 🏠 index.html            # Main upload interface  
│   ├── 📥 download.html         # Download page
│   └── 🗂️ base.html             # Base template
├── 📁 Template_SD/              # H5P SlideDeck library templates
├── 📁 00_Output/                # Processing output directory
├── 📁 uploads/                  # Temporary file uploads
└── 🐍 venv/                     # Python virtual environment
```

## 🎯 Usage

### Web Interface (Recommended)
1. **Access the Application**: Navigate to `http://localhost:5000`
2. **Upload PPTX**: Drag and drop or click to upload your PowerPoint file
3. **Processing**: The system automatically:
   - Converts PPTX to PDF via Google Slides API
   - Extracts embedded audio files
   - Extracts speaker notes
   - Builds H5P SlideDeck package
4. **Download**: Receive your ready-to-use `.h5p` file

### Command Line Interface
```bash
# Basic conversion
python SD_Generator.py --pptx your-presentation.pptx

# With custom output name  
python SD_Generator.py --pptx presentation.pptx --output custom-name.h5p

# Verbose output for debugging
python SD_Generator.py --pptx presentation.pptx --verbose
```

### File Requirements
- **PPTX Format**: Only PowerPoint 2007+ format (.pptx) is supported
- **Audio Support**: MP3, WAV, M4A embedded audio files
- **Size Limit**: Up to 100MB per file
- **Notes**: Speaker notes in PowerPoint will be preserved in the H5P package

## 🛠️ Development

### Adding New Features
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes and test thoroughly
3. Update documentation if needed
4. Submit a pull request with clear description

### Code Structure
- **`SD_Generator.py`**: Core conversion logic with three main classes:
  - `H5PSlideDeckGenerator`: Handles H5P package creation
  - `GoogleSlidesConverter`: Manages Google API interactions
  - `CombinedSlideDeckGenerator`: Orchestrates the complete workflow
- **`app.py`**: Flask web application with upload/download endpoints
- **`config.py`**: Project configuration and path management

### Development Tools
```bash
# Run tests (if available)
python -m pytest

# Format code (if using black)
black SD_Generator.py app.py

# Type checking (if using mypy)
mypy SD_Generator.py
```

## 🚀 Production Deployment

### Build Production Assets
```bash
# Build optimized CSS
npm run css-watch -- --minify

# Or manually with Tailwind CLI
npx @tailwindcss/cli -i ./src/css/input.css -o ./static/css/output.css --minify
```

### Deploy with Gunicorn
```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Run with Gunicorn
gunicorn app:app --bind 0.0.0.0:8000 --workers 4

# Or with specific configuration
gunicorn app:app -c gunicorn.conf.py
```

### Environment Variables for Production
```bash
export GOOGLE_SERVICE_ACCOUNT_KEY="/path/to/service-account-key.json"
export FLASK_ENV="production"
export FLASK_DEBUG="False"
```

## 🔧 Troubleshooting

### Common Issues

#### Google API Authentication Errors
- Ensure service account key file exists and path is correct
- Verify Google Slides and Drive APIs are enabled
- Check service account has necessary permissions

#### PPTX Processing Errors
- Verify file is valid PPTX format (not PPT)
- Check file size is under 100MB limit
- Ensure embedded audio is in supported formats (MP3, WAV, M4A)

#### H5P Package Issues
- Verify Template_SD directory exists and is complete
- Check output directory permissions
- Ensure sufficient disk space for temporary files

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[H5P](https://h5p.org/)** - Interactive content framework
- **[Google Slides API](https://developers.google.com/slides)** - High-quality PDF conversion
- **[Flask](https://flask.palletsprojects.com/)** - Web framework
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[python-pptx](https://python-pptx.readthedocs.io/)** - PowerPoint processing library
- **[PyPDF2](https://pypdf2.readthedocs.io/)** - PDF manipulation library

## 📞 Support

For support and questions:
- 📧 Create an issue on GitHub
- 🌐 Visit [evoltas.de](https://evoltas.de) for more information

---

**Made with ❤️ for educational content creators**
