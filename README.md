# JPG to PDF Converter

A minimalist web application to convert JPG/JPEG images to PDF files.

## Features

- Drag and drop interface
- Supports JPG/JPEG files
- Instant PDF download
- No file storage on server

## Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:3001

## Deploy to Railway

1. Push to GitHub
2. Connect repo on [railway.app](https://railway.app)
3. Deploy

## Tech Stack

- Python / Flask
- Pillow (image processing)
- Vanilla JS frontend
