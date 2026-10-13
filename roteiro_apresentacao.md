# Roteiro de apresentação — aproximadamente 7 minutos e 30 segundos

## Preparação

- Testar o projeto no computador da apresentação.
- Deixar o Claude Desktop configurado e conectado ao suporte-ads.
- Deixar disponíveis o código, o JSON, os resultados e as capturas.
- Para demonstrar a mudança de aberto para fechado, encerrar os processos que usam o servidor e ajustar previamente o status do chamado 101 para aberto no JSON.
- Reabrir o Claude após essa preparação.
- Dividir a explicação entre as integrantes. Cada uma deve explicar uma parte do código e responder a uma pergunta técnica.

## 1. Problema e objetivo — 45 segundos

Explicar:

“Um modelo isolado não conhece necessariamente os registros atuais dos chamados. Implementamos um servidor MCP para disponibilizar dados fictícios de forma padronizada, permitindo consultar, filtrar e fechar chamados.”

Destacar que o projeto possui persistência em JSON, validação e confirmação antes do fechamento pelo cliente de operação.

## 2. Arquitetura — 45 segundos

Mostrar o diagrama do relatório:

Usuário → Claude Desktop → Cliente MCP → Servidor Python → JSON.

Explicar:

- O host oferece a interação com a LLM e mantém um cliente MCP.
- O cliente inicia o servidor e se comunica por stdio.
- O servidor executa as funções e acessa o JSON autorizado.
- O SDK gerencia as mensagens JSON-RPC e a sessão.
- Os clientes Python de terminal fazem chamadas determinadas pelo código, sem LLM.

## 3. Capacidades e testes de leitura — 1 minuto

Executar:

```powershell
.\.venv\Scripts\python.exe test_client.py
```

Mostrar:

- Resources suporte://politica e suporte://chamados;
- Tools consultar_chamado, listar_chamados, filtrar_chamados e fechar_chamado;
- Prompt analisar_chamado;
- consulta ao chamado 101;
- filtro alta, retornando 101 e 104;
- rejeição de ID inexistente, ID negativo, texto e filtros inválidos;
- mensagem final de testes aprovados.

Explicar que o Prompt fornece instruções; ele não executa sozinho uma consulta nem substitui a LLM.

## 4. Confirmação, fechamento e persistência — 2 minutos

Executar:

```powershell
.\.venv\Scripts\python.exe cliente_operacao.py
```

Informar 101 e responder nao.

Mostrar o cancelamento e explicar que o cliente retorna antes da conexão MCP.

Executar novamente, informar 101 e responder sim.

Mostrar alterado=true e status fechado no JSON.

Executar novamente:

```powershell
.\.venv\Scripts\python.exe test_client.py
```

Mostrar que um novo processo continua consultando 101 como fechado.

Repetir o fechamento pelo cliente de operação.

Mostrar alterado=false e a mensagem de chamado já fechado.

## 5. Integração com IA — 2 minutos

No Claude Desktop, realizar ou mostrar os três testes já executados:

1. Consultar o chamado 101 usando consultar_chamado.
2. Consultar o chamado 999 e informar a ausência.
3. Listar os chamados e identificar os de prioridade alta.

Mostrar nos detalhes:

- nome da ferramenta;
- argumentos;
- retorno ou erro;
- resposta final da IA.

Comparar a resposta textual com o resultado da ferramenta. Mostrar que o Claude informou corretamente a ausência de 999 e identificou 101 e 104 como prioridade alta.

Autorizar as chamadas individualmente. O fechamento no host deve exigir aprovação individual ou permanecer desabilitado, sendo demonstrado pelo cliente de operação.

## 6. Segurança, logs e conclusão — 1 minuto

Mostrar um log de sucesso e um de erro, identificando timestamp, operação, ID e resultado.

Explicar:

- stdout é reservado ao protocolo; logs vão para stderr;
- o caminho do JSON é fixo e baseado em __file__;
- não há ferramentas para shell, SQL livre ou caminhos arbitrários;
- confirmação no cliente não é autenticação no servidor;
- o projeto não implementa controle de concorrência ou transações.

Concluir:

“Os testes demonstraram o funcionamento do protocolo, a persistência do fechamento e a IA utilizando os retornos das ferramentas para responder. O projeto tem escopo local e precisaria de controles adicionais para uso por múltiplos usuários.”