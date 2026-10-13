# Implementação de MCP em um assistente de suporte

**Curso:** Análise e Desenvolvimento de Sistemas — 6º semestre  
**Integrantes:** [preencher nomes do grupo]  
**Disciplina:** [preencher]  
**Professor(a):** [preencher]  
**Data:** [preencher]

## 1. Introdução

Este trabalho apresenta a implementação de um servidor baseado no Model Context Protocol (MCP) para disponibilizar dados fictícios de chamados de suporte a uma aplicação cliente. A proposta demonstra como um modelo de IA pode consultar informações externas por meio de capacidades padronizadas, reduzindo a dependência de informações memorizadas pelo próprio modelo.

## 2. Objetivo

Desenvolver e testar um servidor MCP em Python que exponha uma Resource, duas Tools e um Prompt, permitindo a consulta controlada de chamados fictícios. Também se busca distinguir uma resposta textual gerada pelo modelo de uma operação efetivamente executada pelo servidor.

## 3. Tecnologias utilizadas

- Python 3.11 ou superior;
- SDK MCP para Python (`mcp`);
- comunicação local pelo transporte `stdio`;
- JSON para representar os registros;
- cliente de teste MCP (`test_client.py`); opcionalmente, MCP Inspector.

## 4. Arquitetura

A aplicação host é responsável pela interação com o usuário e mantém um cliente MCP. O cliente inicia o servidor Python como processo local e troca mensagens por `stdio`. O SDK gerencia o ciclo de vida da sessão e as mensagens do protocolo. O servidor acessa somente os registros fictícios declarados no código.

## 5. Capacidades implementadas

### 5.1 Resource

A URI `suporte://chamados` disponibiliza a coleção dos chamados em formato JSON para leitura pelo cliente MCP.

### 5.2 Tool: `consultar_chamado`

Recebe um ID inteiro positivo e retorna o registro correspondente. IDs inválidos ou inexistentes produzem erro em vez de inventar um chamado.

### 5.3 Tool: `listar_chamados`

Permite listar os registros e aplicar filtros opcionais por status (`aberto`, `em andamento`, `resolvido`) e prioridade (`alta`, `media`, `baixa`). Valores fora dos permitidos são rejeitados.

### 5.4 Prompt: `analisar_chamado`

Gera instruções para que um modelo consulte primeiro os dados atuais, resuma status e prioridade e proponha um próximo passo sem inventar informações.

## 6. Segurança e rastreabilidade

A solução utiliza dados em memória e não permite acesso genérico ao sistema de arquivos, execução de comandos ou alteração dos chamados. Os parâmetros são validados e os eventos de consulta são registrados com o módulo `logging`. Os logs são enviados para `stderr`, evitando misturar mensagens de diagnóstico com o canal de comunicação MCP em `stdout`.

## 7. Plano de testes e resultados

> **Preencher esta seção após executar `python test_client.py`. Não declarar testes como aprovados sem observar a execução.**

| Teste | Entrada | Resultado esperado | Resultado observado |
|---|---|---|---|
| Inicialização | Cliente conecta por stdio | Sessão inicializada | [preencher] |
| Descoberta | Listar capacidades | Resource, 2 Tools e Prompt encontrados | [preencher] |
| Consulta existente | ID 101 | Chamado aberto, prioridade alta | [preencher] |
| Filtro | Prioridade `alta` | Chamados 101 e 104 | [preencher] |
| ID inexistente | ID 999 | Erro controlado | [preencher] |
| Filtro inválido | Status `urgente` | Erro de validação | [preencher] |
| Leitura de Resource | `suporte://chamados` | JSON com os registros fictícios | [preencher] |
| Prompt | ID 101 | Instruções para análise do chamado | [preencher] |

## 8. Resposta do modelo versus operação de ferramenta

Uma resposta textual do modelo, sem consulta, pode estar incorreta ou não refletir o estado atual dos registros. Já uma chamada de Tool é uma operação enviada pelo cliente MCP ao servidor, que executa a função e devolve um resultado. No exemplo, `consultar_chamado(101)` retorna status `aberto` e prioridade `alta`. A ferramenta de consulta não altera os dados; ela apenas lê e devolve o registro.

## 9. Conclusão

O projeto demonstra a separação entre host, cliente e servidor MCP, o uso de `stdio` para comunicação local e a publicação de recursos, ferramentas e prompts. A validação de parâmetros e o escopo restrito aos dados fictícios ajudam a aplicar o princípio do menor privilégio. A execução prática e o registro dos resultados permitem avaliar se a resposta do assistente está fundamentada nos dados retornados pelas ferramentas.

## 10. Evidências

Inserir capturas de tela reais da execução mostrando:
1. descoberta de Tools, Resources e Prompts;
2. retorno de `consultar_chamado(101)`;
3. filtro de prioridade alta;
4. erro de ID inexistente;
5. leitura da Resource e resultado do Prompt.
