# from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.services.ai_service import identify_plant
# import json
# import re
# router = APIRouter()

# @router.post("/identify")
# async def identify(file: UploadFile = File(...), lang: str = "eng"):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")

#     try:
#         image_bytes = await file.read()
#         raw = identify_plant(image_bytes, lang)

#         # Limpieza robusta — elimina cualquier bloque ```json ... ``` o ``` ... ```
#         clean = re.sub(r"```(?:json)?\s*", "", raw).strip() #clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
#         result = json.loads(clean)
#         return {"success": True, "data": result}

#     except json.JSONDecodeError:
#         return {"success": True, "data": {"raw": raw}}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_service import identify_plant
from app.schemas.plant import IdentificationResult
import json
import re

router = APIRouter()

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
        # Esto evita errores de formato en el procesamiento del texto
        clean_json = raw_response.strip()
        
        # Eliminamos el inicio si trae comillas invertidas
        if clean_json.startswith("```"):
            # Buscamos dónde termina la primera línea (ej: ```json)
            first_newline = clean_json.find('\n')
            if first_newline != -1:
                clean_json = clean_json[first_newline:].strip()
            
            # Eliminamos las comillas del final
            if clean_json.endswith("```"):
                clean_json = clean_json[:-3].strip()

        # 4. Parsear a diccionario
        data_dict = json.loads(clean_json)

        # 5. Validar con Pydantic (Aquí se une con tu plant.py)
        # Si la IA no manda un campo obligatorio, esto lanzará un error capturado abajo
        validated_data = IdentificationResult(**data_dict)

        # 6. Respuesta final impecable
        return {
            "success": True,
            "data": validated_data.model_dump()
        }

    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "La IA no devolvió un JSON válido",
            "raw": raw_response
        }
    except Exception as e:
        # Aquí caerá si Pydantic detecta que faltan campos en el JSON
        raise HTTPException(status_code=500, detail=f"Error en procesamiento: {str(e)}")