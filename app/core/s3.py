import boto3
import io
import uuid
from datetime import datetime
from app.core.config import settings
from botocore.exceptions import NoCredentialsError, ClientError

class S3Client:
    def __init__(self):
        if not all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.S3_BUCKET_NAME]):
            self.enabled = False
            print("S3 disabled: Missing AWS credentials or bucket name")
            return
        
        try:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.bucket = settings.S3_BUCKET_NAME
            
            # Try to test bucket access, but don't fail if limited permissions
            try:
                self.s3.head_bucket(Bucket=self.bucket)
                print(f"S3 initialized successfully with bucket: {self.bucket}")
                self.enabled = True
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code in ['403', 'Forbidden', 'AccessDenied']:
                    # Limited permissions but S3 client might still work for uploads
                    print(f"S3 initialized with limited access to bucket: {self.bucket} (Access may be restricted)")
                    self.enabled = True  # Try to enable anyway
                else:
                    # More serious errors like bucket not existing
                    self.enabled = False
                    print(f"S3 disabled: Bucket error - {e}")
            
        except NoCredentialsError:
            self.enabled = False
            print("S3 disabled: Invalid AWS credentials")
        except Exception as e:
            self.enabled = False
            print(f"S3 disabled: Initialization error - {e}")

    def upload_file(self, file_path, key):
        """Upload file from local path"""
        if not self.enabled:
            return None
        try:
            self.s3.upload_file(file_path, self.bucket, key)
            return self.get_file_url(key)
        except Exception as e:
            print(f"S3 upload error: {e}")
            return None

    def upload_file_bytes(self, file_bytes, filename, user_id=None, content_type=None):
        """Upload file from bytes with automatic key generation"""
        if not self.enabled:
            print("S3 upload skipped: S3 not enabled")
            return None
        
        try:
            # Generate unique key for file
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            file_extension = filename.split('.')[-1].lower()
            
            if user_id:
                key = f"resumes/{user_id}/{timestamp}_{unique_id}.{file_extension}"
            else:
                key = f"resumes/anonymous/{timestamp}_{unique_id}.{file_extension}"
            
            print(f"Attempting S3 upload: bucket={self.bucket}, key={key}")
            
            # Create file-like object from bytes
            file_obj = io.BytesIO(file_bytes)
            
            # Upload to S3
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            else:
                # Set content type based on file extension
                if file_extension == 'pdf':
                    extra_args['ContentType'] = 'application/pdf'
                elif file_extension == 'docx':
                    extra_args['ContentType'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            
            self.s3.upload_fileobj(file_obj, self.bucket, key, ExtraArgs=extra_args)
            print(f"S3 upload successful: s3://{self.bucket}/{key}")
            
            # Return file info
            return {
                'key': key,
                'url': self.get_file_url(key),
                'public_url': f"https://{self.bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}",
                'bucket': self.bucket,
                'size': len(file_bytes),
                'filename': filename
            }
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            print(f"S3 upload failed - AWS Error {error_code}: {error_message}")
            
            if error_code == 'AccessDenied':
                print("Solution: Add s3:PutObject permission to your AWS user/role")
                print(f"Resource: arn:aws:s3:::{self.bucket}/*")
            elif error_code == 'NoSuchBucket':
                print(f"Solution: Create bucket '{self.bucket}' or check bucket name")
            
            return None
        except Exception as e:
            print(f"S3 upload bytes error: {e}")
            return None

    def download_file(self, key, file_path):
        """Download file to local path"""
        if not self.enabled:
            return False
        try:
            self.s3.download_file(self.bucket, key, file_path)
            return True
        except Exception as e:
            print(f"S3 download error: {e}")
            return False

    def get_file_url(self, key):
        """Get permanent file URL"""
        if not self.enabled:
            return None
        return f"https://{self.bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

    def generate_presigned_url(self, key, expiration=3600):
        """Generate temporary signed URL"""
        if not self.enabled:
            return None
        try:
            return self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': key},
                ExpiresIn=expiration
            )
        except Exception as e:
            print(f"S3 presigned URL error: {e}")
            return None

    def delete_file(self, key):
        """Delete file from S3"""
        if not self.enabled:
            return False
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
            return True
        except Exception as e:
            print(f"S3 delete error: {e}")
            return False

    def list_user_files(self, user_id):
        """List all files for a specific user"""
        if not self.enabled:
            return []
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket,
                Prefix=f"resumes/{user_id}/"
            )
            return response.get('Contents', [])
        except Exception as e:
            print(f"S3 list files error: {e}")
            return []

# Initialize S3 client
s3client = S3Client()
