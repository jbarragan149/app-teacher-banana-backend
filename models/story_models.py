from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class StoryRequest(BaseModel):
    """Modelo para solicitud de generación de historia"""
    story_prompt: str = Field(..., description="El prompt de la historia a generar")
    num_scenes: int = Field(default=3, ge=1, le=10, description="Número de escenas a generar (1-10)")
    generate_images: bool = Field(default=True, description="Si generar imágenes para las escenas")

class Scene(BaseModel):
    """Modelo para una escena individual"""
    title: str = Field(..., description="Título de la escena")
    description: str = Field(..., description="Descripción de la escena")
    storytelling: str = Field(..., description="Texto para generación de imágenes")

class SceneResponse(BaseModel):
    """Respuesta con escenas generadas"""
    story_prompt: str
    num_scenes: int
    scenes: List[Scene]
    scenes_text: str

class StoryResponse(SceneResponse):
    """Respuesta completa con escenas e imágenes"""
    images_generated: bool = Field(..., description="Si las imágenes fueron generadas")

class ImageGenerationRequest(BaseModel):
    """Modelo para solicitud de generación de imágenes"""
    scenes: List[Scene] = Field(..., description="Lista de escenas para generar imágenes")

class ImageResponse(BaseModel):
    """Respuesta de generación de imágenes"""
    message: str
    scenes_count: int
    images_saved: bool
