# Use put_object to store object in S3 bucket.
import time
import boto3
import argparse
import os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required = True, help = 'File that needs to be uploaded')
    ap.add_argument('-b', '--bucket', required = True, help = 'Destination bucket')
    ap.add_argument('-k', '--key', required = False, help = 'Destination object key name')
    ap.add_argument('-d', '--directory', required = False, type = str,  help = 'local file directory')
    args = vars(ap.parse_args())
    
    if args['key'] in ['', None]:
        args['key'] = args['file']
    
    if args['directory'] in ['', None]:
        args['directory'] = os.getcwd()
    
    
    file = args['file']
    key = args['key']
    bucket = args['bucket']
    directory = args['directory']
    
    s3client = boto3.client('s3')
    s3resource = boto3.resource('s3')
    
    
    os.chdir(directory)
    with open(file, 'rb') as file_path:
        s3client.put_object(Bucket=bucket, Key=key, Body=file_path)
    
    
if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    print(f'Finished uploading using file_upload in {t2 - t1} seconds')
