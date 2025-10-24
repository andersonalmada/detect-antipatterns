from fastapi import APIRouter
from .endpoints import detectors, sources, runs

router = APIRouter(prefix='/api/v1')
router.include_router(sources.router, prefix='/sources', tags=['sources'])
router.include_router(detectors.router, prefix='/detectors', tags=['detectors'])
router.include_router(runs.router, prefix='/runs', tags=['runs'])
