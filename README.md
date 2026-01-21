# Observa Framework

O Observa é um framework projetado para apoiar a detecção automática de anti-padrões de observabilidade em aplicações distribuídas. Diferentemente das ferramentas convencionais de observabilidade — tradicionalmente voltadas à coleta, visualização e correlação de sinais — o Observa tem como foco avaliar a qualidade da observabilidade efetivamente implementada, identificando más práticas associadas ao uso de métricas, logs, traces, alertas e dashboards.

Para isso, o framework integra fontes heterogêneas de dados de telemetria e emprega detectores especializados, cada um responsável por analisar evidências de um anti-padrão específico. Os anti-padrões foram previamente catalogados e podem ser visualizados em: https://observability-antipatterns.github.io/

---

## Instalação

### Dependências

```
docker compose up -d

## Instalação

![Visão Geral dos Resultados da Detecção de Alertas Excessivos](images/poc-resultalerts.png)

- Figura 2: Visão Geral dos Resultados da Detecção de Alertas Excessivos

![Detalhes de Alertas Detectados como Excessivos](images/poc-resultsalerts2.png)

- Figura 3: Detalhes de Alertas Detectados como Excessivos

![Detalhes de Alertas não Detectados como Excessivos](images/poc-resultsalerts3.png)

- Figura 4: Detalhes de Alertas não Detectados como Excessivos

# Observa: Framework para Detecção Automática de Anti-padrões de Observabilidade


O **Observa** é um framework desenvolvido para facilitar a detecção automática de anti-padrões de observabilidade pelos usuários. 

O framework atua como intermediário entre fontes de dados e detectores de anti-padrões. Por meio do Observa, é possível criar qualquer tipo de fonte de dados, desde que estruturada em formato JSON, como dados de alertas, logs, traces, dashboards, entre outros.

Um vídeo foi criado para facilitar o entendimento prático do framework:  
https://www.youtube.com/watch?v=

## Fontes de Dados

Na configuração das fontes de dados, existem duas possibilidades:

1. Criar uma nova fonte de dados manualmente, em um arquivo JSON;  
2. Adicionar uma fonte de dados existente, vinculando-a por meio de uma API.

No primeiro caso, tratam-se de dados **estáticos**, portanto o detector sempre produzirá a mesma resposta ao analisá-los.  
No segundo caso, como a fonte está vinculada a uma API, o endpoint pode fornecer dados **dinâmicos**. Como pré-requisito, essa API deve disponibilizar os dados via requisição **GET**.

Independentemente da origem, uma vez obtidos os dados, o Observa os envia ao **detector** selecionado pelo usuário.

Cada detector deve ser uma **API** capaz de:
- Receber um JSON via método **POST**;
- Retornar uma resposta também em formato **JSON**, seguindo a estrutura abaixo.

```json
{
  "analyzed": 10,
  "detected": 4,
  "data": []
}
