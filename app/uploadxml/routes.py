from flask import Blueprint, request, jsonify
from app.uploadxml.utils import get_extension, get_unique_file_name, emit_file_processing
import os
from app.uploadxml.models import S3Utils
import boto3
from ..socket import socketio
import io
import zipfile


upload_bp = Blueprint('upload', __name__)


def some_long_running_task():
    for i in range(1, 11):
        socketio.sleep(1)
        socketio.emit('file_upload_response', {
                      'message': f'Processing {i*10}% complete'})
    socketio.emit('file_upload_response', {'message': 'Processing complete'})


def process_further(extracted_file, name, summary, progress):
    _, file_extension = os.path.splitext(name)
    try:
        emit_file_processing(f"Processing file {name}", progress=progress)
        summary.append(
            {"file_name": name, "status": "completed", "completed": True})
    except Exception as e:
        emit_file_processing(f"Error Processing {name}: {str(e)}")
        summary.append(
            {"file_name": name, "status": f"error: {str(e)}", "completed": False})


def process_file(file_name):
    emit_file_processing("Processing started", progress=0)
    file_from_s3 = S3Utils(bucket_name='edataq').get_s3_files(file_name)
    file_like_object = io.BytesIO(file_from_s3)

    summary = []

    with zipfile.ZipFile(file_like_object) as z:
        total_files = len(z.namelist())
        for idx, name in enumerate(z.namelist()):
            socketio.sleep(3)
            progress = int(((idx + 1) / total_files) * 100)
            with z.open(name) as extracted_file:
                process_further(extracted_file, name, summary, progress)

    successful_files = sum(1 for item in summary if item['completed'])

    emit_file_processing(f"Processing Finished: {successful_files}/{total_files} files processed successfully.",
                         progress=100, summary=summary)


@upload_bp.route('/s3-signed-url', methods=['GET'])
def get_signed_url():
    file_name = request.args.get('file_name')
    extension = get_extension(file_name)
    if extension != 'zip':
        return jsonify({"message": "Invalid. Please upload zip file only"}), 400

    unique_file_name = get_unique_file_name(file_name)

    bucket_name = os.getenv('AWS_S3_BUCKET')

    s3_utils = S3Utils(bucket_name)
    signed_url = s3_utils.generate_presigned_url(file_name=unique_file_name)

    if signed_url:

        return jsonify({
            'url': signed_url,
            'file_name': unique_file_name
        }), 200

    return jsonify({
        'message': "There was some problem while uploading file. Please try again later"
    }), 401


@socketio.on("start_processing")
def start_file_processing(data):
    file_name = data.get('file', None)
    if file_name:
        socketio.start_background_task(process_file, file_name)


# @socketio.on("start_processing")
# def start_file_processing(data):
#     socketio.start_background_task(some_long_running_task)
