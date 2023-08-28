# Aws S3 Upload
Welcome to the AWS-S3-Upload guide, where we explore three distinct methods for efficiently uploading objects to an Amazon S3 bucket using the Python SDK. In this comprehensive guide, we address the limitations of the put_object method by delving into alternative approaches that leverage the power of S3 APIs, multithreading, and multiprocessing. Additionally, we enhance the code's versatility by utilizing the ArgParse library, allowing seamless command-line usage.

# Overview
## 1. put_object Method
The guide commences with an exploration of the put_object method—a fundamental approach to uploading single objects to an S3 bucket. While straightforward, this method has limitations, including a maximum object size of 5GB and potential performance bottlenecks due to uploading the complete object in a single HTTP request.

## 2. Multipart Upload with Multithreading
Recognizing the need to overcome these limitations, we dive into the intricacies of S3's API and employ a multithreading approach for multipart uploads. By breaking down the object into smaller parts and concurrently uploading them, we improve upload efficiency and mitigate the impact of I/O-intensive operations. The use of multithreading optimizes the upload process for I/O-bound tasks.

## 3. Multipart Upload with Multiprocessing
Continuing our journey, we explore multipart upload utilizing multiprocessing—an alternative approach to parallelize the upload process. Although we acknowledge that upload and download tasks are I/O-intensive rather than computation-heavy, the multiprocessing approach offers notable advantages in terms of performance. Our code maintains data integrity while significantly reducing upload time compared to the put_object method.

# Performance Comparison
To provide a practical perspective on the efficiency gains, we conducted a comparative analysis of the three methods for uploading a substantial 1.2GB file. The results were as follows:

put_object Method: Time Elapsed: 86s   
Multipart - Multithreading: Time Elapsed: 43s  
Multipart - Multiprocessing: Time Elapsed: 53s 

It's evident that the put_object method exhibited the slowest performance due to its single HTTP request nature. While comparing the multithreading and multiprocessing approaches, it's important to recognize the significance of I/O-intensive operations. As anticipated, multithreading proved to be more efficient for this use case. Notably, the multiprocessing approach still delivered a considerable improvement over the basic put_object method.
