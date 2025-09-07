# 🚀 Story Generator API

Una API profesional para generar historias con imágenes usando Gemini AI, construida con FastAPI.

## ✨ Características

- **Generación de historias**: Crea historias estructuradas con múltiples escenas
- **Generación de imágenes**: Genera imágenes creativas para cada escena usando Gemini AI
- **API RESTful**: Endpoints bien documentados con Swagger UI
- **Dockerizado**: Fácil despliegue con Docker y Docker Compose
- **Variables de entorno**: Configuración segura con archivos .env
- **Manejo de errores**: Respuestas de error detalladas y logging

## 🏗️ Estructura del Proyecto

```
fast-api/
├── main.py                 # API principal con FastAPI
├── story_generator.py      # Lógica de generación con Gemini
├── models.py              # Modelos Pydantic para validación
├── requirements.txt       # Dependencias de Python
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml    # Orquestación de contenedores
├── env.example           # Ejemplo de variables de entorno
├── generated_images/     # Directorio para imágenes generadas
└── README.md            # Este archivo
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd fast-api
```

### 2. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp env.example .env

# Editar el archivo .env y agregar tu API key de Gemini
API_KEY=tu_api_key_de_gemini_aqui
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

#### Opción A: Ejecución directa
```bash
python main.py
```

#### Opción B: Con uvicorn (recomendado para desarrollo)
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

#### Opción C: Con Docker
```bash
# Construir la imagen
docker build -t story-generator-api .

# Ejecutar el contenedor
docker run -p 8080:8080 --env-file .env story-generator-api
```

#### Opción D: Con Docker Compose
```bash
docker-compose up --build
```

## 📡 Endpoints de la API

### Base URL
```
http://localhost:8080
```

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| POST | `/generate-story` | Generar historia completa con imágenes |
| POST | `/generate-scenes` | Generar solo las escenas |
| POST | `/generate-images` | Generar imágenes para escenas existentes |
| GET | `/images/{filename}` | Obtener imagen generada |
| GET | `/docs` | Documentación interactiva (Swagger) |

## 🔧 Uso de la API

### 1. Generar Historia Completa

```bash
curl -X POST "http://localhost:8080/generate-story" \
  -H "Content-Type: application/json" \
  -d '{
    "story_prompt": "Una aventura en el espacio con robots y alienígenas",
    "num_scenes": 3,
    "generate_images": true
  }'
```

### 2. Generar Solo Escenas

```bash
curl -X POST "http://localhost:8080/generate-scenes" \
  -H "Content-Type: application/json" \
  -d '{
    "story_prompt": "Un misterio en una mansión embrujada",
    "num_scenes": 4,
    "generate_images": false
  }'
```

### 3. Generar Imágenes para Escenas Existentes

```bash
curl -X POST "http://localhost:8080/generate-images" \
  -H "Content-Type: application/json" \
  -d '{
    "scenes": [
      {
        "title": "La llegada",
        "description": "El protagonista llega a la mansión",
        "storytelling": "Una figura solitaria se acerca a una mansión gótica..."
      }
    ]
  }'
```

### 4. Obtener Imagen Generada

```bash
curl "http://localhost:8080/images/scene_1_0.png"
```

## 📊 Respuestas de la API

### Respuesta de Historia Completa
```json
{
  "story_prompt": "Una aventura en el espacio",
  "num_scenes": 3,
  "scenes": [
    {
      "title": "El Despegue",
      "description": "La nave espacial despega hacia el espacio",
      "storytelling": "Una nave espacial brillante despega..."
    }
  ],
  "scenes_text": "### Scene 1: El Despegue...",
  "images_generated": true
}
```

## 🐳 Docker

### Construir imagen
```bash
docker build -t story-generator-api .
```

### Ejecutar contenedor
```bash
docker run -p 8080:8080 --env-file .env story-generator-api
```

### Con Docker Compose
```bash
docker-compose up --build
```

## 🔧 Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `API_KEY` | API Key de Google Gemini | ✅ |
| `HOST` | Host del servidor | ❌ (default: 0.0.0.0) |
| `PORT` | Puerto del servidor | ❌ (default: 8080) |
| `DEBUG` | Modo debug | ❌ (default: True) |

## 🛠️ Desarrollo

### Estructura del Código

- **`main.py`**: Configuración de FastAPI, endpoints y middleware
- **`story_generator.py`**: Clase principal para interactuar con Gemini AI
- **`models.py`**: Modelos Pydantic para validación de datos
- **`generated_images/`**: Directorio donde se guardan las imágenes generadas

### Agregar Nuevas Funcionalidades

1. **Nuevos endpoints**: Agregar en `main.py`
2. **Nuevos modelos**: Definir en `models.py`
3. **Nueva lógica de negocio**: Implementar en `story_generator.py`

## 📝 Logs

La aplicación genera logs detallados en la consola:
- Inicialización del generador de historias
- Procesamiento de solicitudes
- Generación de escenas e imágenes
- Errores y excepciones

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación en `/docs`
2. Verifica que tu API_KEY esté configurada correctamente
3. Revisa los logs de la aplicación
4. Abre un issue en GitHub

---

¡Disfruta generando historias increíbles! 🎨✨
