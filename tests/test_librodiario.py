import unittest
from datetime import datetime
from librodiario import LibroDiario  # Asumiendo que el código anterior está en 'librodiario.py'


class TestLibroDiario(unittest.TestCase):

    def setUp(self):
        """Inicializa el objeto LibroDiario antes de cada prueba."""
        self.libro = LibroDiario()

    def test_agregar_transaccion_ingreso_valido(self):
        """Prueba que se agregue correctamente una transacción de tipo 'ingreso'."""
        self.libro.agregar_transaccion("10/10/2024", "Venta producto", 1000.0, "ingreso")
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 1000.0)
        self.assertEqual(resumen["egresos"], 0.0)

    def test_agregar_transaccion_egreso_valido(self):
        """Prueba que se agregue correctamente una transacción de tipo 'egreso'."""
        self.libro.agregar_transaccion("12/10/2024", "Compra material", 500.0, "egreso")
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 0.0)
        self.assertEqual(resumen["egresos"], 500.0)

    def test_tipo_transaccion_invalido(self):
        """Prueba que se lance un error si el tipo de transacción es inválido."""
        with self.assertRaises(ValueError):
            self.libro.agregar_transaccion("15/10/2024", "Pago servicio", 300.0, "pago")

    def test_calcular_resumen_con_varias_transacciones(self):
        """Prueba que el resumen se calcule correctamente con varias transacciones."""
        self.libro.agregar_transaccion("20/10/2024", "Venta producto", 1500.0, "ingreso")
        self.libro.agregar_transaccion("22/10/2024", "Compra material", 700.0, "egreso")
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 1500.0)
        self.assertEqual(resumen["egresos"], 700.0)


if __name__ == "__main__":
    unittest.main()
