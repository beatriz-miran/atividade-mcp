"""Servidor MCP para consulta de chamados fictícios."""
import json
import logging
from typing import Any
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from functools import wraps

# O logging vai para stderr para não corromper o protocolo stdio.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("suporte-mcp")

def auditar_ferramenta(funcao):
    """Registra a execução e os erros de uma ferramenta."""
    @wraps(funcao)
    def executar(*args, **kwargs):
        id_chamado = kwargs.get("id")

        try:
            resultado = funcao(*args, **kwargs)
        except Exception as erro:
            logger.warning(
                "operacao=%s id=%r resultado=erro detalhe=%r",
                funcao.__name__,
                id_chamado,
                str(erro),
            )
            raise

        logger.info(
            "operacao=%s id=%r resultado=sucesso",
            funcao.__name__,
            id_chamado,
        )

        return resultado

    return executar

mcp = FastMCP("Assistente de Suporte - Chamados Fictícios")

ARQUIVO_CHAMADOS = (
    Path(__file__).resolve().parent / "dados" / "chamados.json"
)

STATUS_VALIDOS = {"aberto", "fechado"}
PRIORIDADES_VALIDAS = {"alta", "media", "baixa"}


def ler_chamados() -> list[dict[str, Any]]:
    """Lê os chamados somente do arquivo autorizado do projeto."""
    with ARQUIVO_CHAMADOS.open(encoding="utf-8-sig") as arquivo:
        return json.load(arquivo)


def salvar_chamados(chamados: list[dict[str, Any]]) -> None:
    """Salva os chamados somente no arquivo autorizado do projeto."""
    conteudo = json.dumps(
        chamados,
        ensure_ascii=False,
        indent=2,
    )
    ARQUIVO_CHAMADOS.write_text(conteudo, encoding="utf-8")

@mcp.resource("suporte://politica")
def politica() -> str:
    """Apresenta as regras de acesso aos chamados fictícios."""
    return (
        "Use somente os dados fictícios disponíveis no servidor. "
        "Não invente chamados, prioridades ou status. "
        "O servidor acessa somente dados/chamados.json. "
        "O fechamento exige confirmação no cliente ou aprovação no host. "
        "A confirmação no cliente não é autenticação no servidor. "
        "Outro cliente pode chamar a ferramenta diretamente. "
        "O projeto não implementa controle de escrita concorrente."
    )
@mcp.resource("suporte://chamados")
def recurso_chamados() -> str:
    """Retorna a coleção de chamados fictícios disponíveis para consulta."""
    return json.dumps(ler_chamados(), ensure_ascii=False, indent=2)


@mcp.tool()
@auditar_ferramenta
def consultar_chamado(id: int) -> dict[str, Any]:
    """Consulta um chamado pelo ID positivo e retorna seus dados."""
    if isinstance(id, bool) or not isinstance(id, int) or id <= 0:
        raise ValueError("O ID deve ser um número inteiro positivo.")

    for chamado in ler_chamados():
        if chamado["id"] == id:
            logger.info("Consulta executada para chamado id=%s", id)
            return dict(chamado)

    raise ValueError(f"Chamado {id} não encontrado.")


@mcp.tool()
@auditar_ferramenta
def listar_chamados(status: str = "", prioridade: str = "") -> list[dict[str, Any]]:
    """Lista chamados. Filtros opcionais: status e prioridade."""
    if status and status not in STATUS_VALIDOS:
        raise ValueError(
            "Status inválido. Use: aberto ou fechado."
        )
    if prioridade and prioridade not in PRIORIDADES_VALIDAS:
        raise ValueError("Prioridade inválida. Use: alta, media ou baixa.")

    resultado = [
        c for c in ler_chamados()
        if (not status or c["status"] == status)
        and (not prioridade or c["prioridade"] == prioridade)
    ]
    logger.info(
        "Listagem executada: status=%s prioridade=%s resultados=%s",
        status or "todos", prioridade or "todas", len(resultado)
    )
    return [dict(c) for c in resultado]

@mcp.tool()
@auditar_ferramenta
def filtrar_chamados(prioridade: str) -> list[dict[str, Any]]:
    """Filtra chamados por prioridade: alta, media ou baixa."""
    if prioridade not in PRIORIDADES_VALIDAS:
        raise ValueError(
            "Prioridade inválida. Use: alta, media ou baixa."
        )

    resultado = [
        dict(chamado)
        for chamado in ler_chamados()
        if chamado["prioridade"] == prioridade
    ]

    logger.info(
        "Filtro executado: prioridade=%s resultados=%s",
        prioridade,
        len(resultado),
    )

    return resultado

@mcp.tool()
@auditar_ferramenta
def fechar_chamado(id: int) -> dict[str, Any]:
    """Fecha um chamado e persiste o novo status no JSON."""
    if isinstance(id, bool) or not isinstance(id, int) or id <= 0:
        logger.warning(
            "operacao=fechar_chamado id=%s resultado=id_invalido",
            id,
        )
        raise ValueError("O ID deve ser um número inteiro positivo.")

    chamados = ler_chamados()

    for chamado in chamados:
        if chamado["id"] == id:
            if chamado["status"] == "fechado":
                logger.info(
                    "operacao=fechar_chamado id=%s resultado=ja_fechado",
                    id,
                )
                return {
                    "alterado": False,
                    "mensagem": "O chamado já estava fechado.",
                    "chamado": dict(chamado),
                }

            chamado["status"] = "fechado"
            salvar_chamados(chamados)

            logger.info(
                "operacao=fechar_chamado id=%s resultado=fechado",
                id,
            )

            return {
                "alterado": True,
                "mensagem": "Chamado fechado e salvo no JSON.",
                "chamado": dict(chamado),
            }

    logger.warning(
        "operacao=fechar_chamado id=%s resultado=nao_encontrado",
        id,
    )
    raise ValueError(f"Chamado {id} não encontrado.")

@mcp.prompt()
def analisar_chamado(id: int) -> str:
    """Monta instruções para analisar um chamado com base em dados consultados."""
    if isinstance(id, bool) or not isinstance(id, int) or id <= 0:
        raise ValueError("O ID deve ser um número inteiro positivo.")
    if not any(c["id"] == id for c in ler_chamados()):
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
