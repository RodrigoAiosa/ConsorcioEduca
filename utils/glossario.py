"""Base de dados do glossário educativo sobre consórcios."""

GLOSSARIO = [
    {
        "termo": "Taxa de Administração",
        "categoria": "Custos",
        "explicacao": (
            "É a remuneração que a administradora do consórcio recebe pelo serviço de "
            "organizar o grupo, cobrar as parcelas, realizar assembleias e gerir os recursos. "
            "É expressa em % sobre o valor do bem e diluída ao longo de todo o prazo do plano "
            "(embora algumas administradoras concentrem parte dela nas primeiras parcelas). "
            "Não é devolvida em caso de desistência."
        ),
        "dica": "Compare sempre a taxa TOTAL do plano, não apenas a taxa mensal — administradoras podem apresentar os números de formas diferentes."
    },
    {
        "termo": "Fundo de Reserva",
        "categoria": "Custos",
        "explicacao": (
            "Um percentual adicional cobrado para formar um 'colchão' financeiro do grupo, "
            "usado para cobrir inadimplência de outros participantes ou custos extras. "
            "Parte dele pode ser devolvida ao final do grupo, se sobrar saldo — mas isso "
            "não é garantido e depende do regulamento do grupo."
        ),
        "dica": "Pergunte explicitamente se há previsão de devolução de fundo de reserva no contrato."
    },
    {
        "termo": "Contemplação",
        "categoria": "Funcionamento",
        "explicacao": (
            "É o momento em que o participante recebe a carta de crédito para usar na compra "
            "do bem. Acontece de duas formas: por SORTEIO (mensal, entre todos os cotistas em dia) "
            "ou por LANCE (oferta de valor antecipado, quem oferece mais — ou atende a critérios "
            "do grupo — é contemplado)."
        ),
        "dica": "Ser sorteado não depende de pagar mais: todo participante em dia concorre igualmente ao sorteio."
    },
    {
        "termo": "Lance Livre",
        "categoria": "Estratégia de Contemplação",
        "explicacao": (
            "Oferta de um valor em dinheiro, do próprio bolso do participante, para tentar "
            "antecipar a contemplação. Quem oferece o maior percentual sobre o valor do bem "
            "(ou crédito) geralmente tem prioridade, dependendo das regras do grupo."
        ),
        "dica": "Um lance alto pode contemplar rápido, mas compromete uma reserva financeira que poderia ser usada de outra forma."
    },
    {
        "termo": "Lance Embutido",
        "categoria": "Estratégia de Contemplação",
        "explicacao": (
            "Uma parte do PRÓPRIO crédito do consórcio é usada como lance. Ou seja, o participante "
            "não precisa desembolsar dinheiro extra, mas recebe um crédito líquido menor do que "
            "o valor total contratado ao ser contemplado."
        ),
        "dica": "Muito usado por quem não tem reserva extra, mas reduz o valor final disponível para a compra do bem."
    },
    {
        "termo": "Saldo Devedor",
        "categoria": "Funcionamento",
        "explicacao": (
            "É o valor que ainda falta pagar ao grupo depois da contemplação. Mesmo tendo recebido "
            "a carta de crédito, o participante continua pagando as parcelas mensais até o fim do prazo."
        ),
        "dica": "Contemplação não é 'quitação' — é apenas a liberação do crédito; as parcelas continuam."
    },
    {
        "termo": "Seguro Prestamista",
        "categoria": "Custos",
        "explicacao": (
            "Seguro (geralmente obrigatório) que quita o saldo devedor do consórcio em caso de morte "
            "ou invalidez do participante, protegendo os dependentes de terem que assumir a dívida."
        ),
        "dica": "O custo do seguro normalmente diminui ao longo do plano, pois incide sobre o saldo devedor."
    },
    {
        "termo": "Diluição de Parcela",
        "categoria": "Funcionamento",
        "explicacao": (
            "Quando novos participantes entram no grupo (recompra de cotas desistentes) ou o grupo "
            "é reequilibrado, o valor das parcelas restantes pode ser recalculado e reduzido para os "
            "participantes ainda ativos."
        ),
        "dica": "Não é garantido — depende de haver desistências e política de reposição do grupo."
    },
    {
        "termo": "Assembleia de Contemplação",
        "categoria": "Funcionamento",
        "explicacao": (
            "Reunião mensal (geralmente) onde ocorrem o sorteio e a apuração de lances. É nela que "
            "se define quem será contemplado naquele mês."
        ),
        "dica": "Acompanhe as atas — administradoras sérias publicam os resultados de forma transparente."
    },
    {
        "termo": "CET — Custo Efetivo Total",
        "categoria": "Custos",
        "explicacao": (
            "Soma de todos os custos do consórcio (taxa de administração + fundo de reserva + seguro) "
            "expressos como um percentual sobre o valor do bem. É o número mais justo para comparar "
            "consórcios entre si ou consórcio vs. financiamento."
        ),
        "dica": "Sempre peça o CET total do plano antes de assinar — não confie apenas na 'taxa de administração'."
    },
    {
        "termo": "Grupo e Cota",
        "categoria": "Funcionamento",
        "explicacao": (
            "O 'grupo' é o conjunto de participantes que juntam recursos para contemplar uns aos "
            "outros ao longo do tempo. 'Cota' é a fração/participação individual de cada consorciado "
            "dentro desse grupo."
        ),
        "dica": "Grupos maiores tendem a ter mais sorteios por mês, mas também mais concorrência total."
    },
]
