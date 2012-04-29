import os

from django.conf import settings

from boto.s3.connection import S3Connection


def download_remote_media(destination_dir):
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    
    os.makedirs(destination_dir)
    
    for key in bucket.get_all_keys():
        dest = os.path.join(destination_dir, key.name)
        if key.name.endswith('/'):
            print 'making directory %s' % dest
            os.makedirs(dest)
        else:
            print 'downloading %s to %s' % (key.name, dest)
            fh = open(dest, 'w')
            key.get_contents_to_file(fh)
            fh.close()

def upload_remote_media(src_dir):
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    for base, directories, files in os.walk(src_dir):
        for filename in files:
            full_path = os.path.join(base, filename)
            relative_path = os.path.relpath(full_path, src_dir)
            key = bucket.new_key(relative_path)
            print 'uploading %s' % relative_path
            key.set_contents_from_filename(full_path)
