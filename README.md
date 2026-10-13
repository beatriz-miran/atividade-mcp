# Assistente de Suporte com MCP

Projeto acadêmico de ADS para consulta, filtragem e fechamento de chamados fictícios usando o Model Context Protocol.

O servidor utiliza transporte local stdio e persiste os registros em dados/chamados.json. A integração com LLM foi demonstrada no Claude Desktop.

## Requisitos

- Python 3.11 ou superior;
- internet para instalar dependências;
- Claude Desktop para reproduzir a demonstração com IA.

Ambiente utilizado nos testes: Windows, Python 3.12.3 e SDK MCP 1.30.0.

## Estrutura

- server.py: servidor MCP;
- test_client.py: testes de leitura, descoberta e entradas inválidas;
- cliente_operacao.py: fechamento com confirmação;
- dados/chamados.json: registros fictícios persistidos;
- requirements.txt: faixa de versões das dependências;
- requirements-lock.txt: versões exatas do ambiente;
- relatorio.md: arquitetura, resultados, segurança e limitações;
- roteiro_apresentacao.md: roteiro da demonstração;
- evidencias/: capturas da execução.

## Instalação no Windows

Abra o PowerShell na pasta do projeto:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Para instalar pela faixa de versões e gerar um novo arquivo de dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip freeze | Set-Content -Encoding utf8 requirements-lock.txt
```

O uso direto do interpretador da .venv dispensa ativar o ambiente.

## Testes de leitura

```powershell
.\.venv\Scripts\python.exe test_client.py
```

O cliente inicia o servidor automaticamente. Verifica:

- inicialização e descoberta;
- leitura das duas Resources;
- consulta ao chamado 101;
- listagem e filtros por prioridade;
- rejeição de ID inexistente, ID negativo e texto inválido;
- rejeição de prioridade e status inválidos;
- obtenção do Prompt;
- preservação dos registros durante os testes de leitura.

Mensagem final esperada:

```text
TODOS OS TESTES DE LEITURA PASSARAM.
```

As mensagens de erro dos casos inválidos são esperadas e verificadas com assert.

## Fechamento com confirmação

```powershell
.\.venv\Scripts\python.exe cliente_operacao.py
```

Informe o ID e responda à confirmação:

- sim: conecta ao servidor e solicita o fechamento;
- qualquer outra resposta: cancela antes da conexão MCP.

Resultados:

- chamado aberto: status fechado salvo no JSON e alterado=true;
- chamado já fechado: alterado=false, sem regravar;
- ID inexistente: erro sem criar registro.

Para verificar persistência, execute test_client.py novamente após o fechamento. O novo processo deve consultar o status fechado.

Os dados mantêm as alterações entre execuções. Se precisar repetir o teste de aberto para fechado, encerre os processos que usam o servidor, edite somente o status de 101 para aberto no JSON e salve.

## Capacidades MCP

### Resources

- suporte://politica: regras de uso e limitações;
- suporte://chamados: registros atuais do JSON.

### Tools

- consultar_chamado(id);
- listar_chamados(status="", prioridade="");
- filtrar_chamados(prioridade);
- fechar_chamado(id).

Prioridades permitidas: alta, media e baixa.
Status permitidos: aberto e fechado.

### Prompt

analisar_chamado(id): instruções para consultar os dados e fundamentar a análise.

Na chamada do Prompt, envie o ID como texto:

```python
arguments={"id": "101"}
```

Nas chamadas das Tools, envie o ID como inteiro:

```python
arguments={"id": 101}
```

## Configuração do Claude Desktop

Instale o aplicativo pelo site oficial: https://claude.com/download

Abra Configurações → Desenvolvedor → Editar configuração.

Acrescente mcpServers como uma propriedade na raiz do JSON, preservando as preferências existentes. Exemplo para a pasta utilizada neste projeto:

```json
{
  "mcpServers": {
    "suporte-ads": {
      "command": "C:/Users/isis0/Downloads/atividade-mcp-main/atividade-mcp-main/.venv/Scripts/python.exe",
      "args": [
        "C:/Users/isis0/Downloads/atividade-mcp-main/atividade-mcp-main/server.py"
      ],
      "env": {
        "PYTHONUTF8": "1"
      }
    }
  }
}
```

Ajuste os caminhos absolutos se executar em outro computador ou pasta. O bloco acima é um exemplo de configuração; mantenha outras propriedades já existentes no arquivo do aplicativo.

Salve a configuração com o Claude completamente encerrado e abra novamente. Em Desenvolvedor, confira se suporte-ads aparece em execução.

Mantenha aprovação individual para ferramentas de escrita ou desabilite fechar_chamado no host e use o cliente de operação para os fechamentos. A confirmação implementada no cliente Python não se aplica automaticamente ao Claude.

Referência oficial: https://modelcontextprotocol.io/docs/develop/connect-local-servers

## Demonstração com IA

Faça três solicitações:

1. Consultar o chamado 101 pela ferramenta e informar título, prioridade e status.
2. Consultar o chamado 999 e informar a ausência sem inventar dados.
3. Listar os chamados e identificar os de prioridade alta.

Confira os detalhes das chamadas: nome da ferramenta, argumentos, resultado e resposta da IA. Durante os testes, as chamadas de leitura foram autorizadas com Permitir uma vez.

O cliente Python de testes não contém uma LLM: suas chamadas são determinadas pelo código.

## Logs

O servidor envia logs para stderr com timestamp, operação, ID quando aplicável e resultado. stdout é reservado ao protocolo MCP.

No Claude Desktop, acesse Desenvolvedor → suporte-ads → Ver registros.

## Segurança e limitações

O servidor acessa somente dados/chamados.json, com caminho calculado a partir de __file__. Não aceita caminhos arbitrários nem expõe shell ou SQL livre.

A confirmação no cliente controla o fluxo de uso, mas não autentica quem acessa o servidor. Outro cliente pode chamar a ferramenta diretamente.

A solução não implementa autorização por usuário, transações, atualização atômica do JSON ou controle de escrita concorrente. Seu escopo é uma demonstração local.

## Evidências e entrega

Os resultados observados estão no relatorio.md. As capturas estão na pasta evidencias.

Inclua na entrega o código, os dados fictícios, requirements-lock.txt, README, relatório e evidências. Exclua .venv, credenciais e dados reais.