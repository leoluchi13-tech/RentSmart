# RentSmart

**Aluno:** Leonardo Luchiari  
**RA:** 244548

Sistema de orçamento de locação da R.M Imóveis. Trabalho de **Algorithmic Thinking & Introduction to Object-Oriented Programming**.

## Como executar

Instale Python 3.10 ou superior. Extraia o ZIP e abra um terminal na pasta `RentSmart`. Execute:

```bash
python rentsmart.py
```

No Windows, caso o comando `python` seja indisponível, use `py rentsmart.py`. O programa usa apenas a biblioteca padrão do Python.

O terminal apresenta o aluguel com seus componentes e as parcelas da taxa contratual. O arquivo `projecao_12_meses.csv` é criado no diretório atual e substituído quando outro orçamento é exportado. O CSV usa UTF-8 com BOM, ponto e vírgula entre colunas e vírgula decimal. Se necessário, selecione essas opções ao importá-lo no Excel.

## Demonstração

Escolha **1 → 2 → S → N → 3** para simular um apartamento de dois quartos, uma vaga, sem crianças, com a taxa dividida em três parcelas.

- Aluguel-base de R$ 700,00, adicional de quarto de R$ 200,00 e vaga de R$ 300,00.
- Desconto de R$ 60,00 (5% de R$ 1.200,00). Aluguel mensal de R$ 1.140,00.
- Taxa contratual de R$ 2.000,00, com parcelas de R$ 666,66, R$ 666,66 e R$ 666,68.
- Total previsto de R$ 15.680,00 em 12 meses.

O arquivo `exemplo_projecao_12_meses.csv` mostra o resultado dessa execução. Para o estúdio, a contratação da garagem é opcional e começa pelo pacote de duas vagas. A taxa contratual é lançada a partir do primeiro mês e eventual diferença de centavos entra na última parcela.

## Organização

`Imovel` guarda as regras de preço da categoria. `Orcamento` combina a categoria e as escolhas do cliente, detalha o aluguel e calcula os pagamentos do primeiro ano. As funções de terminal e exportação cuidam das entradas e saídas.
