from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_payload
from app.core.config import settings
import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import datetime, timedelta, timezone

from app.schemas.upload import PresignedUrlRequest, PresignedUrlResponse

router = APIRouter()

# Configure Cloudflare R2 client
r2_client = boto3.client(
    's3',
    endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT, 
    aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_ACCESS_KEY,
    region_name='auto'  # R2 uses 'auto' for region
)

@router.post("/presigned-url", response_model=PresignedUrlResponse)
async def generate_presigned_url(
    request: PresignedUrlRequest,
    auth_payload: dict = Depends(get_payload)
):
    """Generate a presigned URL for uploading audio files to Cloudflare R2"""
    
    try:
        # Validate file type
        allowed_types = ['audio/webm', 'audio/wav', 'audio/mp3', 'audio/m4a']
        if request.fileType not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed types: {allowed_types}"
            )
        
        # Generate unique file name
        user_id = auth_payload.get("sub")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        # Extract file extension from original filename
        file_extension = request.fileName.split('.')[-1] if '.' in request.fileName else 'webm'
        
        # Create structured path: audio/{user_id}/{year}/{month}/{filename}
        current_date = datetime.now(timezone.utc)
        object_key = f"audio/{user_id}/{current_date.year}/{current_date.month:02d}/{timestamp}_{unique_id}.{file_extension}"
        
        # Generate presigned URL for PUT operation
        expiration = 3600  # 1 hour
        
        presigned_url = r2_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.CLOUDFLARE_R2_BUCKET_NAME,
                'Key': object_key,
                'ContentType': request.fileType,
                'ContentDisposition': f'attachment; filename="{request.fileName}"'
            },
            ExpiresIn=expiration
        )
        
        # Generate the public URL for accessing the file
        file_url = f"{settings.CLOUDFLARE_R2_PUBLIC_URL}/{object_key}"
        
        return PresignedUrlResponse(
            presignedUrl=presigned_url,
            fileUrl=file_url,
            expiresIn=expiration
        )
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate presigned URL: {error_code}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.delete("/audio/{object_key}")
async def delete_audio_file(
    object_key: str,
    auth_payload: dict = Depends(get_payload)
):
    """Delete an audio file from Cloudflare R2"""
    
    try:
        # Verify the user owns this file (object_key should contain user_id)
        user_id = auth_payload.get("sub")
        if not object_key.startswith(f"audio/{user_id}/"):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this file"
            )
        
        r2_client.delete_object(
            Bucket=settings.CLOUDFLARE_R2_BUCKET_NAME,
            Key=object_key
        )
        
        return {"message": "File deleted successfully"}
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            raise HTTPException(status_code=404, detail="File not found")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete file: {error_code}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )