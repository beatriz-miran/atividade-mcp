"""Servidor MCP para consulta de chamados fictícios."""
import json
import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

# O logging vai para stderr para não corromper o protocolo stdio.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("suporte-mcp")

mcp = FastMCP("Assistente de Suporte - Chamados Fictícios")

CHAMADOS: list[dict[str, Any]] = [
    {
        "id": 101,
        "titulo": "Sistema fora do ar",
        "descricao": "Usuários não conseguem acessar o sistema interno.",
        "prioridade": "alta",
        "status": "aberto",
        "solicitante": "Ana",
    },
    {
        "id": 102,
        "titulo": "Erro ao gerar relatório",
        "descricao": "O relatório mensal apresenta erro ao exportar.",
        "prioridade": "media",
        "status": "em andamento",
        "solicitante": "Carlos",
    },
    {
        "id": 103,
        "titulo": "Solicitação de alteração de senha",
        "descricao": "Usuário precisa redefinir a senha de acesso.",
        "prioridade": "baixa",
        "status": "resolvido",
        "solicitante": "Marina",
    },
    {
        "id": 104,
        "titulo": "Computador sem conexão de rede",
        "descricao": "Estação de trabalho não acessa recursos da rede.",
        "prioridade": "alta",
        "status": "aberto",
        "solicitante": "João",
    },
]

STATUS_VALIDOS = {"aberto", "em andamento", "resolvido"}
PRIORIDADES_VALIDAS = {"alta", "media", "baixa"}


@mcp.resource("suporte://chamados")
def recurso_chamados() -> str:
    """Retorna a coleção de chamados fictícios disponíveis para consulta."""
    return json.dumps(CHAMADOS, ensure_ascii=False, indent=2)


@mcp.tool()
def consultar_chamado(id: int) -> dict[str, Any]:
    """Consulta um chamado pelo ID positivo e retorna seus dados."""
    if isinstance(id, bool) or not isinstance(id, int) or id <= 0:
        raise ValueError("O ID deve ser um número inteiro positivo.")

    for chamado in CHAMADOS:
        if chamado["id"] == id:
            logger.info("Consulta executada para chamado id=%s", id)
            return dict(chamado)

    raise ValueError(f"Chamado {id} não encontrado.")


@mcp.tool()
def listar_chamados(status: str = "", prioridade: str = "") -> list[dict[str, Any]]:
    """Lista chamados. Filtros opcionais: status e prioridade."""
    if status and status not in STATUS_VALIDOS:
        raise ValueError(
            "Status inválido. Use: aberto, em andamento ou resolvido."
        )
    if prioridade and prioridade not in PRIORIDADES_VALIDAS:
        raise ValueError("Prioridade inválida. Use: alta, media ou baixa.")

    resultado = [
        c for c in CHAMADOS
        if (not status or c["status"] == status)
        and (not prioridade or c["prioridade"] == prioridade)
    ]
    logger.info(
        "Listagem executada: status=%s prioridade=%s resultados=%s",
        status or "todos", prioridade or "todas", len(resultado)
    )
    return [dict(c) for c in resultado]


@mcp.prompt()
def analisar_chamado(id: int) -> str:
    """Monta instruções para analisar um chamado com base em dados consultados."""
    if isinstance(id, bool) or not isinstance(id, int) or id <= 0:
        raise ValueError("O ID deve ser um número inteiro positivo.")
    if not any(c["id"] == id for c in CHAMADOS):
        raise ValueError(f"Chamado {id} não encontrado.")

    return (
        f"Analise o chamado de ID {id}. Primeiro, use a ferramenta "
        "'consultar_chamado' para obter os dados atuais. Depois, resuma "
        "o título, a prioridade e o status e sugira um próximo passo "
        "proporcional à prioridade. Não invente informações ausentes e "
        "diferencie claramente os dados retornados pelo sistema das suas "
        "sugestões."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
