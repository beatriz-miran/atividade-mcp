"""Verifica o protocolo MCP sem alterar os chamados."""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def extrair_dados(resultado):
    if resultado.structuredContent is not None:
        dados = resultado.structuredContent
        if set(dados) == {"result"}:
            return dados["result"]
        return dados

    textos = [
        json.loads(item.text)
        for item in resultado.content
        if hasattr(item, "text")
    ]

    return textos[0] if len(textos) == 1 else textos


async def testar_tool(session, nome, argumentos, espera_erro=False):
    print(f"\nTESTE: {nome} {argumentos}")

    resultado = await session.call_tool(
        nome,
        arguments=argumentos,
    )

    for item in resultado.content:
        if hasattr(item, "text"):
            print(item.text)

    assert resultado.isError == espera_erro, (
        f"Resultado inesperado em {nome}: "
        f"isError={resultado.isError}"
    )

    print("APROVADO: indicador de erro conforme esperado.")

    return resultado


async def main():
    parametros = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).with_name("server.py").resolve())],
    )

    async with stdio_client(parametros) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as session:
            await session.initialize()

            tools = await session.list_tools()
            resources = await session.list_resources()
            prompts = await session.list_prompts()

            nomes = {tool.name for tool in tools.tools}
            uris = {str(resource.uri) for resource in resources.resources}
            nomes_prompts = {prompt.name for prompt in prompts.prompts}

            print("Tools:", sorted(nomes))
            print("Resources:", sorted(uris))
            print("Prompts:", sorted(nomes_prompts))

            assert {
                "consultar_chamado",
                "listar_chamados",
                "filtrar_chamados",
                "fechar_chamado",
            } <= nomes

            assert {
                "suporte://politica",
                "suporte://chamados",
            } <= uris

            assert "analisar_chamado" in nomes_prompts
            print("APROVADO: inicialização e descoberta.")

            resource = await session.read_resource("suporte://chamados")
            registros = json.loads(resource.contents[0].text)

            politica = await session.read_resource("suporte://politica")
            assert politica.contents[0].text
            print("\nPOLÍTICA:", politica.contents[0].text)
            print("APROVADO: leitura das Resources.")

            resultado = await testar_tool(
                session, "consultar_chamado", {"id": 101}
            )
            chamado = extrair_dados(resultado)

            assert chamado["id"] == 101
            assert chamado["titulo"] == "Falha no login"
            assert chamado["prioridade"] == "alta"
            assert chamado["status"] in {"aberto", "fechado"}
            assert chamado == next(
                c for c in registros if c["id"] == 101
            )
            print("APROVADO: dados do chamado 101.")

            resultado = await testar_tool(
                session, "listar_chamados", {}
            )
            assert extrair_dados(resultado) == registros
            print("APROVADO: listagem completa.")

            for prioridade in ("alta", "media", "baixa"):
                resultado = await testar_tool(
                    session,
                    "filtrar_chamados",
                    {"prioridade": prioridade},
                )
                esperado = [
                    c for c in registros
                    if c["prioridade"] == prioridade
                ]
                assert extrair_dados(resultado) == esperado
                print(f"APROVADO: filtro {prioridade}.")

            casos_invalidos = [
                ("consultar_chamado", {"id": 999}),
                ("consultar_chamado", {"id": -1}),
                ("consultar_chamado", {"id": "abc"}),
                ("filtrar_chamados", {"prioridade": "urgente"}),
                ("listar_chamados", {"status": "urgente"}),
            ]

            for nome, argumentos in casos_invalidos:
                await testar_tool(
                    session,
                    nome,
                    argumentos,
                    espera_erro=True,
                )

            prompt = await session.get_prompt(
                "analisar_chamado",
                arguments={"id": "101"},
            )
            assert prompt.messages
            assert "101" in prompt.messages[0].content.text
            print("\nPROMPT:", prompt.messages[0].content.text)
            print("APROVADO: obtenção do Prompt.")

            depois = await session.read_resource("suporte://chamados")
            assert json.loads(depois.contents[0].text) == registros
            print("APROVADO: registros permaneceram iguais.")

            print("\nTODOS OS TESTES DE LEITURA PASSARAM.")


if __name__ == "__main__":
    print("Iniciando verificação MCP...")
    asyncio.run(main())