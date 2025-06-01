# Heurística de Construção para Mapeamento de Enchentes

Este projeto implementa uma heurística de construção para otimizar a seleção de locais para intervenção em áreas propensas a enchentes em Nova Iguaçu, RJ.

## Descrição

O sistema utiliza uma abordagem heurística para selecionar os melhores locais para intervenção, considerando:

- População afetada
- Criticidade da área
- Impacto da intervenção (em m²)
- Custo da intervenção
- Orçamento disponível
- Limite de intervenções

## Estrutura do Projeto

- `instance_generator.py`: Gera instâncias aleatórias do problema com dados realistas
- `main.py`: Implementa a heurística de construção e resolve o problema
- `nova_iguacu_dataset_heuristica.csv`: Dataset com os dados dos bairros
- `solution_viavel.csv`: Arquivo de saída com a solução encontrada

## Requisitos

- Python 3.x
- pandas
- numpy

## Instalação

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Usar

1. Gere uma nova instância do problema:

```bash
python instance_generator.py
```

2. Execute a heurística:

```bash
python main.py
```

## Parâmetros Configuráveis

No arquivo `main.py`:

- `max_budget`: Orçamento máximo disponível (R$ mil)
- `limit_sewer`: Número máximo de intervenções permitidas

## Saída

O programa gera um arquivo `solution_viavel.csv` contendo:

- Bairros selecionados
- População afetada
- Criticidade
- Impacto da intervenção
- Custo
- Prioridade calculada

## Lógica da Heurística

1. Calcula a prioridade de cada local usando a fórmula:

   ```
   Prioridade = (Impacto × Criticidade) / Custo
   ```
2. Seleciona os locais considerando:

   - Orçamento disponível
   - Limite de intervenções
   - Prioridade calculada

## Contribuição

Sinta-se à vontade para contribuir com o projeto através de pull requests ou reportando issues.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
