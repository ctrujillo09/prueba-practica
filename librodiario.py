"""Programa para gestionar ingresos y egresos."""

from datetime import datetime
from typing import List, Dict
import logging
import traceback

# Configuración de logging
logging.basicConfig(
    filename='logs/log_contable.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


class MontoInvalidoError(Exception):
    """Excepción lanzada cuando el monto es cero o negativo."""
    pass


class LibroDiario:
    """Gestión contable básica de ingresos y egresos."""

    def _init_(self):
        self.transacciones: List[Dict] = []

    def agregar_transaccion(
        self, fecha: str, descripcion: str, monto: float, tipo: str) -> None:
        """Agrega una transacción con manejo de errores."""
        try:
            if tipo.lower() not in ("ingreso", "egreso"):
                raise ValueError(
                    "Tipo de transacción inválido, debe ser 'ingreso' o 'egreso'."
                )

            # Validar formato de fecha
            try:
                fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError as exc:
                raise ValueError(
                    "Formato de fecha inválido, debe usar: yyyy-mm-dd."
                ) from exc

            # Validar monto
            if monto <= 0:
                raise MontoInvalidoError("El monto debe ser mayor a cero.")

            transaccion = {
                "fecha": fecha_dt,
                "descripcion": descripcion,
                "monto": monto,
                "tipo": tipo.lower()
            }
            self.transacciones.append(transaccion)

            logging.info(
                "Transacción registrada: %s | %s | %.2f | %s",
                fecha, descripcion, monto, tipo
            )

        except (ValueError, MontoInvalidoError) as error:
            error_line = traceback.format_exc().strip().splitlines()[-1]
            logging.error("%s - Línea: %s", error, error_line)
            print(f"[ERROR] {error}")

    def cargar_transacciones_desde_archivo(self, path: str) -> None:
        """Carga transacciones desde un archivo .csv (separado por ;) y registra errores."""
        try:
            with open(path, "r", encoding="utf-8") as archivo:
                for linea_nro, linea in enumerate(archivo, start=1):
                    partes = linea.strip().split(";")

                    # Verificar que tenga 4 columnas
                    if len(partes) != 4:
                        logging.error(
                            "Línea %d: Formato incorrecto -> %s",
                            linea_nro,
                            linea.strip()
                        )
                        continue

                    fecha, descripcion, monto_str, tipo = partes

                    try:
                        monto = float(monto_str)
                        self.agregar_transaccion(fecha, descripcion, monto, tipo)
                    except (ValueError, MontoInvalidoError) as error:
                        error_line = traceback.format_exc().strip().splitlines()[-1]
                        logging.error(
                            "Línea %d: %s - Línea: %s",
                            linea_nro,
                            error,
                            error_line
                        )
        except FileNotFoundError:
            logging.critical("No se encontró el archivo: %s", path)
            print(f"[CRÍTICO] No se encontró el archivo: {path}")

    def calcular_resumen(self) -> Dict[str, float]:
        """Devuelve el resumen total de ingresos y egresos."""
        resumen = {"ingresos": 0.0, "egresos": 0.0}
        for transaccion in self.transacciones:
            if transaccion["tipo"] == "ingreso":
                resumen["ingresos"] += transaccion["monto"]
            else:
                resumen["egresos"] += transaccion["monto"]
        return resumen

    def exportar_resumen(self, path: str) -> None:
        """Exporta el resumen contable a un archivo especificado."""
        resumen = self.calcular_resumen()
        try:
            with open(path, "w", encoding="utf-8") as archivo:
                archivo.write("Resumen contable:\n")
                archivo.write(
                    f"Total ingresos: {resumen['ingresos']:.2f}\n"
                )
                archivo.write(
                    f"Total egresos: {resumen['egresos']:.2f}\n"
                )
            logging.info("Resumen exportado correctamente a %s", path)
        except OSError as error:
            error_line = traceback.format_exc().strip().splitlines()[-1]
            logging.error(
                "Error al exportar resumen: %s - Línea: %s",
                error,
                error_line
            )
            print(f"[ERROR] No se pudo exportar el resumen: {error}")