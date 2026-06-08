from app.models.Presenca import Presenca
from app.schemas.presenca import PresencaRelatorioResponse, AlunoRelatorio

def presenca_to_relatorio_response(p: Presenca) -> PresencaRelatorioResponse:
    dentro_raio = (
        p.distancia_calculada is not None and
        p.chamada is not None and
        p.distancia_calculada <= p.chamada.raio
    )
    return PresencaRelatorioResponse(
        id=p.id,
        aluno=AlunoRelatorio(
            id=p.aluno.id,
            nome=p.aluno.nome,
            email=p.aluno.email,
            matricula=p.aluno.matricula
        ),
        chamada_id=p.chamada_id,
        distancia_calculada=p.distancia_calculada,
        data_registro=p.data_registro,
        status=p.status,
        dentro_raio=dentro_raio
    )
