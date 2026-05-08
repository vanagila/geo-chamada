from app.models.Presenca import Presenca
from app.schemas.presenca import PresencaResponse

def presenca_to_response(p: Presenca) -> PresencaResponse:
    dentro_raio = (
        p.distancia_calculada is not None and
        p.chamada is not None and
        p.distancia_calculada <= p.chamada.raio
    )
    return PresencaResponse(
        id=p.id,
        aluno_id=p.aluno_id,
        chamada_id=p.chamada_id,
        distancia_calculada=p.distancia_calculada,
        data_registro=p.data_registro,
        status=p.status,
        dentro_raio=dentro_raio
    )
