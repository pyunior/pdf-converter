from flask import Flask, render_template, request, send_file
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'files' not in request.files:
        return 'No files uploaded', 400

    files = request.files.getlist('files')

    if not files or files[0].filename == '':
        return 'No files selected', 400

    if len(files) > 5:
        return 'Maximum 5 files allowed', 400

    for file in files:
        if not allowed_file(file.filename):
            return f'Only JPG/JPEG files are allowed: {file.filename}', 400

    try:
        images = []
        for file in files:
            img = Image.open(file.stream)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            images.append(img)

        pdf_buffer = io.BytesIO()

        if len(images) == 1:
            images[0].save(pdf_buffer, 'PDF', resolution=100.0)
        else:
            images[0].save(pdf_buffer, 'PDF', resolution=100.0, save_all=True, append_images=images[1:])

        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='converted.pdf'
        )
    except Exception as e:
        return f'Error converting files: {str(e)}', 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port)
