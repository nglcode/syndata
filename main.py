# main.py (Versión Final y Verificada)
import os
import argparse
import pandas as pd
import config
from core.patient import Patient
from core.history_generator import HistoryGenerator
from core.reporter import Reporter

def export_data_to_files(patients: list[Patient], history_data: dict):
    """Guarda todos los datos generados en archivos CSV."""
    print("\nGuardando archivos CSV en la carpeta 'output'...")
    separator = '|'
    try:
        patient_records = [p.to_dict() for p in patients]
        pd.DataFrame(patient_records).to_csv('output/patientdata.csv', index=False, sep=separator)
        for key, value in history_data.items():
            df = pd.DataFrame(value) if value else pd.DataFrame()
            if key == "appointments" and not df.empty:
                df['fecha_dt'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y', errors='coerce')
                df = df.sort_values(by=['idPaciente', 'fecha_dt']).drop(columns=['fecha_dt'])
            df.to_csv(f'output/{key.replace("_", "")}data.csv', index=False, sep=separator)
        print("Guardado de archivos CSV completado.")
        return True
    except IOError as e:
        print(f"ERROR: No se pudo escribir un archivo CSV. Comprueba los permisos. Detalle: {e}")
        return False

def _convert_csv_a_txt():
    """Función temporal para duplicar los CSV como TXT."""
    print("\nConvirtiendo archivos CSV a TXT...")
    output_dir = 'output'
    try:
        csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
        for file in csv_files:
            csv_path = os.path.join(output_dir, file)
            txt_path = os.path.join(output_dir, file.replace('.csv', '.txt'))
            df = pd.read_csv(csv_path, sep='|')
            df.to_csv(txt_path, sep='|', index=False)
        print("Conversión a TXT completada.")
    except Exception as e:
        print(f"Error durante la conversión a TXT: {e}")

def run_generator(num_pacientes_arg: int):
    """Orquesta todo el proceso de generación de datos."""
    print(f"Iniciando la generación de datos sintéticos (v5.3 - Final) para {num_pacientes_arg} pacientes...")
    if not os.path.exists('output'): os.makedirs('output')

    patients = [Patient(config) for _ in range(num_pacientes_arg)]
    history_generator = HistoryGenerator(config)
    full_history_data = history_generator.generate_full_history_for_all(patients)
    
    reporter = Reporter(patients, full_history_data, config)
    reporter.run_all_reports()

    if export_data_to_files(patients, full_history_data):
        reporter.generate_patient_summary_file()
        _convert_csv_a_txt()

    print("\n¡Proceso completado con éxito!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de Datos Médicos Sintéticos.")
    parser.add_argument("-p", "--pacientes", type=int, default=config.NUM_PACIENTES,
                        help=f"Número de pacientes a generar. Por defecto: {config.NUM_PACIENTES} (definido en config.py)")
    args = parser.parse_args()
    run_generator(args.pacientes)