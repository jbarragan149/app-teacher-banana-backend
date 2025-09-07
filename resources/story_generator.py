import os
import base64
import mimetypes
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class StoryGenerator:
    def __init__(self):
        """Inicializar el generador de historias con la API de Gemini"""
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY no encontrada en las variables de entorno")
        
        genai.configure(api_key=self.api_key)
        self.model_text = genai.GenerativeModel("gemini-1.5-flash")
        self.model_image = genai.GenerativeModel("gemini-1.5-flash")
        
        # Crear directorio para imágenes si no existe
        os.makedirs("generated_images", exist_ok=True)
    
    def generate_story_scenes(self, story_prompt: str, num_scenes: int) -> str:
        """
        Generar escenas de una historia usando Gemini
        
        Args:
            story_prompt: El prompt de la historia
            num_scenes: Número de escenas a generar
            
        Returns:
            Texto con las escenas generadas
        """
        prompt = (
            f"Break this story into {num_scenes} short scenes.\n"
            "For each scene, provide:\n"
            "1. title\n"
            "2. a short description\n"
            "3. storytelling suitable for generating creative images\n\n"
            f"Story: {story_prompt}"
        )

        response = self.model_text.generate_content(prompt)
        return response.text
    
    def parse_story_scenes(self, text: str) -> List[Dict[str, str]]:
        """
        Parsear el texto de escenas en un formato estructurado
        
        Args:
            text: Texto con las escenas generadas
            
        Returns:
            Lista de diccionarios con las escenas parseadas
        """
        scenes = []
        raw_scenes = [s.strip() for s in text.split("### Scene") if s.strip()]

        for raw_scene in raw_scenes:
            lines = [line.strip() for line in raw_scene.split("\n") if line.strip()]
            if not lines:
                continue

            first_line = lines[0]
            if ":" in first_line:
                _, title = first_line.split(":", 1)
                title = title.strip()
            else:
                title = first_line.strip()

            description = ""
            storytelling = ""
            capture_story = False

            for line in lines[1:]:
                if line.startswith("**Description:**"):
                    description = line.replace("**Description:**", "").strip()
                elif line.startswith("**Storytelling for Creative Images:**"):
                    storytelling = line.replace("**Storytelling for Creative Images:**", "").strip()
                    capture_story = True
                elif capture_story:
                    storytelling += " " + line

            storytelling = storytelling.replace("---", "").strip()

            if title or description or storytelling:
                scenes.append({
                    "title": title or "Untitled Scene",
                    "description": description,
                    "storytelling": storytelling,
                })

        return scenes
    
    def generate_scene_images(self, scenes: List[Dict[str, str]]) -> None:
        """
        Generar descripciones detalladas para las escenas (placeholder para futura integración con generación de imágenes)
        
        Args:
            scenes: Lista de escenas con información de storytelling
        """
        for idx, scene in enumerate(scenes, 1):
            print(f"\n=== {scene['title']} ===")
            print(scene['storytelling'], "\n")
            
            # Generar descripción detallada para la imagen
            image_prompt = f"Create a detailed visual description for this scene: {scene['storytelling']}"
            response = self.model_image.generate_content(image_prompt)
            
            # Guardar descripción como archivo de texto
            file_name = f"generated_images/scene_{idx}_description.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(f"Scene: {scene['title']}\n")
                f.write(f"Original storytelling: {scene['storytelling']}\n")
                f.write(f"Detailed visual description: {response.text}\n")
            
            print(f"Visual description saved to: {file_name}")
    
    def _save_binary_file(self, file_name: str, data: bytes) -> None:
        """Guardar archivo binario"""
        with open(file_name, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_name}")
