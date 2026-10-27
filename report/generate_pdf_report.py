
import os
import sys
import json
import pandas as pd
from pypdf import PdfReader

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        if self._pageNumber > 1:
            self.drawString(45, 810, "Trabalho Prático: Paradigma de Divisão e Conquista — Análise e Projeto de Algoritmos")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(45, 804, 550, 804)

        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.5)
        self.line(45, 45, 550, 45)

        texto_rodape = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(550, 32, texto_rodape)
        self.drawString(45, 32, "Relatório Técnico — Samuel Lopes & Rodrigo Temporal | Divisão e Conquista")
        self.restoreState()


def build_pdf_report(pdf_path: str):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    bench_dir = os.path.join(base_dir, 'benchmarks')
    fig_dir = os.path.join(bench_dir, 'figures')

    df_e1 = pd.read_csv(os.path.join(bench_dir, 'benchmark_etapa1_resumo.csv'))
    df_e2 = pd.read_csv(os.path.join(bench_dir, 'benchmark_etapa2_resumo.csv'))
    df_lim = pd.read_csv(os.path.join(bench_dir, 'benchmark_etapa2_limiares.csv'))
    df_cross = pd.read_csv(os.path.join(bench_dir, 'benchmark_etapa2_crossover.csv'))

    with open(os.path.join(bench_dir, 'configuracao_maquina.json'), 'r', encoding='utf-8') as f:
        specs = json.load(f)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    dark_neutral = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#F7FAFC")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral,
        spaceAfter=5,
        alignment=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#2C5282")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        alignment=1
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    author_style = ParagraphStyle(
        'DocAuthors',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=primary_color,
        alignment=1,
        spaceAfter=8
    )

    story = []

    story.append(Paragraph("Trabalho Prático: Paradigma de Divisão e Conquista", title_style))
    story.append(Paragraph("Implementação, Análise Assintótica, Otimizações e Avaliação Experimental", subtitle_style))
    story.append(Paragraph("<b>Alunos / Dupla:</b> Samuel Lopes &nbsp;&nbsp;|&nbsp;&nbsp; Rodrigo Temporal", author_style))

    meta_info = [
        [
            Paragraph("<b>Alunos:</b> Samuel Lopes e Rodrigo Temporal", body_style),
            Paragraph("<b>Data de Entrega:</b> 28/10/2026", body_style)
        ],
        [
            Paragraph("<b>Disciplina:</b> Análise e Projeto de Algoritmos", body_style),
            Paragraph("<b>Linguagem:</b> Python 3.12 (CPython 64-bit)", body_style)
        ],
        [
            Paragraph(f"<b>CPU:</b> {specs['processor']}", body_style),
            Paragraph(f"<b>Configuração:</b> {specs['cpu_cores']} | {specs['ram']}", body_style)
        ],
        [
            Paragraph(f"<b>Sistema Operacional:</b> {specs['os']}", body_style),
            Paragraph("<b>Reprodutibilidade:</b> CLI main.py & Testes 100% OK", body_style)
        ]
    ]
    t_meta = Table(meta_info, colWidths=[250, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), light_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Introdução e Objetivos", h1_style))
    story.append(Paragraph(
        "O paradigma de <b>Divisão e Conquista (D&C)</b> baseia-se na decomposição recursiva de uma instância "
        "complexa de tamanho <i>n</i> em subproblemas menores e independentes do mesmo tipo, na resolução recursiva "
        "desses subproblemas e na combinação linear eficiente de suas soluções para compor a resposta global. "
        "O presente trabalho aborda dois problemas clássicos e fundamentais da computação que não envolvem ordenação: "
        "<b>(1) Subarranjo de Soma Máxima (Maximum Subarray Problem)</b> e <b>(2) Par de Pontos Mais Próximos (Closest Pair of Points)</b>. "
        "Para ambos, implementamos e comparamos exaustivamente as soluções de força bruta contra as formulações "
        "em divisão e conquista, estendendo a análise à solução linear <i>O(n)</i> de Kadane (questão desafio), "
        "validando empiricamente as ordens assintóticas através de medições reais de tempo em laboratório.",
        body_style
    ))

    story.append(Paragraph("2. Etapa 1: Subarranjo de Soma Máxima", h1_style))
    story.append(Paragraph(
        "<b>Contexto e Formulação:</b> Uma corretora de valores registra a variação diária no preço de determinado ativo financeiro "
        "como uma sequência de inteiros <i>A = [a<sub>0</sub>, a<sub>1</sub>, ..., a<sub>n-1</sub>]</i>, onde valores positivos representam "
        "lucro e negativos prejuízo. Deseja-se determinar o intervalo contínuo <i>[i, j]</i> (com 0 &le; i &le; j &lt; n) que maximiza "
        "o ganho acumulado &sum;<sub>k=i</sub><sup>j</sup> a<sub>k</sub>.",
        body_style
    ))

    story.append(Paragraph("2.1. Abordagens Implementadas", h2_style))
    story.append(Paragraph(
        "<b>1. Força Bruta O(n²):</b> Itera sobre todos os possíveis índices iniciais <i>i</i> e finais <i>j</i>. Ao manter a soma "
        "corrente acumulada de forma incremental, o cálculo de cada subarranjo ocorre em tempo <i>O(1)</i>, totalizando "
        "&sum;<sub>i=0</sub><sup>n-1</sup> (n - i) = n(n+1)/2 avaliações, resultando em complexidade de tempo <b>&Theta;(n²)</b> e espaço <i>O(1)</i>.<br/>"
        "<b>2. Divisão e Conquista O(n log n):</b> Divide o vetor no ponto médio <i>mid = &lfloor;(low + high)/2&rfloor;</i>. Pelo princípio da divisão, "
        "o subarranjo máximo contínuo reside inteiramente na metade esquerda <i>[low .. mid]</i>, inteiramente na metade direita <i>[mid+1 .. high]</i>, "
        "ou cruza o ponto central. A função de cruzamento computa o melhor sufixo da esquerda terminando em <i>mid</i> e o melhor prefixo da direita "
        "iniciando em <i>mid+1</i> em tempo estritamente linear <i>O(n)</i>.<br/>"
        "<b>3. Questão Desafio — Algoritmo de Kadane O(n):</b> Aplica programação dinâmica linear. Para cada posição <i>i</i>, a soma máxima terminando "
        "em <i>i</i> é dada por <i>S[i] = max(a[i], S[i-1] + a[i])</i>. Executa em <b>&Theta;(n)</b> em uma única passagem pelo vetor e espaço <i>O(1)</i>.",
        body_style
    ))

    story.append(Paragraph("2.2. Resolução da Recorrência da Etapa 1 via Teorema Mestre", h2_style))
    story.append(Paragraph(
        "O algoritmo de Divisão e Conquista divide o vetor de tamanho <i>n</i> em dois subvetores de tamanho <i>n/2</i> e realiza "
        "a combinação cruzada examinando cada elemento exatamente uma vez em tempo linear &Theta;(n). A relação de recorrência é dada por:<br/>"
        "<font color='#1A365D'><b>&nbsp;&nbsp;&nbsp;&nbsp;T(n) = 2 &middot; T(n/2) + &Theta;(n), &nbsp;&nbsp;&nbsp;&nbsp;com T(1) = &Theta;(1)</b></font><br/>"
        "Aplicando o <b>Teorema Mestre</b> para recorrências da forma <i>T(n) = a &middot; T(n/b) + f(n)</i>:<br/>"
        "&bull; Identificamos os parâmetros: <i>a = 2</i> (número de subproblemas), <i>b = 2</i> (fator de redução), e <i>f(n) = &Theta;(n)</i>.<br/>"
        "&bull; Computamos o expoente crítico: <i>log<sub>b</sub>(a) = log<sub>2</sub>(2) = 1</i>, gerando a função de referência <i>n<sup>log<sub>b</sub> a</sup> = n<sup>1</sup> = n</i>.<br/>"
        "&bull; Comparando <i>f(n)</i> com <i>n<sup>log<sub>b</sub> a</sup></i>: temos que <i>f(n) = &Theta;(n) = &Theta;(n<sup>1</sup>)</i>. "
        "Isso caracteriza com exatidão o <b>Caso 2 do Teorema Mestre</b>.<br/>"
        "&bull; Conclusão Analítica: <b>T(n) = &Theta;(n<sup>log<sub>b</sub> a</sup> &middot; log n) = &Theta;(n log n)</b>.",
        body_style
    ))

    story.append(Paragraph("2.3. Tratamento Rigoroso de Casos de Borda", h2_style))
    story.append(Paragraph(
        "<b>&bull; Vetor com apenas valores negativos:</b> Se todos os valores forem negativos (ex: [-5, -2, -8]), a soma de qualquer intervalo "
        "com dois ou mais elementos é mais negativa que seus elementos individuais. Nossos três algoritmos tratam esse caso sem retornar zero "
        "ou intervalo vazio: identificam corretamente o elemento menos negativo (-2 no índice 1) com intervalo [1, 1].<br/>"
        "<b>&bull; Vetor unitário (n = 1):</b> Constitui a condição de parada base da recursão (low == high), retornando imediatamente o valor e índice [0, 0].<br/>"
        "<b>&bull; Empates na soma máxima:</b> Estabelecemos um critério determinístico e uniforme: em caso de empate numérico na soma, "
        "prioriza-se o intervalo de menor comprimento (fim - inicio + 1); se persistir o empate, prioriza-se o de menor índice inicial.",
        body_style
    ))

    story.append(PageBreak())
    story.append(Paragraph("3. Etapa 2: Par de Pontos Mais Próximos (Closest Pair of Points)", h1_style))
    story.append(Paragraph(
        "<b>Contexto e Formulação:</b> Dadas as coordenadas no plano cartesiano &real;² de <i>n</i> estações de monitoramento "
        "<i>P = {(x<sub>0</sub>, y<sub>0</sub>), ..., (x<sub>n-1</sub>, y<sub>n-1</sub>)}</i>, o objetivo é encontrar o par de estações "
        "<i>(p<sub>i</sub>, p<sub>j</sub>)</i> com <i>i &ne; j</i> que minimiza a distância euclidiana "
        "<i>d(p<sub>i</sub>, p<sub>j</sub>) = &radic;((x<sub>i</sub> - x<sub>j</sub>)² + (y<sub>i</sub> - y<sub>j</sub>)²)</i>.",
        body_style
    ))

    story.append(Paragraph("3.1. Abordagens e Estrutura Algorítmica", h2_style))
    story.append(Paragraph(
        "<b>1. Força Bruta O(n²):</b> Avalia exaustivamente todos os <i>n(n-1)/2</i> pares não ordenados de pontos, mantendo a menor "
        "distância encontrada. Possui tempo &Theta;(n²) e dispensa ordenação prévia.<br/>"
        "<b>2. Divisão e Conquista O(n log n):</b> Executa em três etapas estruturadas:<br/>"
        "&nbsp;&nbsp;&bull; <i>Pré-processamento:</i> Ordena o conjunto de pontos por coordenada <i>x</i> (obtendo <i>P<sub>x</sub></i>) e por "
        "coordenada <i>y</i> (obtendo <i>P<sub>y</sub></i>) uma única vez no início, utilizando o algoritmo padrão da linguagem em <i>O(n log n)</i>.<br/>"
        "&nbsp;&nbsp;&bull; <i>Divisão Recursiva:</i> Encontra a linha vertical mediana <i>x = mid<sub>x</sub></i> baseada em <i>P<sub>x</sub>[&lfloor;n/2&rfloor;]</i>. "
        "Particiona <i>P<sub>x</sub></i> em metades esquerda <i>Q<sub>x</sub></i> e direita <i>R<sub>x</sub></i>. De forma crucial, particiona "
        "<i>P<sub>y</sub></i> em <i>Q<sub>y</sub></i> e <i>R<sub>y</sub></i> em tempo estritamente linear <i>O(n)</i> preservando a ordenação em <i>y</i>, "
        "sem recorrer a reordenações.<br/>"
        "&nbsp;&nbsp;&bull; <i>Conquista e Combinação:</i> Calcula recursivamente <i>&delta;<sub>E</sub></i> e <i>&delta;<sub>D</sub></i>, definindo "
        "<i>&delta; = min(&delta;<sub>E</sub>, &delta;<sub>D</sub>)</i>. Em seguida, filtra em <i>O(n)</i> os pontos situados na faixa vertical "
        "<i>[mid<sub>x</sub> - &delta;, mid<sub>x</sub> + &delta;]</i>. Para cada ponto da faixa, compara sua distância euclidiana com no máximo "
        "<b>7 vizinhos subsequentes ordenados por y</b>.",
        body_style
    ))

    story.append(Paragraph("3.2. Resolução da Recorrência da Etapa 2 via Teorema Mestre", h2_style))
    story.append(Paragraph(
        "Como a ordenação de <i>P<sub>x</sub></i> e <i>P<sub>y</sub></i> é realizada como pré-processamento global fora do loop recursivo em tempo <i>O(n log n)</i>, "
        "e cada chamada recursiva realiza apenas a divisão de listas em <i>O(n)</i> e a varredura da faixa com no máximo <i>7n = O(n)</i> comparações, "
        "a recorrência do algoritmo recursivo é:<br/>"
        "<font color='#1A365D'><b>&nbsp;&nbsp;&nbsp;&nbsp;T(n) = 2 &middot; T(n/2) + O(n), &nbsp;&nbsp;&nbsp;&nbsp;com T(n &le; limiar) = O(1)</b></font><br/>"
        "Pelo <b>Teorema Mestre</b>: temos <i>a = 2</i>, <i>b = 2</i>, <i>f(n) = O(n)</i>. O valor de <i>n<sup>log<sub>2</sub> 2</sup> = n</i> é assintoticamente "
        "equivalente a <i>f(n)</i> (Caso 2), resultando em <b>T<sub>rec</sub>(n) = O(n log n)</b>.<br/>"
        "O tempo total do algoritmo é dado por <i>T<sub>total</sub>(n) = T<sub>sort</sub>(n) + T<sub>rec</sub>(n) = O(n log n) + O(n log n) = <b>O(n log n)</b></i>.",
        body_style
    ))

    story.append(Paragraph("3.3. Demonstração Formal: Por que bastam no máximo 7 comparações por ponto na faixa?", h2_style))
    story.append(Paragraph(
        "Esta é a propriedade geométrica central que garante a complexidade <i>O(n log n)</i> do algoritmo:<br/>"
        "1. Seja <i>&delta; = min(&delta;<sub>E</sub>, &delta;<sub>D</sub>)</i> a menor distância encontrada nas metades esquerda e direita. "
        "Nenhum par de pontos pertencente inteiramente à esquerda ou inteiramente à direita pode distar menos que <i>&delta;</i>.<br/>"
        "2. Logo, um par mais próximo só pode surgir se um ponto estiver à esquerda da linha divisória e o outro à direita, "
        "ambos contidos na faixa vertical de largura <i>2&delta;</i> centrada em <i>mid<sub>x</sub></i>.<br/>"
        "3. Para cada ponto <i>p<sub>i</sub> = (x<sub>i</sub>, y<sub>i</sub>)</i> nessa faixa, qualquer ponto <i>p<sub>j</sub></i> com <i>y<sub>j</sub> &ge; y<sub>i</sub></i> "
        "que satisfaça <i>dist(p<sub>i</sub>, p<sub>j</sub>) &lt; &delta;</i> deve obrigatoriamente possuir coordenada <i>y</i> no intervalo semiaberto "
        "<i>[y<sub>i</sub>, y<sub>i</sub> + &delta;]</i> e coordenada <i>x</i> no intervalo <i>[mid<sub>x</sub> - &delta;, mid<sub>x</sub> + &delta;]</i>.<br/>"
        "4. Isso define uma região retangular de dimensões <b>2&delta; de largura por &delta; de altura</b>.<br/>"
        "5. A linha vertical central <i>x = mid<sub>x</sub></i> divide este retângulo em duas metades simétricas de dimensões <i>&delta; &times; &delta;</i> "
        "(lado esquerdo e lado direito).<br/>"
        "6. Subdividimos cada quadrado <i>&delta; &times; &delta;</i> em <b>4 subquadrados menores</b> de lado <i>(&delta;/2) &times; (&delta;/2)</i>, "
        "totalizando 8 compartimentos no retângulo completo.<br/>"
        "7. A distância máxima possível entre quaisquer dois pontos dentro de um mesmo subquadrado de lado <i>&delta;/2</i> é a sua diagonal:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>d<sub>max</sub> = &radic;((&delta;/2)² + (&delta;/2)²) = &radic;(2 &middot; &delta;²/4) = &delta; &middot; &radic;2 / 2 &approx; 0,7071 &middot; &delta; &lt; &delta;</i>.<br/>"
        "8. Pelo <b>Princípio da Casa dos Pombos</b>, como todos os pontos em uma mesma metade distam pelo menos <i>&delta;</i> entre si, "
        "<b>nenhum subquadrado menor de lado &delta;/2 pode conter mais de 1 ponto</b>!<br/>"
        "9. Consequentemente, cada metade <i>&delta; &times; &delta;</i> pode conter no máximo 4 pontos, e o retângulo total de <i>2&delta; &times; &delta;</i> "
        "pode conter no máximo <b>4 + 4 = 8 pontos</b>.<br/>"
        "10. Como um desses 8 pontos é o próprio ponto de referência <i>p<sub>i</sub></i>, restam no máximo <b>8 - 1 = 7 outros pontos</b> "
        "que precisam ser examinados na ordenação por <i>y</i>. Fica rigorosamente demonstrado que examinar no máximo 7 vizinhos é suficiente.",
        body_style
    ))

    fig_faixa = os.path.join(fig_dir, "faixa_7_vizinhos_geometria.png")
    if os.path.exists(fig_faixa):
        story.append(Spacer(1, 4))
        story.append(Image(fig_faixa, width=15*cm, height=9.2*cm))
        story.append(Paragraph("<b>Figura 1:</b> Diagrama demonstrativo da partição geométrica da faixa de largura 2&delta; em 8 subcompartimentos de &delta;/2 &times; &delta;/2.", callout_style))

    story.append(PageBreak())
    story.append(Paragraph("4. Análise Experimental: Etapa 1 (Subarranjo de Soma Máxima)", h1_style))
    story.append(Paragraph(
        "A avaliação empírica do tempo de execução foi conduzida no ambiente experimental padronizado (processador AMD Ryzen 5 3400G, "
        "16 GB RAM, Python 3.12 64-bit). Para cada tamanho de entrada <i>n &in; {100, 200, 400, 800, 1600, 3200, 6400}</i>, "
        "foram executadas <b>5 repetições independentes com sementes controladas</b> para obtenção da média aritmética e do desvio padrão.",
        body_style
    ))

    tabela_e1_dados = [
        [
            Paragraph("<b>Tamanho (n)</b>", table_header_style),
            Paragraph("<b>Força Bruta O(n²)<br/>Média &plusmn; Desvio (s)</b>", table_header_style),
            Paragraph("<b>Divisão & Conquista O(n log n)<br/>Média &plusmn; Desvio (s)</b>", table_header_style),
            Paragraph("<b>Kadane O(n) [Desafio]<br/>Média &plusmn; Desvio (s)</b>", table_header_style),
            Paragraph("<b>Speedup<br/>(BF / DC)</b>", table_header_style),
            Paragraph("<b>Speedup<br/>(BF / Kadane)</b>", table_header_style)
        ]
    ]

    for _, row in df_e1.iterrows():
        n_val = int(row["tamanho_n"])
        t_bf = row["bf_media_s"]
        d_bf = row["bf_desvio_s"]
        t_dc = row["dc_media_s"]
        d_dc = row["dc_desvio_s"]
        t_kd = row["kd_media_s"]
        d_kd = row["kd_desvio_s"]
        sp_dc = t_bf / t_dc
        sp_kd = t_bf / t_kd

        tabela_e1_dados.append([
            Paragraph(f"{n_val:,}", table_cell_style),
            Paragraph(f"{t_bf:.5f} &plusmn; {d_bf:.5f}", table_cell_style),
            Paragraph(f"{t_dc:.5f} &plusmn; {d_dc:.5f}", table_cell_style),
            Paragraph(f"{t_kd:.6f} &plusmn; {d_kd:.6f}", table_cell_style),
            Paragraph(f"<b>{sp_dc:.1f}&times;</b>", table_cell_style),
            Paragraph(f"<b>{sp_kd:.0f}&times;</b>", table_cell_style)
        ])

    t_e1 = Table(tabela_e1_dados, colWidths=[70, 115, 125, 115, 50, 55])
    t_e1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_e1)
    story.append(Paragraph("<b>Tabela 1:</b> Medições de tempo real e speedup da Etapa 1 para tamanhos crescentes de entrada.", callout_style))
    story.append(Spacer(1, 8))

    fig_e1 = os.path.join(fig_dir, "etapa1_comparacao_tempos.png")
    if os.path.exists(fig_e1):
        story.append(Image(fig_e1, width=17.5*cm, height=6.8*cm))
        story.append(Paragraph("<b>Figura 2:</b> Curvas experimentais de tempo da Etapa 1 em escala linear (esquerda) e escala log-log (direita).", callout_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("4.1. Discussão dos Resultados da Etapa 1", h2_style))
    story.append(Paragraph(
        "A análise dos dados experimentais confirma com rigor cirúrgico as previsões assintóticas:<br/>"
        "&bull; <b>Comportamento Quadrático da Força Bruta:</b> Ao dobrar a entrada de <i>n = 1.600</i> (0,195 s) para <i>n = 3.200</i> (0,790 s) "
        "e em seguida para <i>n = 6.400</i> (3,132 s), o tempo quadruplica a cada passo (fatores de 4,05&times; e 3,96&times;), "
        "obedecendo rigorosamente à relação <i>(2n)² = 4n²</i> inerente a <i>O(n²)</i>.<br/>"
        "&bull; <b>Comportamento Subquadrático de D&C:</b> O algoritmo de divisão e conquista escala suavemente, saltando de 3,88 ms em <i>n = 1.600</i> "
        "para 16,3 ms em <i>n = 6.400</i>. O fator de crescimento ao dobrar <i>n</i> é de apenas ~2,1&times; (exatamente compatível com <i>2n &middot; log(2n) / (n log n)</i>). "
        "Em <i>n = 6.400</i>, o algoritmo D&C já é <b>192 vezes mais veloz</b> que a força bruta.<br/>"
        "&bull; <b>Excelência do Algoritmo Linear de Kadane (Desafio):</b> Processa 6.400 elementos em escassos 1,31 milissegundos, "
        "sendo <b>12,4 vezes mais rápido que D&C e impressionantes 2.379 vezes mais rápido que a força bruta</b>. A curva linear no gráfico log-log "
        "apresenta inclinação unitária perfeita, validando a ausência de sobrecarga de pilha ou divisão.",
        body_style
    ))

    story.append(PageBreak())
    story.append(Paragraph("5. Análise Experimental: Etapa 2 (Par de Pontos Mais Próximos)", h1_style))
    story.append(Paragraph(
        "Para a Etapa 2, foram avaliados rigorosamente os tamanhos recomendados no enunciado: "
        "<i>n &in; {100, 200, 400, 800, 1600, 3200, 6400}</i> com coordenadas aleatórias bidimensionais e 5 repetições por tamanho.",
        body_style
    ))

    tabela_e2_dados = [
        [
            Paragraph("<b>Quantidade de Pontos (n)</b>", table_header_style),
            Paragraph("<b>Força Bruta O(n²)<br/>Média &plusmn; Desvio (s)</b>", table_header_style),
            Paragraph("<b>Divisão & Conquista O(n log n)<br/>Média &plusmn; Desvio (s)</b>", table_header_style),
            Paragraph("<b>Speedup Real<br/>(t<sub>BF</sub> / t<sub>DC</sub>)</b>", table_header_style),
            Paragraph("<b>Relação Teórica<br/>n / log₂(n)</b>", table_header_style)
        ]
    ]

    import math
    for _, row in df_e2.iterrows():
        n_val = int(row["tamanho_n"])
        t_bf = row["bf_media_s"]
        d_bf = row["bf_desvio_s"]
        t_dc = row["dc_media_s"]
        d_dc = row["dc_desvio_s"]
        sp = row["speedup_dc_sobre_bf"]
        teorico_rel = n_val / math.log2(n_val)

        tabela_e2_dados.append([
            Paragraph(f"{n_val:,}", table_cell_style),
            Paragraph(f"{t_bf:.5f} &plusmn; {d_bf:.5f}", table_cell_style),
            Paragraph(f"{t_dc:.5f} &plusmn; {d_dc:.5f}", table_cell_style),
            Paragraph(f"<b>{sp:.1f}&times;</b>", table_cell_style),
            Paragraph(f"{teorico_rel:.1f}", table_cell_style)
        ])

    t_e2 = Table(tabela_e2_dados, colWidths=[100, 140, 140, 75, 75])
    t_e2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_e2)
    story.append(Paragraph("<b>Tabela 2:</b> Resultados empíricos para o problema do Par de Pontos Mais Próximos na máquina de testes.", callout_style))
    story.append(Spacer(1, 6))

    fig_e2_tempos = os.path.join(fig_dir, "etapa2_comparacao_tempos.png")
    if os.path.exists(fig_e2_tempos):
        story.append(Image(fig_e2_tempos, width=17*cm, height=8*cm))
        story.append(Paragraph("<b>Figura 3:</b> Desempenho e curva de Speedup (eixo secundário) para a Etapa 2.", callout_style))

    story.append(Spacer(1, 6))
    fig_e2_ajuste = os.path.join(fig_dir, "etapa2_ajuste_teorico.png")
    if os.path.exists(fig_e2_ajuste):
        story.append(Image(fig_e2_ajuste, width=17*cm, height=6.5*cm))
        story.append(Paragraph("<b>Figura 4:</b> Ajuste do modelo analítico teórico (linhas pontilhadas) sobre os pontos experimentais reais (círculos/quadrados).", callout_style))

    story.append(PageBreak())
    story.append(Paragraph("6. Discussão Aprofundada dos Gráficos e Ajuste Teórico", h1_style))
    story.append(Paragraph(
        "A <b>Figura 3</b> e a <b>Figura 4</b> ilustram com clareza cristalina o descolamento assintótico entre as complexidades:<br/>"
        "&bull; <b>Aderência Perfeita ao Modelo c &middot; n²:</b> Na Figura 4 (esquerda), a curva ajustada pelo modelo teórico <i>c &middot; n²</i> "
        "passa com exatidão sobre todas as medições de força bruta (R² > 0,999). A força bruta cresce de 1,26 milissegundo para 6,03 segundos em <i>n = 6.400</i>.<br/>"
        "&bull; <b>Aderência ao Modelo c &middot; n log₂ n:</b> Na Figura 4 (direita), o algoritmo D&C acompanha rigorosamente a curva teórica "
        "<i>c &middot; n log₂ n</i>. Para <i>n = 6.400</i>, o tempo de execução foi de apenas 50,8 milissegundos, atingindo um <b>speedup impressionante de 118,7&times;</b>.<br/>"
        "&bull; <b>Crescimento Monotônico do Speedup:</b> O speedup cresce de 2,7&times; (n=100) para 118,7&times; (n=6.400). A teoria prevê que "
        "<i>Speedup(n) = &Theta;(n² / (n log n)) = &Theta;(n / log n)</i>. Como verificado na Tabela 2, a razão entre os speedups práticos "
        "espelha com fidelidade o aumento da métrica <i>n / log₂(n)</i>.",
        body_style
    ))

    story.append(Paragraph("7. Por que a Força Bruta ou a Divisão e Conquista Vence para Tamanhos Diferentes?", h1_style))
    story.append(Paragraph(
        "Um equívoco comum em análise assintótica é supor que um algoritmo de menor ordem de complexidade (ex: <i>O(n log n)</i>) é "
        "sempre mais rápido do que um de maior ordem (ex: <i>O(n²)</i>) para qualquer tamanho de entrada. Na prática, a fórmula real do tempo "
        "é governada por constantes ocultas e termos de ordem inferior:<br/>"
        "<font color='#1A365D'><b>&nbsp;&nbsp;&nbsp;&nbsp;T<sub>BF</sub>(n) = c<sub>BF</sub> &middot; n² + k<sub>BF</sub> &nbsp;&nbsp;&nbsp;&nbsp;versus&nbsp;&nbsp;&nbsp;&nbsp; "
        "T<sub>DC</sub>(n) = c<sub>DC</sub> &middot; n log n + O(n) + C<sub>pilha</sub></b></font><br/>"
        "As razões fundamentais para a inversão de dominância (ponto de crossover) são:<br/>"
        "<b>1. Sobrecarga de Alocação de Memória e List Comprehensions:</b> O algoritmo D&C cria subconjuntos de listas (<i>Q<sub>x</sub>, R<sub>x</sub>, Q<sub>y</sub>, R<sub>y</sub></i> "
        "e a faixa <i>strip</i>), o que consome ciclos de CPU com alocação de objetos em memória heap e passagem de referências na pilha de recursão.<br/>"
        "<b>2. Simplicidade e Localidade de Cache da Força Bruta:</b> A força bruta executa apenas dois laços contíguos com acesso linear direto a um único array, "
        "sem nenhuma chamada de função recursiva e sem alocar um único byte adicional de memória. Em hardware moderno, isso maximiza a eficiência "
        "da linha de cache L1 da CPU e permite ao interpretador executar loops densos com baixíssimo overhead constante.<br/>"
        "<b>3. Ponto de Crossover Experimental:</b> Para quantificar o limiar exato onde a Força Bruta perde a liderança, realizamos uma análise "
        "experimental dedicada para instâncias pequenas (<i>n &le; 128</i>), apresentada na <b>Figura 5</b>.",
        body_style
    ))

    fig_cross = os.path.join(fig_dir, "etapa2_crossover.png")
    if os.path.exists(fig_cross):
        story.append(Spacer(1, 4))
        story.append(Image(fig_cross, width=15*cm, height=7*cm))
        story.append(Paragraph("<b>Figura 5:</b> Análise de Crossover para instâncias microscópicas (n &le; 128): a Força Bruta vence para n &le; 32 devido à ausência de sobrecarga recursiva.", callout_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Os dados revelam que para <i>n &le; 32</i> a <b>Força Bruta é superior</b> (para <i>n = 4</i>, BF leva 3,3 &mu;s vs 11,5 &mu;s de D&C; "
        "para <i>n = 16</i>, BF leva 32,7 &mu;s vs 55,1 &mu;s de D&C). Entre <b>n = 32 e n = 40</b> ocorre a interseção exata (crossover), "
        "e a partir de <i>n &ge; 48</i> o crescimento quadrático supera a sobrecarga fixa, consagrando a Divisão e Conquista como imbatível.",
        body_style
    ))

    story.append(PageBreak())
    story.append(Paragraph("8. Justificativa Teórica e Experimental do Limiar (Threshold) na Etapa 2", h1_style))
    story.append(Paragraph(
        "No algoritmo clássico de Divisão e Conquista, o limiar padrão adotado nos livros-texto é <i>limiar = 3</i>, pois com 3 ou menos pontos "
        "é inviável particionar geometricamente sem gerar subproblemas triviais de tamanho 1 (para os quais a distância entre pares não é definida). "
        "Entretanto, em implementações reais, <b>interromper a recursão mais cedo e resolver subconjuntos pequenos por força bruta</b> é uma técnica "
        "de engenharia de software de altíssimo impacto (semelhante ao que faz o Timsort ou Introsort).<br/>"
        "Para justificar a escolha do limiar de parada ótimo, mantivemos fixa uma entrada representativa de <b>n = 3.200 pontos</b> "
        "e variamos o parâmetro <i>threshold</i> entre <b>2 e 128</b>, medindo o tempo médio de 5 execuções independentes.",
        body_style
    ))

    fig_lim = os.path.join(fig_dir, "etapa2_estudo_limiar.png")
    if os.path.exists(fig_lim):
        story.append(Image(fig_lim, width=15*cm, height=7.2*cm))
        story.append(Paragraph("<b>Figura 6:</b> Variação do tempo de execução em função do limiar de caso base (threshold) para n = 3.200.", callout_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("8.1. Interpretação dos Resultados do Limiar", h2_style))
    story.append(Paragraph(
        "A curva da Figura 6 apresenta uma forma côncava característica de otimização convexa, evidenciando o compromisso de desempenho:<br/>"
        "&bull; <b>Zona de Sobrecarga Recursiva (Threshold &le; 3):</b> Para <i>T = 2</i> o tempo foi de <b>25,17 ms</b>, e para <i>T = 3</i> foi de <b>22,56 ms</b>. "
        "Nessa faixa, a árvore de recursão é aprofundada até o nível máximo <i>&lceil;log₂ n&rceil; &approx; 12</i> níveis, gerando milhares "
        "de chamadas de função desnecessárias para particionar subarranjos diminutos de 2 ou 3 elementos.<br/>"
        "&bull; <b>Faixa Ótima de Equilíbrio (Threshold entre 8 e 24):</b> O tempo atinge seu ponto mínimo global em <b>T = 16 (18,00 ms)</b>, "
        "proporcionando um ganho de eficiência de <b>28,5% sobre T = 2</b> e <b>20,2% sobre T = 3</b>. Nesse limiar, eliminam-se os últimos "
        "4 níveis mais profundos da árvore recursiva (economizando mais de 200 chamadas recursivas), transferindo a resolução para a força bruta, "
        "que para 16 pontos requer apenas <i>16 &times; 15 / 2 = 120</i> comparações ultrarrápidas em memória contígua.<br/>"
        "&bull; <b>Zona de Degradação Quadrática (Threshold &ge; 48):</b> Quando o limiar cresce excessivamente (<i>T = 64</i>: 30,30 ms; <i>T = 128</i>: 49,85 ms), "
        "o custo quadrático <i>O(T²)</i> de rodar força bruta nas folhas começa a superar os benefícios da divisão, degradando o tempo total.<br/>"
        "<b>Conclusão e Justificativa:</b> Mantivemos o valor padrão em <i>threshold = 3</i> no código para atender com fidelidade estrita à especificação "
        "teórica clássica da disciplina, mas disponibilizamos o parâmetro configurável via CLI (<code>--threshold 16</code>) permitindo que o usuário "
        "alcance o desempenho prático máximo.",
        body_style
    ))

    story.append(Paragraph("9. Bateria de Testes Automatizados e Cobertura de Casos de Borda", h1_style))
    story.append(Paragraph(
        "Em conformidade com o peso de <b>40% na avaliação</b>, desenvolvemos uma suíte abrangente com 19 testes automatizados "
        "em <code>unittest</code> e arquivos de casos de teste em formatos legível (<code>.txt</code>) e estruturado (<code>.json</code>):<br/>"
        "<b>1. Casos de Borda da Etapa 1:</b><br/>"
        "&nbsp;&nbsp;&bull; <i>Vetor totalmente negativo:</i> Entrada <code>[-5, -2, -8, -12, -3]</code> &rarr; Retorna com precisão a soma máxima <code>-2</code> e índice <code>[1, 1]</code>.<br/>"
        "&nbsp;&nbsp;&bull; <i>Vetor unitário:</i> Testado com valor positivo (<code>[42]</code> &rarr; <code>(42, 0, 0)</code>) e negativo (<code>[-99]</code> &rarr; <code>(-99, 0, 0)</code>).<br/>"
        "&nbsp;&nbsp;&bull; <i>Empates múltiplos:</i> Entrada <code>[3, -5, 3]</code> &rarr; Aplicação do critério determinístico de menor tamanho e menor índice inicial (índice 0).<br/>"
        "&nbsp;&nbsp;&bull; <i>Neutros aditivos (zeros):</i> Garante que zeros intermediários não dilatem incorretamente o intervalo ótimo.<br/>"
        "<b>2. Casos de Borda da Etapa 2:</b><br/>"
        "&nbsp;&nbsp;&bull; <i>Pontos coincidentes:</i> Pares com exatamente a mesma coordenada geográfica &rarr; Retorna distância exata <code>0.000000</code>.<br/>"
        "&nbsp;&nbsp;&bull; <i>Alinhamentos perpendiculares:</i> Pontos colineares horizontais (mesmo <i>y</i>) e verticais (mesmo <i>x</i>).<br/>"
        "&nbsp;&nbsp;&bull; <i>Tamanhos mínimos:</i> Instâncias com <i>n = 2</i> e <i>n = 3</i> pontos, validando os casos base.<br/>"
        "&nbsp;&nbsp;&bull; <i>Coordenadas em múltiplos quadrantes:</i> Valores fracionários finos e negativos.<br/>"
        "&nbsp;&nbsp;&bull; <i>Teste de Par Cruzado Crítico:</i> Instância em que o par mais próximo cruza a linha divisória vertical da mediana.",
        body_style
    ))

    story.append(PageBreak())
    story.append(Paragraph("10. Conclusões e Considerações Finais", h1_style))
    story.append(Paragraph(
        "A realização deste trabalho prático permitiu comprovar de forma empírica e analítica a supremacia assintótica do paradigma "
        "de <b>Divisão e Conquista</b> sobre métodos ingênuos de Força Bruta para problemas geométricos e de otimização contígua:<br/>"
        "1. <b>Equivalência Teórico-Experimental:</b> As medições de laboratório com cronometria de alta resolução demonstraram uma correlação "
        "quase perfeita com as soluções analíticas obtidas pelo Teorema Mestre. A duplicação da entrada resultou em quadruplicação do tempo para a força bruta "
        "(<i>O(n²)</i>) e em apenas duplicação marginal para a divisão e conquista (<i>O(n log n)</i>).<br/>"
        "2. <b>Impacto do Algoritmo de Kadane:</b> A implementação da questão desafio em tempo estritamente linear <i>O(n)</i> evidenciou "
        "o poder da programação dinâmica sobre a divisão e conquista quando a estrutura ótima do problema permite eliminar o custo de combinação recursiva, "
        "superando a força bruta por um fator superior a 2.300 vezes.<br/>"
        "3. <b>Importância da Poda Geométrica:</b> Na Etapa 2, a restrição de examinar no máximo 7 vizinhos ordenados na faixa provou ser o coração "
        "da eficiência do algoritmo, evitando que a etapa de combinação degenerasse para o custo quadrático.<br/>"
        "4. <b>Engenharia de Algoritmos no Mundo Real:</b> O estudo de crossover e limiares comprovou que algoritmos práticos de alto desempenho "
        "devem combinar o melhor dos dois mundos: o paradigma de divisão e conquista para guiar a macroestrutura assintótica e a força bruta direta "
        "nas folhas da árvore para anular a sobrecarga de recursão.",
        body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("11. Estrutura do Repositório Git e Entregáveis", h1_style))
    story.append(Paragraph(
        "O repositório do projeto foi estruturado com organização modular e boas práticas de desenvolvimento:<br/>"
        "&bull; <code>src/etapa1_max_subarray.py</code>: Implementações de Força Bruta, Divisão e Conquista e Kadane (Desafio).<br/>"
        "&bull; <code>src/etapa2_closest_pair.py</code>: Implementações de Força Bruta e Divisão e Conquista (7 vizinhos e threshold configurável).<br/>"
        "&bull; <code>tests/</code>: Suíte completa de testes unitários automatizados (19 testes aprovados cobrindo 100% dos casos de borda).<br/>"
        "&bull; <code>test_cases/</code>: Arquivos formatados de teste (<code>.txt</code> e <code>.json</code>) com entradas, saídas esperadas e justificativas.<br/>"
        "&bull; <code>benchmarks/</code>: Scripts de benchmark automatizado, medições brutas em CSV e gráficos gerados em alta resolução.<br/>"
        "&bull; <code>main.py</code>: Interface CLI completa para execução, testes, benchmarks e compilação do relatório.<br/>"
        "&bull; <code>README.md</code>: Manual de execução, dependências e guia de reprodução experimental.",
        body_style
    ))

    story.append(Spacer(1, 10))
    story.append(Paragraph("12. Referências Bibliográficas", h1_style))
    story.append(Paragraph(
        "[1] CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. <i>Introduction to Algorithms</i>. 3rd ed. MIT Press, 2009. "
        "Capítulo 4 (Divide-and-Conquer) e Capítulo 33 (Computational Geometry).<br/>"
        "[2] BENTLEY, J. L.; SHAMOS, M. I. <i>Divide-and-conquer in multidimensional space</i>. In: Proceedings of the eighth annual ACM symposium on Theory of computing. 1976. p. 220-230.<br/>"
        "[3] KLEINBERG, J.; TARDOS, É. <i>Algorithm Design</i>. Addison-Wesley, 2006. Capítulo 5 (Divide and Conquer).<br/>"
        "[4] SEDGEWICK, R.; WAYNE, K. <i>Algorithms</i>. 4th ed. Addison-Wesley Professional, 2011.<br/>"
        "[5] KADANE, J. B. <i>Maximum Subarray Problem</i>. In: BENTLEY, J. Programming Pearls. Communications of the ACM, 1984.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Relatório PDF gerado com sucesso em: {pdf_path}")


def main():
    report_dir = os.path.dirname(os.path.abspath(__file__))
    out_pdf = os.path.join(report_dir, "relatorio_divisao_conquista.pdf")
    build_pdf_report(out_pdf)

    reader = PdfReader(out_pdf)
    total_pages = len(reader.pages)
    print(f"Total de páginas no relatório: {total_pages} (Limite do edital: até 8 páginas)")

    downloads_pdf = "D:\\Downloads\\Relatorio_Divisao_e_Conquista.pdf"
    import shutil
    shutil.copyfile(out_pdf, downloads_pdf)
    print(f"Cópia do relatório também salva em: {downloads_pdf}")


if __name__ == "__main__":
    main()
