# Assistente de Suporte com MCP

Projeto acadêmico demonstrativo para a atividade prática de ADS. O servidor expõe chamados **fictícios** usando o Model Context Protocol (MCP).

## Requisitos

- Python 3.11 ou superior
- Internet para instalar a dependência
- Terminal (PowerShell no Windows funciona)

## Estrutura

- `server.py`: servidor MCP com uma Resource, duas Tools e um Prompt.
- `test_client.py`: cliente MCP de teste que inicia o servidor por `stdio`, descobre capacidades e faz chamadas.
- `relatorio.md`: modelo de relatório para revisar e adaptar ao que o grupo executar de fato.
- `roteiro_apresentacao.md`: sequência sugerida para a demonstração.

## Instalação no Windows (PowerShell)

```powershell
py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se a ativação for bloqueada pela política do PowerShell, use o terminal CMD e execute:

```bat
.venv\Scripts\activate.bat
```

## Executar os testes de protocolo

Com o ambiente virtual ativado:

```powershell
python test_client.py
```

O cliente inicia o servidor como processo filho usando `stdio`, executa a inicialização MCP, descobre Tools/Resources/Prompts, chama ferramentas e lê a Resource. Não é necessário contratar uma API de LLM.

## Executar o servidor para um host MCP

O servidor normalmente é iniciado pelo host MCP, que configura o comando Python e o caminho absoluto de `server.py`. Para testar separadamente com o MCP Inspector, execute em outro terminal:

```powershell
npx -y @modelcontextprotocol/inspector
```

Configure o comando com o caminho completo para o interpretador `.venv` e o argumento com o caminho completo para `server.py`. O servidor usa `stdio`; não digite perguntas diretamente no terminal do processo servidor.

## Capacidades

- Resource: `suporte://chamados`
- Tool: `consultar_chamado(id)`
- Tool: `listar_chamados(status="", prioridade="")`
- Prompt: `analisar_chamado(id)`

## Segurança e limites

Os registros são constantes em memória; não há acesso a arquivos arbitrários, shell, banco externo ou operações de alteração. As ferramentas validam IDs, status e prioridade. Os logs vão para `stderr`, preservando o canal `stdout` para o protocolo stdio.

## Dados de demonstração

- 101: Sistema fora do ar — prioridade alta — aberto.
- 102: Erro ao gerar relatório — prioridade média — em andamento.
- 103: Solicitação de alteração de senha — prioridade baixa — resolvido.
- 104: Computador sem conexão de rede — prioridade alta — aberto.

## Testes
<img width="978" height="610" alt="image" src="https://github.com/user-attachments/assets/7f39a92b-810c-45d3-9955-ff4f57a16e2a" />

<img width="991" height="680" alt="image" src="https://github.com/user-attachments/assets/4caa2244-c228-4921-b1b0-87f95e6268fd" />

