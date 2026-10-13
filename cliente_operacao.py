"""Cliente MCP para fechar chamados com confirmação prévia."""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def executar_fechamento(id_chamado: int) -> int:
    servidor = Path(__file__).with_name("server.py").resolve()

    parametros = StdioServerParameters(
        command=sys.executable,
        args=[str(servidor)],
    )

    async with stdio_client(parametros) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as session:
            await session.initialize()

            resultado = await session.call_tool(
                "fechar_chamado",
                arguments={"id": id_chamado},
            )

            for item in resultado.content:
                if hasattr(item, "text"):
                    print(item.text)

            return 1 if resultado.isError else 0


def main() -> int:
    try:
        id_chamado = int(
            input("ID do chamado que deseja fechar: ").strip()
        )
    except ValueError:
        print("ID inválido. Informe um número inteiro positivo.")
        return 1

    if id_chamado <= 0:
        print("ID inválido. Informe um número inteiro positivo.")
        return 1

    confirmacao = input(
        f"Confirma fechar o chamado {id_chamado}? "
        "Digite sim para confirmar: "
    ).strip().lower()

    if confirmacao != "sim":
        print(
            "Operação cancelada. "
            "Nenhuma chamada de escrita foi enviada."
        )
        return 0

    return asyncio.run(executar_fechamento(id_chamado))


if __name__ == "__main__":
    raise SystemExit(main())