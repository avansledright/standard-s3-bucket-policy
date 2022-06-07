# S3 Standard Policy
This simple script will add a bucket policy to a provided S3 bucket

## Usage
python3 main.py <bucket-name>

Replace bucket-name with the name of your bucket. The script will check to see if you have a bucket policy already deployed. If you do, it will add the new statement that denies traffic not from HTTPS. If you do not have a policy it will add the standard policy to your bucket.