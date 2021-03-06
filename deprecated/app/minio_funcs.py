#© 2020 By The Rector And Visitors Of The University Of Virginia

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from minio import Minio
import os
import hashlib
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,BucketAlreadyExists)

MINIO_URL = os.environ.get("MINIO_URL", "minionas.uvadcos.io")
MINIO_SECRET = os.environ.get("MINIO_SECRET")
MINIO_KEY = os.environ.get("MINIO_KEY")
ROOT_DIR = ''
def remove_file(bucket,location):
    minioClient = Minio(MINIO_URL,
                    access_key=MINIO_KEY,
                    secret_key=MINIO_SECRET,
                    secure=False)

    try:
        minioClient.remove_object(bucket,location)

    except:
        return False, 'Object does not exist'

    return True, None


def bucket_exists(bucketName):

    minioClient = Minio(MINIO_URL,
                    access_key=MINIO_KEY,
                    secret_key=MINIO_SECRET,
                    secure=False)

    try:
        result = minioClient.bucket_exists(bucketName)

    except:
        return False

    return result


def make_bucket(bucketName):
    minioClient = Minio(MINIO_URL,
                    access_key=MINIO_KEY,
                    secret_key=MINIO_SECRET,
                    secure=False)
    try:
        minioClient.make_bucket(bucketName)

    except Exception as err:
        return False, str(err)

    return True, None


def delete_bucket(bucketName):
    minioClient = Minio(MINIO_URL,
                    access_key=MINIO_KEY,
                    secret_key=MINIO_SECRET,
                    secure=False)

    if bucketName == 'prevent' or bucketName == 'breakfast' or bucketName == 'puglia':
        return "Can't delete that bucket"

    try:
        minioClient.remove_bucket(bucketName)

    except Exception as err:
        return False, str(err)

    return True, None


def download_script(bucket,location):

    minioClient = Minio(MINIO_URL,
                    access_key= MINIO_KEY,
                    secret_key= MINIO_SECRET,
                    secure=False)
    data = minioClient.get_object(bucket, location)
    file_name = location.split('/')[-1]

    with open(ROOT_DIR + '/app/' + file_name, 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)

    return './' + file_name


def upload(f,name,bucket,folder = ''):
    #filename = get_filename(file)
    minioClient = Minio(MINIO_URL,
                    access_key= MINIO_KEY,
                    secret_key= MINIO_SECRET,
                    secure=False)
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)
    if size == 0:
        return {'upload':False,'error':"Empty File"}
    # try:
    minioClient.put_object(bucket, folder + name, f, size)
    # except ResponseError as err:
    #
    #     return {'upload':False}
    #f.save(secure_filename(f.filename))
    return {'upload':True,'location':'breakfast/' + folder + name}


def get_obj_hash(name,bucket,folder = ''):

    minioClient = Minio(MINIO_URL,
                    access_key= MINIO_KEY,
                    secret_key= MINIO_SECRET,
                    secure=False)
    result = minioClient.stat_object(bucket, folder + name)

    return result.etag
def get_sha256(f):
    f.seek(0)
    sha256_hash = hashlib.sha256()
    for byte_block in iter(lambda: f.read(4096),b""):
        sha256_hash.update(byte_block)
    hash = sha256_hash.hexdigest()
    return hash
