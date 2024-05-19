import os
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi import status
import logging

logger = logging.getLogger(__name__)

def list_directory(config,  path: str = '/'):
    if path.startswith('/'):
        path = path[1:]
    abs_path = os.path.join(config.workspace_base, path)
    try:
        files = os.listdir(abs_path)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'error': 'Path not found'},
        )
    files = [
        f + '/' if os.path.isdir(os.path.join(config.workspace_base, f)) else f for f in files
    ]
    return files
