import unittest
import math
import random
from src.etapa2_closest_pair import (
    closest_pair_brute_force,
    closest_pair_divide_conquer,
    euclidean_distance
)


class TestEtapa2ClosestPair(unittest.TestCase):

    def test_caso_borda_tamanho_2(self):
        pts = [(1.0, 2.0), (4.0, 6.0)]
        d_esperada = 5.0
        d_bf, pair_bf = closest_pair_brute_force(pts)
        d_dc, pair_dc = closest_pair_divide_conquer(pts)

        self.assertAlmostEqual(d_bf, d_esperada, places=6)
        self.assertAlmostEqual(d_dc, d_esperada, places=6)

    def test_caso_borda_tamanho_3(self):
        pts = [(0.0, 0.0), (10.0, 10.0), (0.0, 1.0)]
        d_esperada = 1.0
        d_bf, pair_bf = closest_pair_brute_force(pts)
        d_dc, pair_dc = closest_pair_divide_conquer(pts)

        self.assertAlmostEqual(d_bf, d_esperada, places=6)
        self.assertAlmostEqual(d_dc, d_esperada, places=6)

    def test_caso_borda_pontos_coincidentes(self):
        pts = [(5.0, 5.0), (1.0, 2.0), (5.0, 5.0), (10.0, 20.0)]
        d_bf, pair_bf = closest_pair_brute_force(pts)
        d_dc, pair_dc = closest_pair_divide_conquer(pts)

        self.assertAlmostEqual(d_bf, 0.0, places=6)
        self.assertAlmostEqual(d_dc, 0.0, places=6)

    def test_caso_borda_multiplos_coincidentes(self):
        pts = [(0.0, 0.0), (0.0, 0.0), (7.0, 7.0), (7.0, 7.0)]
        d_bf, _ = closest_pair_brute_force(pts)
        d_dc, _ = closest_pair_divide_conquer(pts)

        self.assertAlmostEqual(d_bf, 0.0, places=6)
        self.assertAlmostEqual(d_dc, 0.0, places=6)

    def test_caso_borda_alinhamento_horizontal(self):
        pts = [(10.0, 5.0), (2.0, 5.0), (4.5, 5.0), (20.0, 5.0)]
        d_bf, _ = closest_pair_brute_force(pts)
        d_dc, _ = closest_pair_divide_conquer(pts)

        self.assertAlmostEqual(d_bf, 2.5, places=6)
        self.assertAlmostEqual(d_dc, 2.5, places=6)

    def test_caso_borda_alinhamento_vertical(self):
        pts = [(3.0, 15.0), (3.0, -2.0), (3.0, 0.0), (3.0, 100.0)]
        d_bf, _ = closest_pair_brute_force(pts)
        d_dc, _ = closest_pair_divide_conquer(pts)

        self.assertAlmostEqual(d_bf, 2.0, places=6)
        self.assertAlmostEqual(d_dc, 2.0, places=6)

    def test_coordenadas_negativas_e_flutuantes(self):
        pts = [
            (-100.5, -200.75),
            (50.25, 30.1),
            (-100.2, -200.75),
            (0.0, 0.0)
        ]
        d_bf, _ = closest_pair_brute_force(pts)
        d_dc, _ = closest_pair_divide_conquer(pts)

        self.assertAlmostEqual(d_bf, 0.3, places=6)
        self.assertAlmostEqual(d_dc, 0.3, places=6)

    def test_diferentes_limiares(self):
        pts = [
            (0, 0), (5, 5), (10, 10), (1, 1.2), (9, 9.1),
            (20, 20), (25, 25), (30, 30), (50, 50), (100, 100)
        ]
        d_bf, _ = closest_pair_brute_force(pts)

        for thresh in [2, 3, 4, 5, 8]:
            d_dc, _ = closest_pair_divide_conquer(pts, threshold=thresh)
            self.assertAlmostEqual(d_dc, d_bf, places=6,
                                   msg=f"Falha com limiar {thresh}")

    def test_amostras_aleatorias(self):
        random.seed(42)
        for _ in range(50):
            n = random.randint(4, 60)
            pts = [(random.uniform(-1000, 1000), random.uniform(-1000, 1000)) for _ in range(n)]
            d_bf, _ = closest_pair_brute_force(pts)
            d_dc, _ = closest_pair_divide_conquer(pts, threshold=3)
            self.assertAlmostEqual(d_dc, d_bf, places=6)


if __name__ == '__main__':
    unittest.main()
