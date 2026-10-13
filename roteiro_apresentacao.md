# Roteiro de apresentação — 5 minutos

## 1. Problema e objetivo (30 segundos)
“Um modelo de IA isolado não conhece necessariamente o estado atual dos chamados e pode inventar informações. Criamos um servidor MCP para disponibilizar registros fictícios de forma controlada.”

## 2. Arquitetura (45 segundos)
Apontar o `test_client.py` como cliente, `server.py` como servidor e explicar que o cliente inicia o processo Python e usa `stdio`. O SDK gerencia as mensagens MCP/JSON-RPC.

## 3. Descoberta de capacidades (45 segundos)
Executar `python test_client.py` e mostrar a lista de Tools, Resources e Prompts. Identificar:
- Resource `suporte://chamados`;
- Tools `consultar_chamado` e `listar_chamados`;
- Prompt `analisar_chamado`.

## 4. Consultas reais (1 minuto)
Mostrar o retorno da consulta ao chamado 101 e a listagem filtrada pela prioridade `alta`. Explicar que o resultado vem dos dados do servidor.

## 5. Erros e segurança (1 minuto)
Mostrar o teste do ID 999 e explicar a validação dos filtros. Destacar que não há acesso arbitrário a arquivos, execução de comandos ou ferramenta de alteração.

## 6. Modelo versus ferramenta (1 minuto)
Comparar uma resposta sem consulta (“o chamado está em andamento”) com o resultado efetivo da ferramenta, que informa que o chamado 101 está aberto e tem prioridade alta. Explicar que o modelo deve se apoiar no retorno da ferramenta.

## 7. Encerramento (30 segundos)
“Concluímos que o MCP padroniza a comunicação entre a aplicação cliente e o servidor, enquanto as validações e o escopo limitado ajudam a controlar o acesso aos dados.”

## Antes de apresentar
- Executar os testes no computador que será usado.
- Preencher o relatório com os resultados realmente observados.
- Capturar telas da execução real.
- Se usar host com IA, demonstrar a consulta à ferramenta e não apenas uma resposta textual inventada.
