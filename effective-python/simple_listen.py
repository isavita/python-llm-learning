import os
import logger

def list_files(config, path: str = '/'):
    if path.startswith('/'):
        path = path[1:]
    abs_path = os.path.join(config.workspace_base, path)
    try:
        files = os.listdir(abs_path)
    except Exception as e:
        logger.error(f'Error listing files: {e}', exc_info=False)
        raise e

    return files
