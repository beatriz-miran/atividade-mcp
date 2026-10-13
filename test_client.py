"""Cliente de teste MCP: inicializa o servidor e testa descoberta e chamadas."""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_file = Path(__file__).with_name("server.py").resolve()
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_file)],
        env=None,
    )

    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            resources = await session.list_resources()
            prompts = await session.list_prompts()

            print("=== DESCOBERTA MCP ===")
            print("Tools:", [tool.name for tool in tools.tools])
            print("Resources:", [resource.uri for resource in resources.resources])
            print("Prompts:", [prompt.name for prompt in prompts.prompts])

            print("\n=== CHAMADA: consultar_chamado(101) ===")
            result = await session.call_tool(
                "consultar_chamado", arguments={"id": 101}
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)
            print("isError:", result.isError)

            print("\n=== CHAMADA: listar_chamados(prioridade='alta') ===")
            result = await session.call_tool(
                "listar_chamados", arguments={"prioridade": "alta"}
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)
            print("isError:", result.isError)

            print("\n=== LEITURA DA RESOURCE ===")
            resource_result = await session.read_resource("suporte://chamados")
            for item in resource_result.contents:
                if hasattr(item, "text"):
                    print(item.text)

            print("\n=== ERRO ESPERADO: chamado inexistente ===")
            result = await session.call_tool(
                "consultar_chamado", arguments={"id": 999}
            )
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)
            print("isError:", result.isError)

            print("\n=== PROMPT ===")
            prompt_result = await session.get_prompt(
                "analisar_chamado", arguments={"id": 101}
            )
            for message in prompt_result.messages:
                content = message.content
                if hasattr(content, "text"):
                    print(content.text)


if __name__ == "__main__":
    asyncio.run(main())
