#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Use put_object to store object in S3 bucket.
import time
import boto3
import argparse
import os
from boto3.s3.transfer import TransferConfig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required = True, help = 'File that needs to be uploaded')
    ap.add_argument('-b', '--bucket', required = True, help = 'Destination bucket')
    ap.add_argument('-k', '--key', required = False, help = 'Destination object key name')
    ap.add_argument('-d', '--directory', required = False, type = str,  help = 'local file directory')
    ap.add_argument('-c', '--concurrency', required = False, default = 10, type = int, help = 'number of concurrent processes', choices = range(5,101)\
                   ,metavar = '[5-100]')
    ap.add_argument('-cs', '--chunksize', required = False, default = 25, type = int, help = 'chunksize to divide file', choices = range(5,101)\
                   ,metavar = '[5-100]')
    args = vars(ap.parse_args())
    
    if args['key'] in ['', None]:
        args['key'] = args['file']
    
    if args['directory'] in ['', None]:
        args['directory'] = os.getcwd()
    
    
    file = args['file']
    key = args['key']
    bucket = args['bucket']
    directory = args['directory']
    chunksize = args['chunksize']
    concurrency = args['concurrency']
    
    s3client = boto3.client('s3')
    s3resource = boto3.resource('s3')
    
    os.chdir(directory)

    config = TransferConfig(multipart_threshold=1024 * 25, 
                            max_concurrency=concurrency,
                            multipart_chunksize=1024 * chunksize,
                            use_threads=True)


    def multipart_upload_boto3(file, key, bucket):

        s3resource.Object(bucket, key).upload_file(file,
                                Config=config
                                )


    multipart_upload_boto3(file, key, bucket)
    
if __name__ == '__main__':
    
    t1 = time.time()
    main()
    t2 = time.time()
    print(f'Finished uploading using multipart upload using multithreading in {t2 - t1} seconds')

