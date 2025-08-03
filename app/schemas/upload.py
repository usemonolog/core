from pydantic import BaseModel

class PresignedUrlRequest(BaseModel):
    fileType: str
    fileName: str

class PresignedUrlResponse(BaseModel):
    presignedUrl: str
    fileUrl: str
    expiresIn: int