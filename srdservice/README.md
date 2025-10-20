# S.A.M. – SRDService (FastAPI)

Servicio ligero para cargar y exponer el SRD 5.2.1 Simplificado (JSON) para el backend de S.A.M.

## Estructura
- `main.py` – App FastAPI y bootstrap de SRD.
- `srd_service.py` – Cargador en memoria + endpoints.
- `.env.example` – Variables de entorno.
- `requirements.txt` – Dependencias.

## Variables de entorno
- `SRD_BASE_PATH` – Ruta a la carpeta `/srd` con los JSON (por defecto `./srd`).
- `ADMIN_TELEGRAM_ID` – (Opcional) ID de admin para futuros endpoints protegidos.

## Instalar y ejecutar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # y ajusta SRD_BASE_PATH si es necesario
uvicorn main:app --reload --port 8000
```

## Probar
- Salud: `GET http://localhost:8000/health`
- Atributos: `GET http://localhost:8000/srd/attributes`
- Hechizos (todos): `GET http://localhost:8000/srd/spells`
- Hechizo por nombre: `GET http://localhost:8000/srd/spells/Fire%20Bolt`
- Buscar monstruos: `GET http://localhost:8000/srd/monsters?q=goblin`
(update for render)
