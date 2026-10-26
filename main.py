import argparse
import sys
import os

from src.etapa1_max_subarray import (
    max_subarray_brute_force,
    max_subarray_divide_conquer,
    max_subarray_kadane
)
from src.etapa2_closest_pair import (
    closest_pair_brute_force,
    closest_pair_divide_conquer
)


def run_etapa1_cli(args):
    if args.input:
        nums = [int(x) for x in args.input.strip().split()]
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read().strip().split()
            n = int(content[0])
            nums = [int(x) for x in content[1:n+1]]
    else:
        print("Digite os elementos separados por espaço:")
        nums = [int(x) for x in sys.stdin.readline().strip().split()]

    print(f"\nVetor de entrada ({len(nums)} elementos): {nums[:15]}{'...' if len(nums) > 15 else ''}")

    alg = args.alg.lower()
    if alg in ['bf', 'brute_force', 'forca_bruta']:
        s, i, f = max_subarray_brute_force(nums)
        nome = "Força Bruta O(n²)"
    elif alg in ['dc', 'divide_conquer', 'divisao_conquista']:
        s, i, f = max_subarray_divide_conquer(nums)
        nome = "Divisão e Conquista O(n log n)"
    elif alg in ['kd', 'kadane', 'linear']:
        s, i, f = max_subarray_kadane(nums)
        nome = "Kadane O(n) [Desafio]"
    else:
        print(f"Executando todos os 3 algoritmos para comparação...")
        s_bf, i_bf, f_bf = max_subarray_brute_force(nums)
        s_dc, i_dc, f_dc = max_subarray_divide_conquer(nums)
        s_kd, i_kd, f_kd = max_subarray_kadane(nums)
        print(f"  [Força Bruta O(n²)]           -> Soma: {s_bf}, Início: {i_bf}, Fim: {f_bf}")
        print(f"  [Divisão e Conquista O(n log n)] -> Soma: {s_dc}, Início: {i_dc}, Fim: {f_dc}")
        print(f"  [Kadane O(n) - Desafio]       -> Soma: {s_kd}, Início: {i_kd}, Fim: {f_kd}")
        return

    print(f"\nResultado [{nome}]:")
    print(f"  Soma Máxima: {s}")
    print(f"  Índice Início: {i}")
    print(f"  Índice Fim: {f}")
    print(f"  Subarranjo: {nums[i:f+1]}")


def run_etapa2_cli(args):
    points = []
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            tokens = f.read().strip().split()
            n = int(tokens[0])
            coords = [float(x) for x in tokens[1:2*n+1]]
            points = [(coords[2*i], coords[2*i+1]) for i in range(n)]
    else:
        print("Digite os pares x y (linha por linha, finalize com Ctrl+D/Ctrl+Z ou digite 'fim'):")
        for line in sys.stdin:
            line = line.strip()
            if not line or line.lower() == 'fim':
                break
            parts = line.split()
            if len(parts) >= 2:
                points.append((float(parts[0]), float(parts[1])))

    if len(points) < 2:
        print("Erro: São necessários pelo menos 2 pontos.")
        return

    print(f"\nTotal de pontos carregados: {len(points)}")

    alg = args.alg.lower()
    if alg in ['bf', 'brute_force', 'forca_bruta']:
        d, pair = closest_pair_brute_force(points)
        nome = "Força Bruta O(n²)"
    elif alg in ['dc', 'divide_conquer', 'divisao_conquista']:
        d, pair = closest_pair_divide_conquer(points, threshold=args.threshold)
        nome = f"Divisão e Conquista O(n log n) [Limiar={args.threshold}]"
    else:
        print("Executando ambos os algoritmos para comparação...")
        d_bf, p_bf = closest_pair_brute_force(points)
        d_dc, p_dc = closest_pair_divide_conquer(points, threshold=args.threshold)
        print(f"  [Força Bruta O(n²)]           -> Distância: {d_bf:.6f}, Par: {p_bf}")
        print(f"  [Divisão e Conquista O(n log n)] -> Distância: {d_dc:.6f}, Par: {p_dc}")
        return

    print(f"\nResultado [{nome}]:")
    print(f"  Distância Mínima: {d:.6f}")
    print(f"  Estações / Par Mais Próximo: {pair}")


def main():
    parser = argparse.ArgumentParser(
        description="Trabalho Prático: Divisão e Conquista"
    )
    parser.add_argument("--etapa", type=int, choices=[1, 2], help="Etapa a ser executada (1 ou 2)")
    parser.add_argument("--alg", type=str, default="all", help="Algoritmo: 'bf', 'dc', 'kd', ou 'all'")
    parser.add_argument("--input", type=str, help="Sequência de números para a Etapa 1 em string")
    parser.add_argument("--file", type=str, help="Caminho para arquivo de entrada de dados")
    parser.add_argument("--threshold", type=int, default=3, help="Limiar de parada para D&C da Etapa 2 (padrão: 3)")
    parser.add_argument("--test", action="store_true", help="Executa a bateria de testes automatizados")
    parser.add_argument("--benchmark", action="store_true", help="Executa medições de desempenho e gera CSVs")
    parser.add_argument("--plot", action="store_true", help="Gera os gráficos baseados nos CSVs")
    parser.add_argument("--report", action="store_true", help="Compila o relatório final em PDF")

    args = parser.parse_args()

    if args.test:
        import unittest
        loader = unittest.TestLoader()
        tests = loader.discover('tests')
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(tests)
        return

    if args.benchmark:
        from benchmarks.run_benchmarks import main as run_b
        run_b()
        return

    if args.plot:
        from benchmarks.plot_graphs import main as run_p
        run_p()
        return

    if args.report:
        from report.generate_pdf_report import main as gen_r
        gen_r()
        return

    if args.etapa == 1:
        run_etapa1_cli(args)
    elif args.etapa == 2:
        run_etapa2_cli(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
