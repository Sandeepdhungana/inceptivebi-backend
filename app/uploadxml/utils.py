import uuid
from ..socket import socketio
import io
import zipfile


def get_unique_file_name(file_name):
    extension = get_extension(file_name)
    return f"{uuid.uuid4()}.{extension}"


def get_extension(file_name):
    extension = file_name.split(
        '.')[-1] if '.' in file_name else ''
    return extension


def emit_file_processing(message="", progress=0, error="", summary=[]):
    socketio.emit('file_upload_response', {
        'message': message,
        "progress": progress,
        "error": error,
        "summary": summary
    })
