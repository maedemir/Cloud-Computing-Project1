#-------------- image_storage code --------------
# in this file we have some functions to store and get images in arvan object storage

import boto3
import logging
from botocore.exceptions import ClientError

def upload_image_s3(path , name):
   # Configure logging
   logging.basicConfig(level=logging.INFO)
   try:
      s3_resource = boto3.resource(
         's3',
         endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
         aws_access_key_id='86f378f2-ba7a-43b8-80f1-d5daaf3c57c2',
         aws_secret_access_key='53d7d9101ccdf6f5beb0e082f7af1014a1133b47'
      )

   except Exception as exc:
      logging.error(exc)
   else:
      try:
         bucket = s3_resource.Bucket('hw1-cc')
         file_path = path
         object_name = name

         with open(file_path, "rb") as file:
               bucket.put_object(
                  ACL='private',
                  Body=file,
                  Key=object_name
               )
      except ClientError as e:
         logging.error(e)

def download_image_s3(id):

   logging.basicConfig(level=logging.INFO)

   try:
      s3_resource = boto3.resource(
         's3',
         endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
         aws_access_key_id='86f378f2-ba7a-43b8-80f1-d5daaf3c57c2',
         aws_secret_access_key='53d7d9101ccdf6f5beb0e082f7af1014a1133b47'
      )
   except Exception as exc:
      logging.error(exc)
   else:
      try:
         # bucket
         bucket = s3_resource.Bucket('hw1-cc')

         object_name = str(id)+'.png'
         download_path = './temp/'+str(id)+'.png'

         bucket.download_file(
               object_name,
               download_path
         )
      except ClientError as e:
         logging.error(e)
