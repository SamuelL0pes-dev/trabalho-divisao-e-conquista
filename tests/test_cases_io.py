import json
import math
import os
import sys
import unittest

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


class TestCasesIOValidation(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test_cases'))
        with open(os.path.join(base_dir, 'etapa1_casos_teste.json'), 'r', encoding='utf-8') as f:
            self.casos_etapa1 = json.load(f)
        with open(os.path.join(base_dir, 'etapa2_casos_teste.json'), 'r', encoding='utf-8') as f:
            self.casos_etapa2 = json.load(f)

    def test_todos_casos_etapa1(self):
        for caso in self.casos_etapa1:
            arr = caso["entrada"]
            soma_exp = caso["soma_esperada"]
            ini_exp = caso["inicio_esperado"]
            fim_exp = caso["fim_esperado"]

            for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
                soma, ini, fim = alg(arr)
                self.assertEqual(soma, soma_exp, f"Erro em {caso['nome']} ({alg.__name__}): soma={soma} != {soma_exp}")
                self.assertEqual(ini, ini_exp, f"Erro em {caso['nome']} ({alg.__name__}): ini={ini} != {ini_exp}")
                self.assertEqual(fim, fim_exp, f"Erro em {caso['nome']} ({alg.__name__}): fim={fim} != {fim_exp}")

    def test_todos_casos_etapa2(self):
        for caso in self.casos_etapa2:
            pontos = [tuple(p) for p in caso["pontos"]]
            dist_exp = caso["distancia_esperada"]

            d_bf, _ = closest_pair_brute_force(pontos)
            d_dc, _ = closest_pair_divide_conquer(pontos, threshold=3)

            self.assertAlmostEqual(d_bf, dist_exp, places=5,
                                   msg=f"Erro BF em {caso['nome']}: {d_bf} != {dist_exp}")
            self.assertAlmostEqual(d_dc, dist_exp, places=5,
                                   msg=f"Erro DC em {caso['nome']}: {d_dc} != {dist_exp}")


if __name__ == '__main__':
    unittest.main()
