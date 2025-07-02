import unittest
from datetime import datetime
from librodiario import LibroDiario, MontoInvalidoError


class TestLibroDiario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicialización del objeto LibroDiario antes de todas las pruebas."""
        cls.libro = LibroDiario()

    def test_agregar_transaccion_ingreso_valido(self):
        """Prueba agregar una transacción válida de ingreso"""
        self.libro.agregar_transaccion("10/10/2024", "Venta de productos", 1000.0, "ingreso")
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 1000.0)
        self.assertEqual(resumen["egresos"], 0.0)

    def test_agregar_transaccion_egreso_valido(self):
        """Prueba agregar una transacción válida de egreso"""
        self.libro.agregar_transaccion("15/10/2024", "Compra de insumos", 500.0, "egreso")
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 0.0)
        self.assertEqual(resumen["egresos"], 500.0)

    def test_agregar_transaccion_tipo_invalido(self):
        """Prueba agregar una transacción con tipo inválido"""
        with self.assertRaises(ValueError):
            self.libro.agregar_transaccion("20/10/2024", "Error en transacción", 200.0, "invalid")

    def test_agregar_transaccion_fecha_invalida(self):
        """Prueba agregar una transacción con fecha en formato incorrecto"""
        with self.assertRaises(ValueError):
            self.libro.agregar_transaccion("2024/10/20", "Error de formato de fecha", 200.0, "ingreso")

    def test_agregar_transaccion_monto_invalido(self):
        """Prueba agregar una transacción con monto negativo"""
        with self.assertRaises(ValueError):
            self.libro.agregar_transaccion("20/10/2024", "Error en monto", -500.0, "egreso")

    def test_calcular_resumen_con_transacciones(self):
        """Prueba calcular el resumen con varias transacciones"""
        self.libro.agregar_transaccion("01/10/2024", "Venta de productos", 1500.0, "ingreso")
        self.libro.agregar_transaccion("05/10/2024", "Pago de alquiler", 700.0, "egreso")
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 1500.0)
        self.assertEqual(resumen["egresos"], 700.0)

    def test_calcular_resumen_sin_transacciones(self):
        """Prueba calcular el resumen sin transacciones"""
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 0.0)
        self.assertEqual(resumen["egresos"], 0.0)

    def test_agregar_transacciones_multipes(self):
        """Prueba agregar múltiples transacciones de manera sucesiva"""
        self.libro.agregar_transaccion("01/11/2024", "Venta de productos", 1200.0, "ingreso")
        self.libro.agregar_transaccion("02/11/2024", "Pago de proveedores", 400.0, "egreso")
        self.libro.agregar_transaccion("03/11/2024", "Cobro de cuentas por cobrar", 800.0, "ingreso")
        
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 2000.0)
        self.assertEqual(resumen["egresos"], 400.0)

    def test_agregar_transaccion_doble_tipo(self):
        """Prueba agregar dos transacciones del mismo tipo"""
        self.libro.agregar_transaccion("01/12/2024", "Venta de servicios", 1000.0, "ingreso")
        self.libro.agregar_transaccion("02/12/2024", "Pago de publicidad", 300.0, "egreso")
        
        resumen = self.libro.calcular_resumen()
        self.assertEqual(resumen["ingresos"], 1000.0)
        self.assertEqual(resumen["egresos"], 300.0)

    def test_excepcion_monto_invalido(self):
        """Prueba si se lanza la excepción MontoInvalidoError con monto negativo"""
        with self.assertRaises(MontoInvalidoError):
            self.libro.agregar_transaccion("25/10/2024", "Error con monto", -500.0, "ingreso")

    def test_transacciones_iniciadas_vacias(self):
        """Prueba que las transacciones inicien vacías"""
        libro_vacio = LibroDiario()
        self.assertEqual(libro_vacio.transacciones, [])

if __name__ == "__main__":
    unittest.main()
