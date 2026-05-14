from geoalchemy2.shape import to_shape
from app.models.Chamada import Chamada
from app.schemas.chamada import ChamadaResponse, Coordenadas

def chamada_to_response(c: Chamada) -> ChamadaResponse: 
    if not c.coordenadas_professor:
        lat, lon = 0.0, 0.0
    else:
        ponto_geom = to_shape(c.coordenadas_professor)
        lat, lon = ponto_geom.y, ponto_geom.x
    return ChamadaResponse(
        id=c.id,
        turma_id=c.turma_id,
        professor_id=c.professor_id,
        raio=c.raio,
        data_abertura=c.data_abertura,
        data_encerramento=c.data_encerramento,
        status=c.status,
        coordenadas_professor=Coordenadas(
            latitude=ponto_geom.y,
            longitude=ponto_geom.x
        )
    )
