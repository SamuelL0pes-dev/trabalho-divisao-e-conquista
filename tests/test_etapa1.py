import unittest
from src.etapa1_max_subarray import (
    max_subarray_brute_force,
    max_subarray_divide_conquer,
    max_subarray_kadane
)


class TestEtapa1MaxSubarray(unittest.TestCase):

    def test_caso_borda_apenas_negativos(self):
        arr = [-5, -2, -8, -12, -3]
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            soma, ini, fim = alg(arr)
            self.assertEqual(soma, -2, f"Falha no algoritmo {alg.__name__}")
            self.assertEqual(ini, 1, f"Falha no algoritmo {alg.__name__}")
            self.assertEqual(fim, 1, f"Falha no algoritmo {alg.__name__}")

    def test_caso_borda_tamanho_unitario_positivo(self):
        arr = [42]
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            soma, ini, fim = alg(arr)
            self.assertEqual(soma, 42)
            self.assertEqual(ini, 0)
            self.assertEqual(fim, 0)

    def test_caso_borda_tamanho_unitario_negativo(self):
        arr = [-99]
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            soma, ini, fim = alg(arr)
            self.assertEqual(soma, -99)
            self.assertEqual(ini, 0)
            self.assertEqual(fim, 0)

    def test_caso_borda_empate_mesma_soma(self):
        arr = [3, -5, 3]
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            soma, ini, fim = alg(arr)
            self.assertEqual(soma, 3)
            self.assertEqual(ini, 0)
            self.assertEqual(fim, 0)

    def test_caso_classico_cormen(self):
        arr = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            soma, ini, fim = alg(arr)
            self.assertEqual(soma, 43)
            self.assertEqual(ini, 7)
            self.assertEqual(fim, 10)

    def test_todos_positivos(self):
        arr = [1, 2, 3, 4, 5]
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            soma, ini, fim = alg(arr)
            self.assertEqual(soma, 15)
            self.assertEqual(ini, 0)
            self.assertEqual(fim, 4)

    def test_presenca_de_zeros(self):
        arr = [0, -1, 0, 5, 0, -2]
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            soma, ini, fim = alg(arr)
            self.assertEqual(soma, 5)
            self.assertEqual(ini, 3)
            self.assertEqual(fim, 3)

    def test_excecao_vetor_vazio(self):
        for alg in [max_subarray_brute_force, max_subarray_divide_conquer, max_subarray_kadane]:
            with self.assertRaises(ValueError):
                alg([])


if __name__ == '__main__':
    unittest.main()
