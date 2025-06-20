# PPT2SD - PowerPoint to H5P SlideDeck Converter

A modern web application that converts PowerPoint presentations into interactive H5P SlideDeck packages. Upload your PDF slides and PPTX files to create engaging, web-ready presentations with embedded audio and speaker notes.

## ✨ Features

- **📄 PDF to Slides**: Automatically splits PDF presentations into individual slide components
- **🎵 Audio Integration**: Extracts and embeds audio files from PPTX presentations
- **📝 Speaker Notes**: Preserves and includes speaker notes from PowerPoint files
- **🌐 Modern Web Interface**: Clean, responsive UI with drag-and-drop file upload
- **⚡ Real-time Processing**: Live conversion progress with notifications
- **📦 H5P Package Generation**: Creates complete .h5p files ready for LMS deployment
- **🧹 Automatic Cleanup**: Smart file management with post-download cleanup

## 🚀 Quick Start

### Prerequisites

- **Python 3.13** with venv support
- **Node.js** (for Tailwind CSS build process)
- **Git** for cloning the repository

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/benhoehne/PPT2SD.git
cd PPT2SD
```

2. **Set up Python environment:**
```bash
python3.13 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. **Install Node.js dependencies:**
```bash
npm install
```

4. **Build CSS assets:**
```bash
npm run css-watch  # For development with auto-rebuild
# OR for production:
npx @tailwindcss/cli -i ./src/css/input.css -o ./static/css/output.css --minify
```

5. **Run the application:**
```bash
# Development mode (with CSS watching):
npm run dev

# OR manual Flask run:
python app.py
```

Visit `http://localhost:5000` to access the application.

## 📋 How to Use

### Basic Workflow

1. **Upload PDF** (Required): Your presentation slides exported as PDF
2. **Upload PPTX** (Optional): Your original PowerPoint file containing:
   - Embedded audio files
   - Speaker notes
   - Additional metadata
3. **Convert**: Click "Convert to H5P SlideDeck" 
4. **Download**: Receive your complete .h5p package

### File Requirements

- **PDF Files**: Up to 100MB, exported presentation slides
- **PPTX Files**: Up to 100MB, original PowerPoint with audio/notes
- **Supported Audio**: MP3 format embedded in PPTX slides
- **Notes Format**: Standard PowerPoint speaker notes

## 🏗️ Project Architecture

### Directory Structure
```
PPT2SD/
├── app.py                    # Main Flask application
├── SD_Generator.py           # Core H5P generation logic
├── config.py                 # Project configuration
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies & scripts
├── tailwind.config.js        # Tailwind CSS configuration
├── 
├── src/css/
│   └── input.css            # Tailwind source
├── static/
│   ├── css/output.css       # Compiled CSS
│   └── img/                 # Static images
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Upload interface
│   └── download.html        # Download page
├── Template_SD/             # H5P SlideDeck template
│   ├── H5P.SlideDeck-1.0/   # Main SlideDeck library
│   ├── H5P.Audio-1.5/       # Audio component
│   ├── H5P.PDFViewer-1.0/   # PDF display component
│   └── [other H5P libraries]/
├── 00_Output/               # Generated project files
├── uploads/                 # Temporary upload storage
└── venv/                    # Python virtual environment
```

### Technical Stack

**Backend:**
- Flask (Web framework)
- PyPDF2 (PDF processing)
- python-pptx (PowerPoint processing)
- python-docx (Document handling)
- Pillow (Image processing)

**Frontend:**
- Tailwind CSS v4 (Styling)
- Vanilla JavaScript (Interactions)
- Modern responsive design

**H5P Integration:**
- Custom H5P.SlideDeck template
- Multi-media content support
- LMS-compatible package generation

## 🛠️ Development

### Development Scripts

```bash
# Start development server with CSS watching
npm run dev

# Watch CSS changes only
npm run css-watch

# Build production CSS
npx @tailwindcss/cli -i ./src/css/input.css -o ./static/css/output.css --minify
```

### Adding Features

1. **H5P Components**: Add new libraries to `Template_SD/`
2. **Processing Logic**: Extend `SD_Generator.py` for new content types
3. **UI Components**: Update templates and rebuild CSS
4. **API Endpoints**: Add routes in `app.py`

### Configuration

Edit `config.py` to customize:
- Default project settings
- File paths and directories
- Processing parameters

## 🚀 Deployment

### Production Setup

1. **Build assets:**
```bash
npx @tailwindcss/cli -i ./src/css/input.css -o ./static/css/output.css --minify
```

2. **Use production WSGI server:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

3. **Configure reverse proxy** (nginx recommended)
4. **Set environment variables** for production paths

### Environment Variables

```bash
FLASK_ENV=production
MAX_CONTENT_LENGTH=104857600  # 100MB
UPLOAD_FOLDER=/path/to/uploads
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure CSS builds correctly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [H5P](https://h5p.org/) - Interactive content framework
- [Flask](https://flask.palletsprojects.com/) - Web application framework  
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint processing
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF manipulation

---

**Developed by [Evoltas](https://evoltas.de)** | Visit our website for more educational technology solutions.
