import csv
import json
import os
import platform
import random
import sys
import time
from typing import Dict, List, Tuple
import statistics
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.etapa1_max_subarray import (
    max_subarray_brute_force,
    max_subarray_divide_conquer,
    max_subarray_kadane
)
from src.etapa2_closest_pair import (
    closest_pair_brute_force,
    closest_pair_divide_conquer
)


def get_machine_specs() -> Dict[str, str]:
    return {
        "processor": platform.processor() or "AMD Ryzen 5 3400G with Radeon Vega Graphics",
        "cpu_cores": "4 núcleos / 8 threads",
        "ram": "16 GB DDR4",
        "os": f"{platform.system()} {platform.release()} ({platform.version()})",
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


def run_benchmark_etapa1(sizes: List[int], repetitions: int = 5) -> Tuple[List[Dict], List[Dict]]:
    print(f"\n[1/3] Executando Benchmark da Etapa 1 (Tamanhos: {sizes}, Repetições: {repetitions})...")
    raw_data = []
    summary_data = []

    for n in sizes:
        print(f"  -> Testando Etapa 1 para n = {n}...")
        times_bf = []
        times_dc = []
        times_kd = []

        for rep in range(1, repetitions + 1):
            random.seed(1000 * n + rep)
            arr = [random.randint(-1000, 1000) for _ in range(n)]

            t0 = time.perf_counter()
            s_bf, i_bf, f_bf = max_subarray_brute_force(arr)
            t_bf = time.perf_counter() - t0
            times_bf.append(t_bf)
            raw_data.append({
                "etapa": "Etapa 1",
                "algoritmo": "Forca Bruta O(n^2)",
                "tamanho_n": n,
                "repeticao": rep,
                "tempo_segundos": t_bf,
                "resultado_soma": s_bf
            })

            t0 = time.perf_counter()
            s_dc, i_dc, f_dc = max_subarray_divide_conquer(arr)
            t_dc = time.perf_counter() - t0
            times_dc.append(t_dc)
            raw_data.append({
                "etapa": "Etapa 1",
                "algoritmo": "Divisao e Conquista O(n log n)",
                "tamanho_n": n,
                "repeticao": rep,
                "tempo_segundos": t_dc,
                "resultado_soma": s_dc
            })

            t0 = time.perf_counter()
            s_kd, i_kd, f_kd = max_subarray_kadane(arr)
            t_kd = time.perf_counter() - t0
            times_kd.append(t_kd)
            raw_data.append({
                "etapa": "Etapa 1",
                "algoritmo": "Kadane O(n) [Desafio]",
                "tamanho_n": n,
                "repeticao": rep,
                "tempo_segundos": t_kd,
                "resultado_soma": s_kd
            })

            assert s_bf == s_dc == s_kd, f"Divergência na soma para n={n}, rep={rep}"

        summary_data.append({
            "tamanho_n": n,
            "bf_media_s": statistics.mean(times_bf),
            "bf_desvio_s": statistics.stdev(times_bf) if len(times_bf) > 1 else 0.0,
            "dc_media_s": statistics.mean(times_dc),
            "dc_desvio_s": statistics.stdev(times_dc) if len(times_dc) > 1 else 0.0,
            "kd_media_s": statistics.mean(times_kd),
            "kd_desvio_s": statistics.stdev(times_kd) if len(times_kd) > 1 else 0.0,
        })

    return raw_data, summary_data


def run_benchmark_etapa2(sizes: List[int], repetitions: int = 5) -> Tuple[List[Dict], List[Dict]]:
    print(f"\n[2/3] Executando Benchmark da Etapa 2 (Tamanhos: {sizes}, Repetições: {repetitions})...")
    raw_data = []
    summary_data = []

    for n in sizes:
        print(f"  -> Testando Etapa 2 para n = {n}...")
        times_bf = []
        times_dc = []

        for rep in range(1, repetitions + 1):
            random.seed(2000 * n + rep)
            pts = [(random.uniform(-10000.0, 10000.0), random.uniform(-10000.0, 10000.0)) for _ in range(n)]

            t0 = time.perf_counter()
            d_bf, _ = closest_pair_brute_force(pts)
            t_bf = time.perf_counter() - t0
            times_bf.append(t_bf)
            raw_data.append({
                "etapa": "Etapa 2",
                "algoritmo": "Forca Bruta O(n^2)",
                "tamanho_n": n,
                "repeticao": rep,
                "tempo_segundos": t_bf,
                "distancia_minima": d_bf
            })

            t0 = time.perf_counter()
            d_dc, _ = closest_pair_divide_conquer(pts, threshold=3)
            t_dc = time.perf_counter() - t0
            times_dc.append(t_dc)
            raw_data.append({
                "etapa": "Etapa 2",
                "algoritmo": "Divisao e Conquista O(n log n)",
                "tamanho_n": n,
                "repeticao": rep,
                "tempo_segundos": t_dc,
                "distancia_minima": d_dc
            })

            assert math.isclose(d_bf, d_dc, abs_tol=1e-6), f"Divergência na distância para n={n}, rep={rep}"

        summary_data.append({
            "tamanho_n": n,
            "bf_media_s": statistics.mean(times_bf),
            "bf_desvio_s": statistics.stdev(times_bf) if len(times_bf) > 1 else 0.0,
            "dc_media_s": statistics.mean(times_dc),
            "dc_desvio_s": statistics.stdev(times_dc) if len(times_dc) > 1 else 0.0,
            "speedup_dc_sobre_bf": statistics.mean(times_bf) / statistics.mean(times_dc)
        })

    return raw_data, summary_data


def run_threshold_study(n: int = 3200, thresholds: List[int] = None, repetitions: int = 5) -> List[Dict]:
    if thresholds is None:
        thresholds = [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 128]
    print(f"\n[3/3] Avaliando sensibilidade ao Limiar na Etapa 2 (n={n}, Limiares={thresholds})...")

    results = []
    for th in thresholds:
        times = []
        for rep in range(1, repetitions + 1):
            random.seed(3000 * th + rep)
            pts = [(random.uniform(-10000.0, 10000.0), random.uniform(-10000.0, 10000.0)) for _ in range(n)]
            t0 = time.perf_counter()
            d, _ = closest_pair_divide_conquer(pts, threshold=th)
            times.append(time.perf_counter() - t0)

        results.append({
            "tamanho_n": n,
            "limiar_threshold": th,
            "tempo_medio_s": statistics.mean(times),
            "desvio_padrao_s": statistics.stdev(times) if len(times) > 1 else 0.0
        })
    return results


def run_crossover_study() -> List[Dict]:
    small_sizes = [2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128]
    reps = 15
    results = []

    for n in small_sizes:
        times_bf = []
        times_dc = []
        for rep in range(reps):
            random.seed(4000 * n + rep)
            pts = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
            t0 = time.perf_counter()
            closest_pair_brute_force(pts)
            times_bf.append(time.perf_counter() - t0)

            t0 = time.perf_counter()
            closest_pair_divide_conquer(pts, threshold=3)
            times_dc.append(time.perf_counter() - t0)

        results.append({
            "tamanho_n": n,
            "bf_media_s": statistics.mean(times_bf),
            "dc_media_s": statistics.mean(times_dc)
        })
    return results


def main():
    bench_dir = os.path.dirname(os.path.abspath(__file__))
    specs = get_machine_specs()

    specs_path = os.path.join(bench_dir, "configuracao_maquina.json")
    with open(specs_path, "w", encoding="utf-8") as f:
        json.dump(specs, f, indent=4, ensure_ascii=False)
    print(f"Configurações da máquina salvas em: {specs_path}")

    tamanhos_etapa1 = [100, 200, 400, 800, 1600, 3200, 6400]
    tamanhos_etapa2 = [100, 200, 400, 800, 1600, 3200, 6400]

    raw_e1, summary_e1 = run_benchmark_etapa1(tamanhos_etapa1, repetitions=5)
    raw_e2, summary_e2 = run_benchmark_etapa2(tamanhos_etapa2, repetitions=5)
    threshold_results = run_threshold_study(n=3200, repetitions=5)
    crossover_results = run_crossover_study()

    csv_e1_path = os.path.join(bench_dir, "benchmark_etapa1_bruto.csv")
    with open(csv_e1_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=raw_e1[0].keys())
        writer.writeheader()
        writer.writerows(raw_e1)

    csv_e1_resumo_path = os.path.join(bench_dir, "benchmark_etapa1_resumo.csv")
    with open(csv_e1_resumo_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=summary_e1[0].keys())
        writer.writeheader()
        writer.writerows(summary_e1)

    csv_e2_path = os.path.join(bench_dir, "benchmark_etapa2_bruto.csv")
    with open(csv_e2_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=raw_e2[0].keys())
        writer.writeheader()
        writer.writerows(raw_e2)

    csv_e2_resumo_path = os.path.join(bench_dir, "benchmark_etapa2_resumo.csv")
    with open(csv_e2_resumo_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=summary_e2[0].keys())
        writer.writeheader()
        writer.writerows(summary_e2)

    csv_th_path = os.path.join(bench_dir, "benchmark_etapa2_limiares.csv")
    with open(csv_th_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=threshold_results[0].keys())
        writer.writeheader()
        writer.writerows(threshold_results)

    csv_cross_path = os.path.join(bench_dir, "benchmark_etapa2_crossover.csv")
    with open(csv_cross_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=crossover_results[0].keys())
        writer.writeheader()
        writer.writerows(crossover_results)

    print("\nTodos os benchmarks foram executados e os CSVs foram gerados com sucesso!")


if __name__ == "__main__":
    main()
