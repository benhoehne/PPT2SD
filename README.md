# PPT 2 SlideDeck

A web application that converts PowerPoint presentations into H5P SlideDeck format, preserving audio and notes. Built with Flask and modern web technologies.

## Features

- Convert PowerPoint presentations to H5P SlideDeck format
- Extract and preserve embedded audio from PPTX files
- Extract and preserve slide notes from PPTX files
- Modern, responsive web interface
- Drag-and-drop file upload
- Automatic matching of audio and notes to corresponding slides

## Prerequisites

- Python 3.13
- Node.js and npm
- Virtual environment (venv)

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PPT2SD.git
cd PPT2SD
```

2. Set up Python virtual environment:
```bash
python3.13 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies:
```bash
npm install
```

5. Build Tailwind CSS:
```bash
npx tailwindcss -i ./static/css/main.css -o ./static/css/output.css --watch
```

6. Run the Flask application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
PPT2SD/
├── app.py                 # Flask application
├── SD_Generator.py        # Core conversion logic
├── static/
│   ├── css/
│   │   ├── main.css      # Tailwind CSS source
│   │   └── output.css    # Compiled CSS
│   ├── js/               # JavaScript files
│   └── img/              # Images
├── templates/
│   └── index.html        # Main template
├── uploads/              # Temporary upload directory
├── venv/                 # Python virtual environment
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind configuration
└── requirements.txt      # Python dependencies
```

## Usage

1. Open the web interface in your browser
2. Upload your PDF slides (required)
3. Optionally upload your PPTX file to include:
   - Embedded audio files
   - Slide notes
4. Click "Convert" to generate the H5P SlideDeck
5. Download the generated .h5p file

## Development

### Adding New Features

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

### Building for Production

1. Update the Tailwind CSS:
```bash
npx tailwindcss -i ./static/css/main.css -o ./static/css/output.css --minify
```

2. Use a production WSGI server (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn app:app
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- H5P SlideDeck library
- Flask web framework
- Tailwind CSS
- Python-pptx library
