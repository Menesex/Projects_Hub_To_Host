from fastapi import APIRouter, UploadFile, File, HTTPException
from .services import identify_plant
from .schemas import IdentificationResult
import json

router = APIRouter(prefix="/api/plants", tags=["Plant Detection"])


@router.post("/identify")
async def identify(file: UploadFile = File(...), lang: str = "es"):
    # 1. Validar que sea una imagen
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

    try:
        # 2. Leer imagen y llamar al servicio de Groq
        image_bytes = await file.read()
        raw_response = identify_plant(image_bytes, lang)

        # 3. Limpieza manual de bloques Markdown (```json ... ```)
        clean_json = raw_response.strip()

        if clean_json.startswith("```"):
            first_newline = clean_json.find('\n')
            if first_newline != -1:
                clean_json = clean_json[first_newline:].strip()

            if clean_json.endswith("```"):
                clean_json = clean_json[:-3].strip()

        # 4. Parsear a diccionario
        data_dict = json.loads(clean_json)

        # 5. Validar con Pydantic
        validated_data = IdentificationResult(**data_dict)

        # 6. Respuesta final con estructura esperada por frontend
        return {
            "success": True,
            "data": validated_data.model_dump()
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "La IA no devolvió un JSON válido"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error en procesamiento: {str(e)}"
        }
