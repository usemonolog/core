from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_session
from app.models.feedback import Feedback as FeedbackModel
from app.schemas.feedback import Feedback
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.auth import get_payload
import uuid

router = APIRouter()

@router.get("/{submission_id}", response_model=Feedback)
async def read_feedback(
    submission_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    auth_payload: dict = Depends(get_payload)
):
    """Get feedback for a specific submission"""
    stmt = select(FeedbackModel).where(FeedbackModel.submission_id == submission_id)
    result = await session.execute(stmt)
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return feedback

@router.get("/structured/{submission_id}")
async def get_structured_feedback(
    submission_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    auth_payload: dict = Depends(get_payload)
):
    """Get the structured feedback JSON for a submission"""
    stmt = select(FeedbackModel).where(FeedbackModel.submission_id == submission_id)
    result = await session.execute(stmt)
    feedback = result.scalar_one_or_none()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    if not feedback.structured_feedback:
        raise HTTPException(status_code=404, detail="Structured feedback not available")
    
    return {
        "submission_id": submission_id,
        "feedback_id": feedback.id,
        "structured_feedback": feedback.structured_feedback,
        "overall_performance": feedback.overall_performance,
        "total_score": feedback.total_score,
        "score_breakdown": {
            "content_alignment": feedback.content_alignment_score,
            "scenario_appropriateness": feedback.scenario_appropriateness_score,
            "communication_clarity": feedback.communication_clarity_score,
            "audio_delivery": feedback.audio_delivery_score
        },
        "created_at": feedback.created_at
    }