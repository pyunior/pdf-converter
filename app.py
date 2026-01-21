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
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    if not allowed_file(file.filename):
        return 'Only JPG/JPEG files are allowed', 400

    try:
        image = Image.open(file.stream)

        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')

        pdf_buffer = io.BytesIO()
        image.save(pdf_buffer, 'PDF', resolution=100.0)
        pdf_buffer.seek(0)

        original_name = os.path.splitext(file.filename)[0]

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{original_name}.pdf'
        )
    except Exception as e:
        return f'Error converting file: {str(e)}', 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=port)
