import os
import subprocess

DEBUG = True

GIT_ROOT = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip()
MEDIA_FOLDER = os.path.join(GIT_ROOT, 'media')
MEDIA_URL = '/media/'
THUMBNAIL_SIZE = '300x168'
