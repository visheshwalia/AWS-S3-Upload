#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import time
import argparse
import boto3
import json
import multiprocessing
import os

os.chdir(r'/Users/vishesh/Downloads')


def start_upload(bucket, key):
    s3_client = boto3.client('s3')
    response = s3_client.create_multipart_upload(
                Bucket = bucket,
                Key = key)
    
    return response['UploadId']

def add_part(proc_queue, body, bucket, key, upload_id, part_number):
    s3_client = boto3.client('s3')
    
    response = s3_client.upload_part(
                Body = body,
                Bucket = bucket,
                Key = key,
                UploadId = upload_id,
                PartNumber = part_number
                )
    
    print(f"Finished part: {part_number}, ETag: {response['ETag']}")
    proc_queue.put({"PartNumber" : part_number, "ETag" : response["ETag"]})
    
    return
          
          
def end_upload(bucket, key, upload_id, finished_parts):
    s3_client = boto3.client('s3')
          
    response = s3_client.complete_multipart_upload(
                      Bucket = bucket,
                      Key = key,
                      MultipartUpload = {
                          "Parts" : finished_parts
                      },
                      UploadId = upload_id)
          
    return response

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', required = True, help = 'file that needs to be chunked')
    ap.add_argument('-k', '--key', help = 'key for the bucket object')
    ap.add_argument('-b', '--bucket', required = True, help = 'destination bucket')
    ap.add_argument('-cs', '--chunksize', required = True, type = int, help = 'chunk size in MB, >5MB', choices = range(5,101)                   ,metavar = '[5-100]' )
    ap.add_argument('-p', '--processes', choices = range(0,256), type = int, metavar = '[0-256]', default = 10, help = 'number of processes to run simultaneously')
    
    args = vars(ap.parse_args())
    
    if args['key'] in ('', None):
        args['key'] = args['file']
        
    file = args['file']
    key = args['key']
    bucket = args['bucket']
    sim_proc = args['processes']
    upload_id = start_upload(bucket, key)
    print(f'Starting upload: {upload_id}')
    
    file_upload = open(file, 'rb')
    part_procs = []
    queue_returns = []
    proc_queue = multiprocessing.Queue()
    chunk_size = (args['chunksize'] * 1024) * 1024
    part_number = 1
    chunk = file_upload.read(chunk_size)
    
    while len(chunk) > 0:
        proc = multiprocessing.Process(target = add_part, args = (proc_queue, chunk, bucket, key, upload_id, part_number))
        part_procs.append(proc)
        part_number += 1
        chunk = file_upload.read(chunk_size)
    
    part_procs = [part_procs[i:i + sim_proc] for i in range(0, len(part_procs), sim_proc)]

        
    for i in range(len(part_procs)):
        for p in part_procs[i]:
            p.start()
        
        for p in part_procs[i]:
            p.join()
        
        for p in part_procs[i]:
            queue_returns.append(proc_queue.get())
            
    queue_returns = sorted(queue_returns, key = lambda i: i['PartNumber'])
    response = end_upload(bucket, key, upload_id, queue_returns)
    print(json.dumps(response, sort_keys = True, indent = 4))
    

if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    print(f'Finished upload in {t2 - t1} seconds')
          

