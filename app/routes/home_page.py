import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Request, Response, status


router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}