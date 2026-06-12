from pydantic import BaseModel, field_validator
from typing import Optional
import re


class EmployeeBase(BaseModel):
    name: str
    access_id: Optional[str] = None
    area: str
    position: str
    entry_hour: str

    @field_validator("name", "area", "position")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Este campo no puede estar vacío")
        if len(v) > 100:
            raise ValueError("Máximo 100 caracteres")
        return v

    @field_validator("entry_hour")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not re.match(r"^\d{2}:\d{2}$", v):
            raise ValueError("Formato de hora inválido. Usa HH:MM")
        h, m = int(v[:2]), int(v[3:])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("Hora fuera de rango")
        return v

    @field_validator("access_id")
    @classmethod
    def validate_access_id(cls, v: Optional[str]) -> Optional[str]:
        if v:
            v = v.strip()
            if len(v) > 50:
                raise ValueError("Access ID: máximo 50 caracteres")
            return v or None
        return None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    access_id: Optional[str] = None
    area: Optional[str] = None
    position: Optional[str] = None
    entry_hour: Optional[str] = None

    @field_validator("name", "area", "position")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Este campo no puede estar vacío")
        if len(v) > 100:
            raise ValueError("Máximo 100 caracteres")
        return v

    @field_validator("entry_hour")
    @classmethod
    def validate_time(cls, v: str) -> str:
        if v is None:
            return v
        if not re.match(r"^\d{2}:\d{2}$", v):
            raise ValueError("Formato de hora inválido. Usa HH:MM")
        h, m = int(v[:2]), int(v[3:])
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError("Hora fuera de rango")
        return v

    @field_validator("access_id")
    @classmethod
    def validate_access_id(cls, v: Optional[str]) -> Optional[str]:
        if v:
            v = v.strip()
            if len(v) > 50:
                raise ValueError("Access ID: máximo 50 caracteres")
            return v or None
        return None


class EmployeeResponse(EmployeeBase):
    id: int
    active: bool

    class Config:
        from_attributes = True
