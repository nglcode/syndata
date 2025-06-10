# core/reporter.py (Versión Final y Verificada)
from datetime import datetime
import pandas as pd
from collections import Counter
from .patient import Patient 

class Reporter:
    """Analiza los datos generados, valida la coherencia y genera informes."""
    def __init__(self, patients: list[Patient], history_data: dict, config: object):
        self.patients = patients
        self.history = history_data
        self.config = config
        self.errors = []
        self.stats = {}

    def run_all_reports(self):
        print("\n--- INICIANDO FASE DE VALIDACIÓN Y ESTADÍSTICAS ---")
        self._validate_data()
        self._calculate_stats()
        self._print_report()

    def _validate_data(self):
        min_event_date = datetime.strptime(self.config.FECHA_MINIMA_EVENTOS, '%Y-%m-%d')
        for act in self.history['clinical_acts']:
            patient = next((p for p in self.patients if p.medicalRecord == act['idPaciente']), None)
            if not patient: continue
            if act['fechaAtencion'] < patient.fechaNacimiento or act['fechaAtencion'] < min_event_date:
                self.errors.append(f"Error Temporal: Acto {act['tipo']} para paciente {patient.medicalRecord} antes de fecha válida.")
        
        app_df = pd.DataFrame(self.history['appointments'])
        if not app_df.empty:
            first_visits = app_df[app_df['prestacion'].str.contains("PRIMERA VISITA", na=False)]
            if not first_visits.empty:
                duplicated_first_visits = first_visits[first_visits.duplicated(subset=['idPaciente', 'servicio'], keep=False)]
                if not duplicated_first_visits.empty:
                    self.errors.append(f"Error de Duplicidad: {len(duplicated_first_visits)} 'PRIMERA VISITA' duplicadas encontradas.")

    def _calculate_stats(self):
        self.stats['total_pacientes'] = len(self.patients)
        self.stats['genero'] = Counter(p.sexo for p in self.patients)
        acts_df = pd.DataFrame(self.history['clinical_acts'])
        if not acts_df.empty: self.stats['distribucion_actos'] = acts_df['tipo'].value_counts().to_dict()
        ages = [p.get_age_at_date(datetime.now()) for p in self.patients]
        bins = [0, 18, 40, 65, 120]
        labels = ["0-17", "18-39", "40-64", "65+"]
        age_groups = pd.cut(ages, bins=bins, labels=labels, right=False)
        self.stats['distribucion_edad'] = age_groups.value_counts().sort_index().to_dict()

    def _print_report(self):
        if self.errors:
            print(f"\n[VALIDACIÓN] Se encontraron {len(self.errors)} errores:")
            for error in self.errors[:5]: print(f"  - {error}")
        else: print("\n[VALIDACIÓN] OK - No se encontraron errores de coherencia.")
        print("\n[ESTADÍSTICAS] Resumen de los datos generados:")
        if 'distribucion_actos' in self.stats:
            print("  - Distribución de Actos Clínicos:")
            for tipo, count in self.stats['distribucion_actos'].items(): print(f"    - {tipo}: {count}")
        print("  - Distribución por Género:")
        for genero, count in self.stats['genero'].items(): print(f"    - {genero}: {count}")

    def generate_patient_summary_file(self):
        print("\nGenerando archivo de resumen de pacientes (pacientes_resumen.txt)...")
        try:
            with open('output/pacientes_resumen.txt', 'w', encoding='utf-8') as f:
                for patient in self.patients:
                    f.write("="*40 + "\n")
                    f.write(f"ID Paciente: {patient.medicalRecord}\n")
                    f.write(f"Nombre: {patient.nombre} {patient.apellido}\n")
                    f.write(f"Edad: {patient.get_age_at_date(datetime.now())} años\n")
                    f.write(f"Género: {patient.sexo}\n")
                    alergias_paciente = [a['descripcion'] for a in self.history['allergies'] if a['idPaciente'] == patient.medicalRecord]
                    f.write(f"Alergias: {', '.join(alergias_paciente) or 'Ninguna conocida'}\n")
                    condiciones_paciente = list(patient.estado_patologias.keys())
                    f.write(f"Patologías Crónicas: {', '.join(condiciones_paciente) or 'Sano (solo chequeos)'}\n")
                
                f.write("\n\n" + "="*50 + "\n")
                f.write("RESUMEN ESTADÍSTICO GENERAL\n")
                f.write("="*50 + "\n")
                f.write(f"Número total de pacientes: {self.stats.get('total_pacientes', 0)}\n")
                f.write("\nDesglose por Género:\n")
                for genero, count in self.stats.get('genero', {}).items(): f.write(f"  - {genero}: {count}\n")
                f.write("\nDesglose por Rango de Edad:\n")
                if 'distribucion_edad' in self.stats:
                    for rango, count in self.stats.get('distribucion_edad', {}).items(): f.write(f"  - {rango}: {count}\n")
            print("Archivo 'pacientes_resumen.txt' generado con éxito.")
        except IOError as e: print(f"ERROR: No se pudo escribir el archivo de resumen. Detalle: {e}")