"""
Motor de cálculo financeiro para simulação de consórcios.

Todas as funções retornam estruturas simples (dict / list de dict) para
serem consumidas diretamente pelo Streamlit e pelo pandas.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ParametrosConsorcio:
    valor_bem: float
    prazo_meses: int
    taxa_administracao_total: float  # em % sobre o valor do bem, total do plano
    fundo_reserva_total: float       # em % sobre o valor do bem, total do plano
    seguro_mensal_perc: float        # em % ao mês sobre o saldo devedor (aprox.)
    lance_embutido_perc: float = 0.0  # em % do valor do bem, usado como lance mas
                                       # que "sai" do próprio crédito
    lance_proprio_perc: float = 0.0   # em % do valor do bem, dinheiro próprio ofertado como lance


@dataclass
class ParametrosReajuste:
    indice_anual_perc: float = 0.0   # ex: 4.5 significa 4,5% ao ano
    mes_aplicacao: int = 12          # a cada quantos meses o reajuste é aplicado (geralmente 12)


@dataclass
class ParametrosFinanciamento:
    valor_bem: float
    entrada_perc: float
    prazo_meses: int
    taxa_juros_mensal: float  # em % a.m. (ex: 1.5 = 1,5% a.m.)


def parcela_consorcio_pre_contemplacao(p: ParametrosConsorcio) -> Dict:
    """
    Calcula a parcela mensal do consórcio ANTES da contemplação (fase padrão,
    sem considerar redução por lance ou diluição de saldo).

    Fórmula simplificada, próxima da prática do mercado:
      Custo total do plano = valor_bem + (taxa_administracao_total% * valor_bem)
                                        + (fundo_reserva_total% * valor_bem)
      Parcela pura (crédito) = custo_total / prazo_meses
      Seguro = seguro_mensal_perc% * saldo_devedor (aproximado pelo valor do bem
               na primeira parcela, decrescente ao longo do plano)
    """
    custo_administracao = p.valor_bem * (p.taxa_administracao_total / 100)
    custo_fundo_reserva = p.valor_bem * (p.fundo_reserva_total / 100)
    custo_total_plano = p.valor_bem + custo_administracao + custo_fundo_reserva

    parcela_base = custo_total_plano / p.prazo_meses

    # seguro decrescente: aproxima saldo devedor linear
    seguros = []
    saldo = p.valor_bem
    decremento = p.valor_bem / p.prazo_meses
    for _ in range(p.prazo_meses):
        seguro_mes = saldo * (p.seguro_mensal_perc / 100)
        seguros.append(seguro_mes)
        saldo -= decremento

    parcela_media_com_seguro = parcela_base + (sum(seguros) / p.prazo_meses)

    return {
        "custo_administracao": custo_administracao,
        "custo_fundo_reserva": custo_fundo_reserva,
        "custo_total_plano": custo_total_plano,
        "parcela_base": parcela_base,
        "seguro_medio_mensal": sum(seguros) / p.prazo_meses,
        "parcela_media_total": parcela_media_com_seguro,
        "custo_efetivo_total_perc": (custo_total_plano - p.valor_bem) / p.valor_bem * 100,
    }


def fluxo_mensal_consorcio(p: ParametrosConsorcio) -> List[Dict]:
    """Gera o fluxo mês a mês (parcela + seguro decrescente)."""
    base = parcela_consorcio_pre_contemplacao(p)
    parcela_base = base["parcela_base"]

    fluxo = []
    saldo = p.valor_bem
    decremento = p.valor_bem / p.prazo_meses
    for mes in range(1, p.prazo_meses + 1):
        seguro_mes = saldo * (p.seguro_mensal_perc / 100)
        fluxo.append({
            "mes": mes,
            "parcela_base": round(parcela_base, 2),
            "seguro": round(seguro_mes, 2),
            "parcela_total": round(parcela_base + seguro_mes, 2),
            "saldo_devedor_estimado": round(saldo, 2),
        })
        saldo -= decremento
    return fluxo


def fluxo_mensal_consorcio_com_reajuste(p: ParametrosConsorcio, reajuste: ParametrosReajuste) -> List[Dict]:
    """
    Gera o fluxo mês a mês do consórcio considerando reajuste periódico
    (ex: anual) do valor do bem por um índice como INCC ou IPCA.

    Modelo didático: a cada `mes_aplicacao` meses, o saldo remanescente
    (tanto o custo total ainda a pagar quanto o saldo devedor usado para
    calcular o seguro) é corrigido pelo índice informado. A parcela é
    recalculada dividindo o custo restante pelos meses restantes — por
    isso ela "dá um salto" no mês do reajuste, como costuma acontecer na
    prática (ex: consórcio de imóvel reajustado pelo INCC).
    """
    base = parcela_consorcio_pre_contemplacao(p)
    custo_total_restante = base["custo_total_plano"]
    saldo_devedor = p.valor_bem
    meses_restantes = p.prazo_meses
    fator_indice = 1 + (reajuste.indice_anual_perc / 100)

    fluxo = []
    valor_bem_atualizado = p.valor_bem

    for mes in range(1, p.prazo_meses + 1):
        # aplica o reajuste no aniversário do plano (mês 13, 25, 37... para mes_aplicacao=12)
        if reajuste.indice_anual_perc > 0 and mes > 1 and (mes - 1) % reajuste.mes_aplicacao == 0:
            custo_total_restante *= fator_indice
            saldo_devedor *= fator_indice
            valor_bem_atualizado *= fator_indice

        parcela_base_mes = custo_total_restante / meses_restantes if meses_restantes > 0 else 0
        seguro_mes = saldo_devedor * (p.seguro_mensal_perc / 100)

        fluxo.append({
            "mes": mes,
            "valor_bem_atualizado": round(valor_bem_atualizado, 2),
            "parcela_base": round(parcela_base_mes, 2),
            "seguro": round(seguro_mes, 2),
            "parcela_total": round(parcela_base_mes + seguro_mes, 2),
            "saldo_devedor_estimado": round(saldo_devedor, 2),
        })

        custo_total_restante -= parcela_base_mes
        saldo_devedor -= (saldo_devedor / meses_restantes) if meses_restantes > 0 else 0
        meses_restantes -= 1

    return fluxo


def valor_lance(p: ParametrosConsorcio) -> Dict:
    """Calcula quanto o participante precisa desembolsar de lance próprio
    e quanto do crédito é consumido pelo lance embutido."""
    lance_embutido_valor = p.valor_bem * (p.lance_embutido_perc / 100)
    lance_proprio_valor = p.valor_bem * (p.lance_proprio_perc / 100)
    credito_liquido_apos_embutido = p.valor_bem - lance_embutido_valor
    return {
        "lance_embutido_valor": lance_embutido_valor,
        "lance_proprio_valor": lance_proprio_valor,
        "lance_total_ofertado": lance_embutido_valor + lance_proprio_valor,
        "credito_liquido_apos_embutido": credito_liquido_apos_embutido,
    }


def probabilidade_contemplacao_simples(num_participantes: int, num_contemplados_mes: int,
                                        mes_atual: int, total_meses: int) -> Dict:
    """
    Estimativa didática (não é a fórmula oficial da administradora) da
    chance de contemplação por sorteio em um mês específico, considerando
    participantes ainda não contemplados.
    Objetivo é EDUCATIVO: mostrar como a base de participantes ativos diminui
    e a probabilidade relativa de sorteio se altera ao longo do grupo.
    """
    participantes_restantes = max(num_participantes - (num_contemplados_mes * (mes_atual - 1)), 1)
    prob_mes = min(num_contemplados_mes / participantes_restantes, 1.0)
    # probabilidade acumulada aproximada de já ter sido contemplado até o mês atual
    prob_acumulada = 1 - ((1 - (num_contemplados_mes / num_participantes)) ** mes_atual)
    return {
        "participantes_restantes_estimado": participantes_restantes,
        "probabilidade_sorteio_no_mes": prob_mes,
        "probabilidade_acumulada_estimada": min(prob_acumulada, 1.0),
    }


def simular_financiamento(p: ParametrosFinanciamento) -> Dict:
    """Tabela Price simplificada para comparação."""
    valor_financiado = p.valor_bem * (1 - p.entrada_perc / 100)
    i = p.taxa_juros_mensal / 100
    n = p.prazo_meses

    if i == 0:
        parcela = valor_financiado / n
    else:
        parcela = valor_financiado * (i * (1 + i) ** n) / ((1 + i) ** n - 1)

    total_pago = parcela * n
    total_juros = total_pago - valor_financiado
    entrada_valor = p.valor_bem * (p.entrada_perc / 100)

    return {
        "valor_financiado": valor_financiado,
        "entrada_valor": entrada_valor,
        "parcela_mensal": parcela,
        "total_pago_periodo": total_pago + entrada_valor,
        "total_juros_pagos": total_juros,
        "custo_efetivo_total_perc": (total_juros / valor_financiado) * 100 if valor_financiado else 0,
    }


def simular_poupanca_programada(valor_bem: float, prazo_meses: int, rendimento_mensal_perc: float) -> Dict:
    """
    Quanto seria necessário guardar todo mês, rendendo a uma taxa mensal,
    para juntar o valor do bem ao final do prazo (aporte fixo, valor futuro).
    """
    i = rendimento_mensal_perc / 100
    n = prazo_meses
    if i == 0:
        aporte_mensal = valor_bem / n
    else:
        aporte_mensal = valor_bem * i / (((1 + i) ** n) - 1)

    total_aportado = aporte_mensal * n
    rendimento_total = valor_bem - total_aportado

    return {
        "aporte_mensal": aporte_mensal,
        "total_aportado": total_aportado,
        "rendimento_total_obtido": rendimento_total,
    }
