from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from resources import StoryGenerator
from models import StoryRequest, SceneResponse, StoryResponse, ImageGenerationRequest, ImageResponse
import uvicorn

# Cargar variables de entorno
load_dotenv()

# Crear la instancia de FastAPI
app = FastAPI(
    title="Story Generator API",
    description="API para generar historias con imágenes usando Gemini AI",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar el generador de historias
try:
    story_generator = StoryGenerator()
    print("Story Generator initialized successfully!")
except Exception as e:
    print(f"Error initializing Story Generator: {e}")
    story_generator = None

@app.get("/")
async def root():
    """Endpoint raíz"""
    print("Story Generator API is running!")
    return {
        "message": "Story Generator API", 
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "generate_story": "/generate-story",
            "generate_scenes": "/generate-scenes", 
            "generate_images": "/generate-images",
            "docs": "/docs"
        }
    }

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """Generar una historia completa con escenas e imágenes"""
    if not story_generator:
        raise HTTPException(status_code=500, detail="Story Generator not initialized. Check API_KEY.")
    
    try:
        print(f"Generating story: {request.story_prompt}")
        
        # Generar escenas
        scenes_text = story_generator.generate_story_scenes(
            request.story_prompt, 
            request.num_scenes
        )
        
        # Parsear escenas
        scenes = story_generator.parse_story_scenes(scenes_text)
        
        # Generar imágenes si se solicita
        if request.generate_images:
            story_generator.generate_scene_images(scenes)
        
        return StoryResponse(
            story_prompt=request.story_prompt,
            num_scenes=request.num_scenes,
            scenes=scenes,
            scenes_text=scenes_text,
            images_generated=request.generate_images
        )
        
    except Exception as e:
        print(f"Error generating story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

@app.post("/generate-scenes", response_model=SceneResponse)
async def generate_scenes(request: StoryRequest):
    """Generar solo las escenas de una historia"""
    if not story_generator:
        raise HTTPException(status_code=500, detail="Story Generator not initialized. Check API_KEY.")
    
    try:
        print(f"Generating scenes for: {request.story_prompt}")
        
        scenes_text = story_generator.generate_story_scenes(
            request.story_prompt, 
            request.num_scenes
        )
        
        scenes = story_generator.parse_story_scenes(scenes_text)
        
        return SceneResponse(
            story_prompt=request.story_prompt,
            num_scenes=request.num_scenes,
            scenes=scenes,
            scenes_text=scenes_text
        )
        
    except Exception as e:
        print(f"Error generating scenes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating scenes: {str(e)}")

@app.post("/generate-images", response_model=ImageResponse)
async def generate_images(request: ImageGenerationRequest):
    """Generar imágenes para escenas existentes"""
    if not story_generator:
        raise HTTPException(status_code=500, detail="Story Generator not initialized. Check API_KEY.")
    
    try:
        print(f"Generating images for {len(request.scenes)} scenes")
        
        # Convertir modelos Pydantic a diccionarios
        scenes_dict = [scene.dict() for scene in request.scenes]
        
        story_generator.generate_scene_images(scenes_dict)
        
        return ImageResponse(
            message="Images generated successfully",
            scenes_count=len(request.scenes),
            images_saved=True
        )
        
    except Exception as e:
        print(f"Error generating images: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating images: {str(e)}")

@app.get("/images/{filename}")
async def get_image(filename: str):
    """Obtener una imagen generada"""
    file_path = f"generated_images/{filename}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "story_generator": "initialized" if story_generator else "not_initialized"
    }

if __name__ == "__main__":
    print("Starting Story Generator API...")
    print("Hello world - API is starting!")
    uvicorn.run(app, host="0.0.0.0", port=8080)
