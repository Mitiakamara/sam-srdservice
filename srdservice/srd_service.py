import os
import json
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv

# In-memory store
_SRD: Dict[str, Any] = {}
_ADMIN_ID: Optional[int] = None

def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def init_srd_service(base_path: str) -> None:
    """Load all SRD JSONs into memory on startup."""
    global _SRD, _ADMIN_ID
    load_dotenv()
    _ADMIN_ID = None
    admin_env = os.getenv("ADMIN_TELEGRAM_ID")
    if admin_env:
        try:
            _ADMIN_ID = int(admin_env)
        except ValueError:
            _ADMIN_ID = None

    files = {
        "attributes": "attributes.json",
        "skills": "skills.json",
        "conditions": "conditions.json",
        "classes": "classes.json",
        "races": "races.json",
        "spells": "spells.json",
        "equipment": "equipment.json",
        "monsters": "monsters_srd.json",
        "license": "license.json"
    }
    loaded = {}
    for key, fname in files.items():
        fpath = os.path.join(base_path, fname)
        loaded[key] = _load_json(fpath)
    _SRD = loaded

def _ensure_loaded():
    if not _SRD:
        raise HTTPException(status_code=503, detail="SRD not loaded")

class SearchResult(BaseModel):
    name: str
    data: Dict[str, Any]

def _search_dict(d: Dict[str, Any], q: str) -> List[SearchResult]:
    ql = q.lower()
    results: List[SearchResult] = []
    for k, v in d.items():
        if ql in k.lower() or (isinstance(v, dict) and any(ql in str(val).lower() for val in v.values())):
            results.append(SearchResult(name=k, data=v))
    return results

def get_health_router() -> APIRouter:
    r = APIRouter()
    @r.get("/health")
    def health():
        status = "ready" if bool(_SRD) else "cold"
        return {"status": status, "loaded_keys": list(_SRD.keys()) if _SRD else []}
    return r

def get_router() -> APIRouter:
    router = APIRouter()

    @router.get("/attributes")
    def attributes():
        _ensure_loaded()
        return _SRD["attributes"]

    @router.get("/skills")
    def skills():
        _ensure_loaded()
        return _SRD["skills"]

    @router.get("/conditions")
    def conditions():
        _ensure_loaded()
        return _SRD["conditions"]

    @router.get("/classes")
    def classes():
        _ensure_loaded()
        return _SRD["classes"]

    @router.get("/races")
    def races():
        _ensure_loaded()
        return _SRD["races"]

    @router.get("/spells")
    def spells(q: Optional[str] = Query(default=None, description="Full-text query by name or fields")):
        _ensure_loaded()
        data = _SRD["spells"]
        if not q:
            return data
        return {"results": [s.model_dump() for s in _search_dict(data, q)]}

    @router.get("/spells/{name}")
    def spell_by_name(name: str):
        _ensure_loaded()
        data = _SRD["spells"]
        if name in data:
            return data[name]
        for k in data.keys():
            if k.lower() == name.lower():
                return data[k]
        raise HTTPException(status_code=404, detail="Spell not found")

    @router.get("/equipment")
    def equipment():
        _ensure_loaded()
        return _SRD["equipment"]

    @router.get("/monsters")
    def monsters(q: Optional[str] = Query(default=None, description="Full-text query by name or fields")):
        _ensure_loaded()
        data = _SRD["monsters"]
        if not q:
            return data
        return {"results": [s.model_dump() for s in _search_dict(data, q)]}

    @router.get("/monsters/{name}")
    def monster_by_name(name: str):
        _ensure_loaded()
        data = _SRD["monsters"]
        if name in data:
            return data[name]
        for k in data.keys():
            if k.lower() == name.lower():
                return data[k]
        raise HTTPException(status_code=404, detail="Monster not found")

    return router
    from pydantic import BaseModel
from encounter_engine import generate_encounter

class EncounterRequest(BaseModel):
    party_levels: list[int]
    difficulty: str = "medium"

@router.post("/encounter")
def encounter(req: EncounterRequest):
    _ensure_loaded()
    monsters = _SRD["monsters"]
    result = generate_encounter(req.party_levels, monsters, req.difficulty)
    return result
