# 🧭 Consórcio Educa

Simulador e ferramenta de educação financeira sobre **consórcios**, feito em
Python + Streamlit. O objetivo é atacar uma das maiores deficiências do setor:
a falta de clareza sobre **quanto realmente se paga**, **como funciona a
contemplação** e **como o consórcio se compara** a outras formas de adquirir
um bem (financiamento, poupança programada).

> ⚠️ Projeto educativo. Não substitui consultoria financeira nem o CET oficial
> informado pela administradora.

## ✨ Funcionalidades

- **Simulador de Consórcio** — parcela estimada, custo efetivo total (CET),
  composição de custos (taxa de administração, fundo de reserva, seguro) e
  impacto de lance próprio/embutido.
- **Comparador** — consórcio vs. financiamento (Tabela Price) vs. poupança
  programada, lado a lado, para o mesmo bem.
- **Glossário** — termos do setor explicados sem economês (taxa de
  administração, lance embutido, fundo de reserva, CET, etc.), com busca e
  filtro por categoria.
- **Simulador de Contemplação** — visualização didática de como a
  probabilidade de sorteio evolui conforme o tamanho do grupo e o prazo.
- **Reajuste anual (INCC/IPCA)** — opção no simulador para aplicar reajuste
  periódico do valor do bem, mostrando o "salto" de parcela típico de
  consórcios de imóvel (INCC) ou outros bens corrigidos anualmente.
- **Exportar em PDF** — gera um PDF com o resumo completo da simulação
  (parâmetros, resultado, lance e fluxo mensal) para guardar ou comparar depois.
- **Comparar Administradoras via CSV** — importe uma planilha com condições
  de diferentes administradoras (ou propostas recebidas de vendedores) e
  veja parcela, custo total e CET lado a lado, com ranking automático.

## 🖥️ Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/consorcio-educa.git
cd consorcio-educa

# 2. Crie um ambiente virtual (opcional, recomendado)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o app
streamlit run app.py
```

O app abrirá em `http://localhost:8501`.

## 🚀 Deploy gratuito (Streamlit Community Cloud)

1. Suba este projeto para um repositório no seu GitHub.
2. Acesse [share.streamlit.io](https://share.streamlit.io) e conecte sua conta do GitHub.
3. Selecione o repositório, o branch `main` e o arquivo principal `app.py`.
4. Clique em **Deploy** — pronto, você terá uma URL pública gratuita.

## 📁 Estrutura do projeto

```
consorcio-educa/
├── app.py                     # Página inicial (Home)
├── pages/
│   ├── 1_Simulador.py                  # Simulador de consórcio (com reajuste e export PDF)
│   ├── 2_Comparador.py                 # Comparador consórcio x financiamento x poupança
│   ├── 3_Glossario.py                  # Glossário educativo
│   ├── 4_Contemplacao.py               # Simulador de probabilidade de contemplação
│   └── 5_Comparar_Administradoras.py   # Importação de CSV e comparação entre administradoras
├── utils/
│   ├── calculos.py            # Motor de cálculo financeiro (inclui reajuste anual)
│   ├── pdf_export.py          # Geração do PDF de resumo da simulação
│   └── glossario.py           # Base de dados do glossário
├── .streamlit/
│   └── config.toml            # Tema visual
├── requirements.txt
└── README.md
```

## 🧮 Sobre as fórmulas

As fórmulas usadas são simplificações didáticas baseadas em práticas comuns
do mercado de consórcios brasileiro:

- **Custo total do plano** = valor do bem + (taxa de administração % × valor
  do bem) + (fundo de reserva % × valor do bem).
- **Seguro prestamista** incide sobre o saldo devedor estimado (aproximação
  linear e decrescente ao longo do plano).
- **Financiamento** usa a Tabela Price (parcelas fixas, juros compostos).
- **Poupança programada** usa a fórmula de valor futuro de uma série de
  aportes fixos, para saber quanto seria necessário guardar por mês.
- **Probabilidade de contemplação** é uma estimativa simplificada baseada na
  proporção de contemplados/mês sobre participantes ainda ativos — **não** é
  a fórmula oficial de nenhuma administradora específica.

## 🗺️ Ideias para evolução (roadmap)

- [x] Importar tabelas reais de administradoras (CSV/planilha) para
      comparação mais precisa.
- [x] Adicionar reajuste anual do bem (INCC, IPCA) na simulação de saldo devedor.
- [x] Exportar simulação em PDF.
- [ ] Modo "monte seu plano ideal" com metas de contemplação.
- [ ] Testes automatizados (`pytest`) para o motor de cálculo.
- [ ] Suporte a múltiplos índices de reajuste (INCC, IPCA, IGP-M) com valores históricos reais.

## 🤝 Contribuindo

Pull requests são bem-vindos! Abra uma issue descrevendo a melhoria ou
correção antes de submeter um PR grande, para alinharmos o escopo.

## 📄 Licença

MIT — sinta-se livre para usar, modificar e distribuir.
