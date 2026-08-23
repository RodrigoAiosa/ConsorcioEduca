"""Geração de PDF com o resumo da simulação de consórcio."""

import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

from utils.calculos import valor_lance


def gerar_pdf_simulacao(params, resultado, fluxo, reajuste_aplicado=False, indice_anual=None,
                         lance_proprio_perc=0.0, lance_embutido_perc=0.0) -> bytes:
    """Gera um PDF (em bytes) com o resumo da simulação de consórcio."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle("TituloCustom", parent=styles["Title"], textColor=colors.HexColor("#0F766E"))
    subtitulo_style = ParagraphStyle("SubtituloCustom", parent=styles["Heading2"], textColor=colors.HexColor("#0F766E"),
                                      spaceBefore=14, spaceAfter=6)
    normal = styles["Normal"]
    aviso_style = ParagraphStyle("Aviso", parent=styles["Normal"], textColor=colors.HexColor("#92400E"),
                                  backColor=colors.HexColor("#FEF3C7"), borderPadding=8, spaceBefore=10)

    story = []

    story.append(Paragraph("Consórcio Educa", titulo_style))
    story.append(Paragraph("Resumo da Simulação de Consórcio", styles["Heading3"]))
    story.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal))
    story.append(Spacer(1, 16))

    # --- Parâmetros do plano ---
    story.append(Paragraph("Parâmetros do plano", subtitulo_style))
    dados_params = [
        ["Valor do bem", f"R$ {params.valor_bem:,.2f}"],
        ["Prazo", f"{params.prazo_meses} meses"],
        ["Taxa de administração total", f"{params.taxa_administracao_total:.2f}%"],
        ["Fundo de reserva total", f"{params.fundo_reserva_total:.2f}%"],
        ["Seguro mensal (sobre saldo devedor)", f"{params.seguro_mensal_perc:.2f}%"],
    ]
    if reajuste_aplicado:
        dados_params.append(["Reajuste anual aplicado", f"{indice_anual:.2f}% ao ano"])

    t = Table(dados_params, colWidths=[9 * cm, 7 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0FDF4")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # --- Resultado ---
    story.append(Paragraph("Resultado estimado", subtitulo_style))
    dados_resultado = [
        ["Parcela base estimada", f"R$ {resultado['parcela_base']:,.2f}"],
        ["Parcela média (com seguro)", f"R$ {resultado['parcela_media_total']:,.2f}"],
        ["Custo total do plano", f"R$ {resultado['custo_total_plano']:,.2f}"],
        ["Custo Efetivo Total (CET)", f"{resultado['custo_efetivo_total_perc']:.2f}%"],
    ]
    t2 = Table(dados_resultado, colWidths=[9 * cm, 7 * cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0FDF4")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))

    # --- Lance (se houver) ---
    if lance_proprio_perc > 0 or lance_embutido_perc > 0:
        story.append(Paragraph("Impacto do lance", subtitulo_style))
        info_lance = valor_lance(params)
        dados_lance = [
            ["Lance próprio (desembolso)", f"R$ {info_lance['lance_proprio_valor']:,.2f}"],
            ["Lance embutido (do próprio crédito)", f"R$ {info_lance['lance_embutido_valor']:,.2f}"],
            ["Crédito líquido após embutido", f"R$ {info_lance['credito_liquido_apos_embutido']:,.2f}"],
        ]
        t3 = Table(dados_lance, colWidths=[9 * cm, 7 * cm])
        t3.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0FDF4")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t3)
        story.append(Spacer(1, 10))

    # --- Fluxo mensal (amostra: primeiros 12 meses + últimos 3) ---
    story.append(PageBreak())
    story.append(Paragraph("Evolução mês a mês (amostra)", subtitulo_style))

    linhas_amostra = fluxo[:12]
    if len(fluxo) > 15:
        linhas_amostra = fluxo[:12] + [{"mes": "...", "parcela_base": "...", "seguro": "...",
                                         "parcela_total": "...", "saldo_devedor_estimado": "..."}] + fluxo[-3:]

    cabecalho = ["Mês", "Parcela base (R$)", "Seguro (R$)", "Parcela total (R$)", "Saldo devedor (R$)"]
    linhas_tabela = [cabecalho]
    for linha in linhas_amostra:
        linhas_tabela.append([
            str(linha["mes"]),
            f"{linha['parcela_base']:,.2f}" if isinstance(linha["parcela_base"], (int, float)) else linha["parcela_base"],
            f"{linha['seguro']:,.2f}" if isinstance(linha["seguro"], (int, float)) else linha["seguro"],
            f"{linha['parcela_total']:,.2f}" if isinstance(linha["parcela_total"], (int, float)) else linha["parcela_total"],
            f"{linha['saldo_devedor_estimado']:,.2f}" if isinstance(linha["saldo_devedor_estimado"], (int, float)) else linha["saldo_devedor_estimado"],
        ])

    t4 = Table(linhas_tabela, colWidths=[2 * cm, 3.5 * cm, 3 * cm, 3.5 * cm, 4 * cm], repeatRows=1)
    t4.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
    ]))
    story.append(t4)
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "<b>Aviso:</b> esta simulação usa fórmulas didáticas simplificadas, baseadas em práticas comuns "
        "do mercado de consórcios. Não substitui o contrato oficial nem o Custo Efetivo Total (CET) "
        "informado pela administradora. Consulte sempre a documentação oficial antes de decidir.",
        aviso_style,
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
