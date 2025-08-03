from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_payload
from app.core.database import get_session
from app.models.submission import Submission as SubmissionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any
import uuid

status_router = APIRouter()

@status_router.get("/submission/{submission_id}/status")
async def get_submission_status(
    submission_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    auth_payload: Dict[str, Any] = Depends(get_payload)
):
    """Get the processing status of a submission"""
    stmt = select(SubmissionModel).where(SubmissionModel.id == submission_id)
    result = await session.execute(stmt)
    submission = result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return {
        "submission_id": submission.id,
        "status": submission.processing_status,
        "has_transcription": bool(submission.transcription),
        "has_audio_metrics": bool(submission.audio_metrics),
        "created_at": submission.created_at
    }

@status_router.get("/submissions/stats/{scenario_id}")
async def get_scenario_stats(
    scenario_id: uuid.UUID,
    session: AsyncSession = Depends(get_session), 
    auth_payload: Dict[str, Any] = Depends(get_payload)
):
    """Get statistics for submissions in a scenario"""
    
    # Count submissions by status
    status_counts = await session.execute(
        select(
            SubmissionModel.processing_status,
            func.count(SubmissionModel.id)
        ).where(
            SubmissionModel.scenario_id == scenario_id
        ).group_by(SubmissionModel.processing_status)
    )
    
    status_dict = {status: count for status, count in status_counts.fetchall()}
    
    # Get average processing time for completed submissions
    completed_submissions = await session.execute(
        select(SubmissionModel).where(
            SubmissionModel.scenario_id == scenario_id,
            SubmissionModel.processing_status == "completed"
        )
    )
    
    submissions = completed_submissions.scalars().all()
    
    total_submissions = len(submissions)
    avg_audio_score = None
    
    if submissions:
        scores = []
        for sub in submissions:
            if sub.audio_metrics and 'overall_score' in sub.audio_metrics:
                scores.append(sub.audio_metrics['overall_score'])
        
        if scores:
            avg_audio_score = sum(scores) / len(scores)
    
    return {
        "scenario_id": scenario_id,
        "total_submissions": total_submissions,
        "status_breakdown": status_dict,
        "average_audio_score": round(avg_audio_score, 2) if avg_audio_score else None
    }