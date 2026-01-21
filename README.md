# Observa Framework

O Observa é um framework para detecção automática de anti-padrões de observabilidade em aplicações distribuídas. Seu objetivo é avaliar a qualidade da observabilidade implementada a partir da análise de dados de telemetria, como métricas, logs, traces, alertas e dashboards. O framework integra diferentes fontes de dados e executa detectores especializados, sendo cada detector responsável por identificar um anti-padrão específico.

Um catálogo de anti-padrões de observabilidade está disponível em: https://observability-antipatterns.github.io/

---

## Instalação

Para facilitar a instalação do Observa, foi utilizado o Docker, o qual oferece isolamento completo e facilita o deployment em diferentes ambientes.

**Pré-Requisitos**

- Docker
- Docker Compose

**Passo 1:** Clone o repositório:

```
git clone https://github.com/andersonalmada/detect-antipatterns.git
cd detect-antipatterns
```

**Passo 2:** Execute o docker compose:

```
cd docker
docker compose up -d
```

## Execução

Uma vez iniciado os contêineres, o Observa é gerenciado de forma gráfica por meio do navegador na porta 8000:

```
http://localhost:8000
```

Caso queira encerrar o Observa, execute o seguinte comando:

```
docker compose down
```

## Prova de Conceito

Para demonstrar o Observa, é realizado a execução das principais funcionalidades, como adicionar as fontes de dados, adicionar detectores dos APs, realizar a detecção, visualizar os resultados e históricos das detecções. Nesse exemplo, são utilizados os dados de alertas como fontes de dados e realizado a detecção de APs de Alertas Excessivos.

![Visão Geral dos Resultados da Detecção de Alertas Excessivos](images/poc-resultalerts.png)

- Figura 2: Visão Geral dos Resultados da Detecção de Alertas Excessivos

![Detalhes de Alertas Detectados como Excessivos](images/poc-resultsalerts2.png)

- Figura 3: Detalhes de Alertas Detectados como Excessivos

![Detalhes de Alertas não Detectados como Excessivos](images/poc-resultsalerts3.png)

- Figura 4: Detalhes de Alertas não Detectados como Excessivos

