import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['figure.titlesize'] = 13


def plot_etapa1_tempos(df_resumo: pd.DataFrame, out_path: str):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    n = df_resumo["tamanho_n"]
    t_bf = df_resumo["bf_media_s"]
    t_dc = df_resumo["dc_media_s"]
    t_kd = df_resumo["kd_media_s"]

    ax1.plot(n, t_bf, 'o-', color='#d9534f', linewidth=2, markersize=6, label='Força Bruta $O(n^2)$')
    ax1.plot(n, t_dc, 's-', color='#0275d8', linewidth=2, markersize=6, label='Divisão e Conquista $O(n \\log n)$')
    ax1.plot(n, t_kd, '^-', color='#5cb85c', linewidth=2, markersize=6, label='Kadane $O(n)$ [Desafio]')
    ax1.set_title("Etapa 1: Tempo de Execução (Escala Linear)")
    ax1.set_xlabel("Tamanho da Entrada (n)")
    ax1.set_ylabel("Tempo de Execução (segundos)")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.6)

    ax2.plot(n, t_bf, 'o-', color='#d9534f', linewidth=2, markersize=6, label='Força Bruta $O(n^2)$')
    ax2.plot(n, t_dc, 's-', color='#0275d8', linewidth=2, markersize=6, label='Divisão e Conquista $O(n \\log n)$')
    ax2.plot(n, t_kd, '^-', color='#5cb85c', linewidth=2, markersize=6, label='Kadane $O(n)$ [Desafio]')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title("Etapa 1: Tempo de Execução (Escala Log-Log)")
    ax2.set_xlabel("Tamanho da Entrada (n) [escala log]")
    ax2.set_ylabel("Tempo de Execução (segundos) [escala log]")
    ax2.legend()
    ax2.grid(True, which="both", linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")


def plot_etapa2_tempos(df_resumo: pd.DataFrame, out_path: str):
    fig, ax1 = plt.subplots(figsize=(9, 5.5))

    n = df_resumo["tamanho_n"]
    t_bf = df_resumo["bf_media_s"]
    t_dc = df_resumo["dc_media_s"]
    speedup = df_resumo["speedup_dc_sobre_bf"]

    color_bf = '#d9534f'
    color_dc = '#0275d8'
    color_sp = '#f0ad4e'

    line1 = ax1.plot(n, t_bf, 'o-', color=color_bf, linewidth=2.2, markersize=7, label='Força Bruta $O(n^2)$')
    line2 = ax1.plot(n, t_dc, 's-', color=color_dc, linewidth=2.2, markersize=7, label='Divisão e Conquista $O(n \\log n)$')
    ax1.set_xlabel("Quantidade de Pontos (n)")
    ax1.set_ylabel("Tempo Médio (segundos)", color='#333333')
    ax1.tick_params(axis='y', labelcolor='#333333')
    ax1.grid(True, linestyle="--", alpha=0.6)

    ax2 = ax1.twinx()
    line3 = ax2.plot(n, speedup, 'd--', color=color_sp, linewidth=2, markersize=6, label='Speedup (BF / DC)')
    ax2.set_ylabel("Speedup ($t_{BF} / t_{DC}$)", color='#b87a00')
    ax2.tick_params(axis='y', labelcolor='#b87a00')
    ax2.grid(False)

    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    plt.title("Etapa 2: Par de Pontos Mais Próximos - Desempenho e Speedup")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")


def plot_etapa2_ajuste_teorico(df_resumo: pd.DataFrame, out_path: str):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    n = np.array(df_resumo["tamanho_n"])
    t_bf = np.array(df_resumo["bf_media_s"])
    t_dc = np.array(df_resumo["dc_media_s"])

    c_bf = t_bf[-1] / (n[-1] ** 2)
    t_bf_teorico = c_bf * (n ** 2)

    ax1.plot(n, t_bf, 'o', color='#d9534f', markersize=8, label='Medições Reais (Força Bruta)')
    ax1.plot(n, t_bf_teorico, '--', color='#a94442', linewidth=2, label='Modelo Teórico $c \\cdot n^2$')
    ax1.set_title("Ajuste Assintótico: Força Bruta vs $O(n^2)$")
    ax1.set_xlabel("Quantidade de Pontos (n)")
    ax1.set_ylabel("Tempo (segundos)")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.6)

    n_logn = n * np.log2(n)
    c_dc = t_dc[-1] / n_logn[-1]
    t_dc_teorico = c_dc * n_logn

    ax2.plot(n, t_dc, 's', color='#0275d8', markersize=8, label='Medições Reais (D&C)')
    ax2.plot(n, t_dc_teorico, '--', color='#014c8c', linewidth=2, label='Modelo Teórico $c \\cdot n \\log_2 n$')
    ax2.set_title("Ajuste Assintótico: Divisão e Conquista vs $O(n \\log n)$")
    ax2.set_xlabel("Quantidade de Pontos (n)")
    ax2.set_ylabel("Tempo (segundos)")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")


def plot_limiares_estudo(df_limiares: pd.DataFrame, out_path: str):
    fig, ax = plt.subplots(figsize=(8, 5))

    th = df_limiares["limiar_threshold"]
    t = df_limiares["tempo_medio_s"] * 1000
    err = df_limiares["desvio_padrao_s"] * 1000

    ax.errorbar(th, t, yerr=err, fmt='o-', color='#5bc0de', ecolor='#2aabd2',
                elinewidth=1.5, capsize=4, linewidth=2, markersize=6)
    
    idx_min = t.idxmin()
    best_th = th.iloc[idx_min]
    best_t = t.iloc[idx_min]
    ax.scatter([best_th], [best_t], color='#d9534f', s=120, zorder=5, label=f'Limiar Ótimo (T = {best_th})')
    ax.annotate(f'Mínimo: {best_t:.2f} ms\n(Limiar {best_th})',
                xy=(best_th, best_t), xytext=(best_th + 5, best_t + 0.5),
                arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))

    ax.set_title("Sensibilidade do Tempo ao Limiar de Caso Base (n = 3200)")
    ax.set_xlabel("Limiar de Parada / Cutoff (Tamanho do Caso Base)")
    ax.set_ylabel("Tempo Médio de Execução (ms)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")


def plot_crossover_estudo(df_cross: pd.DataFrame, out_path: str):
    fig, ax = plt.subplots(figsize=(8, 5))

    n = df_cross["tamanho_n"]
    t_bf = df_cross["bf_media_s"] * 1e6
    t_dc = df_cross["dc_media_s"] * 1e6

    ax.plot(n, t_bf, 'o-', color='#d9534f', linewidth=2, markersize=6, label='Força Bruta')
    ax.plot(n, t_dc, 's-', color='#0275d8', linewidth=2, markersize=6, label='Divisão e Conquista')

    ax.set_title("Análise de Crossover para Instâncias Microscópicas (n ≤ 128)")
    ax.set_xlabel("Tamanho da Entrada (n)")
    ax.set_ylabel("Tempo Médio de Execução (µs)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")


def draw_geometric_strip_diagram(out_path: str):
    fig, ax = plt.subplots(figsize=(8, 6.5))

    delta = 4.0
    half_delta = delta / 2.0

    rect = patches.Rectangle((-delta, 0), 2 * delta, delta,
                             linewidth=2, edgecolor='#333333', facecolor='#eef7ff', alpha=0.6)
    ax.add_patch(rect)

    ax.axvline(0, color='#d9534f', linestyle='--', linewidth=2.5, label='Linha Divisória Mediana ($x = x_{mid}$)')

    for x_line in [-half_delta, half_delta]:
        ax.plot([x_line, x_line], [0, delta], color='#888888', linestyle=':', linewidth=1.5)
    ax.plot([-delta, delta], [half_delta, half_delta], color='#888888', linestyle=':', linewidth=1.5)

    boxes = [
        (-3 * half_delta / 2, half_delta / 2, "C1"),
        (-half_delta / 2, half_delta / 2, "C2"),
        (-3 * half_delta / 2, 3 * half_delta / 2, "C3"),
        (-half_delta / 2, 3 * half_delta / 2, "C4"),
        (half_delta / 2, half_delta / 2, "C5"),
        (3 * half_delta / 2, half_delta / 2, "C6"),
        (half_delta / 2, 3 * half_delta / 2, "C7"),
        (3 * half_delta / 2, 3 * half_delta / 2, "C8"),
    ]
    for bx, by, name in boxes:
        ax.text(bx, by, f"{name}\n(max 1 pto)", ha='center', va='center', fontsize=9,
                color='#555555', bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7))

    ax.scatter([-1.0], [0.3], color='#d9534f', s=140, zorder=6, label='Ponto de referência $p_i$')
    ax.annotate('$p_i$ (origem de $y$)', xy=(-1.0, 0.3), xytext=(-3.5, 0.5),
                arrowprops=dict(facecolor='#d9534f', shrink=0.08, width=1, headwidth=5),
                fontsize=10, fontweight='bold', color='#d9534f')

    candidate_pts = [
        (-2.5, 2.5), (-1.2, 3.2), (0.8, 1.2), (1.5, 3.1), (2.8, 1.5), (3.1, 3.5)
    ]
    cx, cy = zip(*candidate_pts)
    ax.scatter(cx, cy, color='#0275d8', s=90, zorder=6, label='Vizinhos ordenados por $y$')

    ax.annotate('', xy=(-delta, -0.4), xytext=(delta, -0.4),
                arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.5))
    ax.text(0, -0.8, 'Largura da Faixa = $2\\delta$', ha='center', fontsize=11, fontweight='bold')

    ax.annotate('', xy=(delta + 0.3, 0), xytext=(delta + 0.3, delta),
                arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.5))
    ax.text(delta + 0.6, delta / 2, 'Altura = $\\delta$', va='center', rotation=270, fontsize=11, fontweight='bold')

    ax.set_xlim(-delta - 1.5, delta + 2.0)
    ax.set_ylim(-1.3, delta + 1.0)
    ax.set_aspect('equal')
    ax.set_title("Justificativa Geometrica: Por que bastam no maximo 7 comparacoes?\n"
                 r"Diagonal de cada caixa = $\delta / \sqrt{2} \approx 0.707\delta < \delta \to \leq 1$ ponto por caixa",
                 fontsize=11)
    ax.legend(loc='upper right', fontsize=9)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Salvo: {out_path}")


def main():
    bench_dir = os.path.dirname(os.path.abspath(__file__))
    fig_dir = os.path.join(bench_dir, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    df_e1 = pd.read_csv(os.path.join(bench_dir, "benchmark_etapa1_resumo.csv"))
    df_e2 = pd.read_csv(os.path.join(bench_dir, "benchmark_etapa2_resumo.csv"))
    df_lim = pd.read_csv(os.path.join(bench_dir, "benchmark_etapa2_limiares.csv"))
    df_cross = pd.read_csv(os.path.join(bench_dir, "benchmark_etapa2_crossover.csv"))

    plot_etapa1_tempos(df_e1, os.path.join(fig_dir, "etapa1_comparacao_tempos.png"))
    plot_etapa2_tempos(df_e2, os.path.join(fig_dir, "etapa2_comparacao_tempos.png"))
    plot_etapa2_ajuste_teorico(df_e2, os.path.join(fig_dir, "etapa2_ajuste_teorico.png"))
    plot_limiares_estudo(df_lim, os.path.join(fig_dir, "etapa2_estudo_limiar.png"))
    plot_crossover_estudo(df_cross, os.path.join(fig_dir, "etapa2_crossover.png"))
    draw_geometric_strip_diagram(os.path.join(fig_dir, "faixa_7_vizinhos_geometria.png"))

    print("Todos os gráficos foram gerados com sucesso!")


if __name__ == "__main__":
    main()
