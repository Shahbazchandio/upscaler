from flask import Blueprint, request, send_file
from app.services.image_processor import process_image
import io

bp = Blueprint('api', __name__)

@bp.route('/process', methods=['POST'])
def process_image_route():
    if 'file' not in request.files:
        return {'error': 'No file part'}, 400
    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    model_type = request.form.get('model_type', 'upscale')
    if model_type not in ['upscale', 'enhance']:
        return {'error': 'Invalid model type'}, 400
    
    try:
        processed_image = process_image(file.read(), model_type)
        return send_file(
            io.BytesIO(processed_image),
            mimetype='image/png',
            as_attachment=True,
            attachment_filename=f'{model_type}d_{file.filename}'
        )
    except Exception as e:
        return {'error': str(e)}, 500