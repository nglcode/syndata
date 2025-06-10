# core/history_generator.py (Versión Final y Verificada)
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
from .patient import Patient, _generate_random_date

fake = Faker("es_ES")


class HistoryGenerator:
    """Genera el historial clínico narrativo para una lista de pacientes."""

    def __init__(self, config):
        self.config = config
        self.next_note_id = 3000000
        self.next_report_id = 7000000

        # --- BLOQUE DE CÓDIGO CORREGIDO Y RESTAURADO ---
        # Convierte las fechas de config a objetos datetime al inicio para ser usados en toda la clase
        try:
            self.fecha_minima_eventos_dt = datetime.strptime(self.config.FECHA_MINIMA_EVENTOS, "%Y-%m-%d")
            self.fecha_maxima_eventos_dt = datetime.strptime(self.config.FECHA_MAXIMA_EVENTOS, "%Y-%m-%d")
            with open("templates/informe_clinico_template.html", "r", encoding="utf-8") as f:
                self.report_template = f.read()
        except FileNotFoundError:
            print("ERROR FATAL: No se encontró 'informe_clinico_template.html' en la carpeta 'templates'.")
            raise
        except ValueError:
            print("ERROR FATAL: El formato de las fechas en config.py debe ser 'YYYY-MM-DD'.")
            raise
        # ---------------------------------------------

    def _generar_descripcion_proceso(self, tipo_acto: str, servicio: str) -> str:
        if tipo_acto == "URGENCIAS":
            return "PROCESO URGENCIAS"
        if tipo_acto == "ANALITICA":
            return "LABORATORIO"
        if tipo_acto == "HOSPITALIZACION":
            return f"HOSPITALIZACION {servicio.upper()}"
        return f"Consultas Externas {servicio}"

    def generate_full_history_for_all(self, patients: list[Patient]) -> dict:
        data = {
            "allergies": [],
            "appointments": [],
            "clinical_acts": [],
            "observations": [],
            "progress_notes": [],
            "clinical_reports": [],
        }
        data["allergies"] = self._create_allergies_for_all(patients)
        for patient in patients:
            self._simulate_patient_timeline(patient, data)
            self._generate_future_appointments(patient, data)
        return data

    def _simulate_patient_timeline(self, patient: Patient, data: dict):
        start_year = max(patient.fechaNacimiento.year + 18, self.fecha_minima_eventos_dt.year)
        end_year = self.fecha_maxima_eventos_dt.year
        for year in range(start_year, end_year + 1):
            current_date_approx = datetime(year, random.randint(1, 12), random.randint(1, 28))
            self._check_for_new_diagnosis(patient, current_date_approx)
            for patologia_nombre, estado_info in list(patient.estado_patologias.items()):
                estado_actual_key = estado_info["estado"]
                config_estado_actual = estado_info["info"]["estados"][estado_actual_key]
                frec_min, frec_max = config_estado_actual["frecuencia_anual"]
                num_eventos_este_ano = random.randint(frec_min, frec_max)
                for _ in range(num_eventos_este_ano):
                    self._generate_event_for_state(patient, patologia_nombre, estado_info, data, current_date_approx)
                self._check_for_state_transition(patient, patologia_nombre, estado_info, current_date_approx)

    def _check_for_new_diagnosis(self, patient: Patient, current_date: datetime):
        if random.random() < 0.08:
            possible_conditions = patient.profile["posibles_condiciones"]
            for cond_config in possible_conditions:
                if cond_config["nombre"] not in patient.estado_patologias:
                    key = next(
                        (
                            k
                            for k, v in self.config.CONDICIONES_CLINICAS.items()
                            if v["nombre"] == cond_config["nombre"]
                        ),
                        None,
                    )
                    if key:
                        patient.diagnose_condition(key, current_date)
                        break

    def _check_for_state_transition(
        self, patient: Patient, patologia_nombre: str, estado_info: dict, current_date: datetime
    ):
        config_estado_actual = estado_info["info"]["estados"][estado_info["estado"]]
        for transicion in config_estado_actual.get("transiciones", []):
            if "tras_meses" in transicion and current_date > estado_info["desde_fecha"] + relativedelta(
                months=+transicion["tras_meses"]
            ):
                estado_info["estado"] = transicion["al_estado"]
                estado_info["desde_fecha"] = current_date
                break
            if "probabilidad_anual" in transicion and random.random() < transicion["probabilidad_anual"]:
                estado_info["estado"] = transicion["al_estado"]
                estado_info["desde_fecha"] = current_date
                break

    def _generate_event_for_state(
        self, patient: Patient, patologia_nombre: str, estado_info: dict, data: dict, approx_date: datetime
    ):
        estado_actual_key = estado_info["estado"]
        config_estado_actual = estado_info["info"]["estados"][estado_actual_key]
        if not config_estado_actual["procedimientos"]:
            return
        proc_obj = random.choice(config_estado_actual["procedimientos"])
        procedimiento, tipo_acto = proc_obj["nombre"], proc_obj["tipo_acto"]
        servicio = random.choice(estado_info["info"]["servicios_predominantes"])

        if servicio in patient.servicios_visitados:
            prestacion = random.choice([p for p in self.config.PRESTACIONES_CITA if "PRIMERA" not in p])
        else:
            prestacion = "PRIMERA VISITA"
            patient.servicios_visitados.add(servicio)

        event_date = approx_date - relativedelta(days=random.randint(0, 30))

        data["appointments"].append(
            {
                "idPaciente": patient.medicalRecord,
                "fecha": event_date.strftime("%d/%m/%Y"),
                "prestacion": prestacion,
                "estado": "CERRADO",
                "realizada": "Sí",
                "servicio": servicio,
            }
        )
        data["clinical_acts"].append(
            {
                "idPaciente": patient.medicalRecord,
                "tipo": tipo_acto,
                "diagnosticos": patologia_nombre.upper(),
                "procedimientos": procedimiento,
                "servicio": servicio,
                "fechaAtencion": event_date,
                "fechaAlta": event_date + relativedelta(hours=random.randint(1, 4)),
                "motivoBajaLeq": None,
            }
        )

        observaciones_especificas = proc_obj.get("observaciones", []) + estado_info["info"].get(
            "observaciones_clave", []
        )
        obs_to_add = set(observaciones_especificas)
        if tipo_acto == "URGENCIAS":
            obs_to_add.update(self.config.OBS_VITALES + self.config.OBS_URGENCIAS_ADMIN)
        elif tipo_acto == "HOSPITALIZACION":
            obs_to_add.update(self.config.OBS_VITALES + self.config.OBS_VALORACION_GENERAL)
        else:
            obs_to_add.update(["TAS_GEN", "TAD_GEN"])

        for code in obs_to_add:
            obs_template = self.config.OBSERVACIONES_DB.get(code)
            if obs_template:
                valor_generado = self._get_observation_value(code, obs_template, patient, data, estado_info, event_date)
                observation_record = {
                    "idPaciente": patient.medicalRecord,
                    "codigo": code,
                    "codigoEstandar": obs_template.get("codigoEstandar"),
                    "codigoEstandarAlternativo": None,
                    "nombre": obs_template.get("nombre"),
                    "codigoDepartamento": obs_template.get("codigoDepartamento"),
                    "nombreDepartamento": obs_template.get("nombreDepartamento"),
                    "fechaToma": event_date,
                    "valorAnormalMin": obs_template.get("valorAnormalMin"),
                    "valorAnormalMax": obs_template.get("valorAnormalMax"),
                    "valorErrorMin": obs_template.get("valorErrorMin"),
                    "valorErrorMax": obs_template.get("valorErrorMax"),
                    "valor": valor_generado,
                    "interpretacion": random.choice(obs_template.get("posibles_interpretaciones", [""])),
                    "validada": random.choices(["Validada", "No Validada"], weights=[95, 5], k=1)[0],
                    "comentario": random.choice(obs_template.get("posibles_comentarios", [""])),
                    "unidad": obs_template.get("unidad", ""),
                    "descripcionProceso": self._generar_descripcion_proceso(tipo_acto, servicio),
                }
                data["observations"].append(observation_record)

        usuario = f"{fake.first_name()} {fake.last_name()}"
        contenido_nota = f"<p>Paciente de {patient.get_age_at_date(event_date)} años. {config_estado_actual.get('texto_evolucion', 'Seguimiento.')}</p>"
        data["progress_notes"].append(
            {
                "idNota": self.next_note_id,
                "contenido": contenido_nota,
                "idPaciente": patient.medicalRecord,
                "nombrePlantilla": f"Evolución {servicio.split()[0]}",
                "descripcionProceso": self._generar_descripcion_proceso(tipo_acto, servicio),
                "fechaCreacion": event_date,
                "fechaModificacion": event_date,
                "usuarioCreador": usuario,
                "usuarioModificador": usuario,
            }
        )
        self.next_note_id += 1

        if random.random() < self.config.PROBABILIDAD_INFORME_CLINICO:
            self._generate_clinical_report(patient, event_date, estado_info, servicio, procedimiento, data)

    def _generate_clinical_report(
        self, patient: Patient, event_date: datetime, estado_info: dict, servicio: str, procedimiento: str, data: dict
    ):
        estado_actual_key = estado_info["estado"]
        config_estado_actual = estado_info["info"]["estados"][estado_actual_key]
        antecedentes_pasados = [
            dx_info["info"]["nombre"]
            for dx_nombre, dx_info in patient.estado_patologias.items()
            if dx_info["desde_fecha"] < event_date
        ]
        info_centro = self.config.CENTROS_INFO[patient.centroRef]
        jefe_sexo = random.choice(["male", "female"])
        jefatura_completa = f"{'Dra.' if jefe_sexo == 'female' else 'Dr.'} {fake.first_name_female() if jefe_sexo == 'female' else fake.first_name_male()} {fake.last_name()}"
        texto_evolucion_actual = config_estado_actual.get("texto_evolucion", "Evolución sin incidencias.")
        tratamiento_actual = config_estado_actual.get(
            "tratamiento_recomendado", "Mantener tratamiento y seguimiento habitual."
        )
        replacements = {
            "{{ANTECEDENTES_PERSONALES}}": ", ".join(antecedentes_pasados) or "Sin antecedentes de interés.",
            "{{TRATAMIENTO_RECOMENDADO}}": tratamiento_actual,
            "{{ANAMNESIS}}": texto_evolucion_actual,
            "{{DIAGNOSTICO_PRINCIPAL}}": estado_info["info"]["nombre"].upper(),
            "{{MOTIVO_INGRESO}}": estado_info["info"]["nombre"],
            "{{PACIENTE_NOMBRE}}": f"{patient.nombre} {patient.apellido}",
            "{{FECHA_INFORME}}": event_date.strftime("%d/%m/%Y"),
            "{{NHC}}": str(patient.medicalRecord),
            "{{SERVICIO_MEDICO}}": servicio.upper(),
            "{{ALERGIAS}}": ", ".join(
                [a["descripcion"] for a in data["allergies"] if a["idPaciente"] == patient.medicalRecord]
            )
            or "No conocidas",
            "{{PROCEDIMIENTOS}}": procedimiento,
            "{{JEFATURA_SERVICIO}}": jefatura_completa,
            "{{CENTRO_DIRECCION}}": info_centro["direccion"],
            "{{CENTRO_MUNICIPIO}}": info_centro["municipio"],
            "{{CENTRO_CP}}": info_centro["codigo_postal"],
        }
        informe_contenido = self.report_template
        for placeholder, value in replacements.items():
            informe_contenido = informe_contenido.replace(placeholder, str(value))
        data["clinical_reports"].append(
            {
                "idInforme": self.next_report_id,
                "contenido": informe_contenido,
                "fechaCreacion": event_date,
                "fechaModificacion": event_date,
                "usuarioCreador": "Administrador XYZ XYZ",
                "usuarioModificador": "Administrador XYZ XYZ",
                "idPaciente": patient.medicalRecord,
            }
        )
        self.next_report_id += 1

    def _generate_future_appointments(self, patient: Patient, data: dict):
        if patient.profile_key == "sano":
            return
        today, future_limit = datetime.now(), datetime.now() + relativedelta(months=+self.config.MESES_FUTURO_CITAS)
        for _ in range(random.randint(1, 3)):
            future_date = _generate_random_date(today, future_limit)
            condicion_futura_obj = random.choice(patient.profile["posibles_condiciones"])
            servicio_futuro = random.choice(condicion_futura_obj["servicios_predominantes"])
            prestacion_futura = random.choice([p for p in self.config.PRESTACIONES_CITA if "PRIMERA" not in p])
            data["appointments"].append(
                {
                    "idPaciente": patient.medicalRecord,
                    "fecha": future_date.strftime("%d/%m/%Y"),
                    "prestacion": prestacion_futura,
                    "estado": "PROGRAMADO",
                    "realizada": "No",
                    "servicio": servicio_futuro,
                }
            )

    def _create_allergies_for_all(self, patients: list[Patient]) -> list[dict]:
        allergies_list = []
        for patient in patients:
            if random.random() < self.config.PROBABILIDAD_ALERGIA:
                num_allergies = random.randint(1, 2)
                picked_allergies = random.sample(self.config.ALERGIAS_COMUNES, num_allergies)
                for allergy in picked_allergies:
                    start_date = max(patient.fechaNacimiento, self.fecha_minima_eventos_dt)
                    fecha_registro = _generate_random_date(start_date, self.fecha_maxima_eventos_dt)
                    allergies_list.append(
                        {
                            "idPaciente": patient.medicalRecord,
                            "descripcion": allergy["descripcion"],
                            "tipo": "ALERGIA",
                            "confirmada": random.choice(["SI", "NO"]),
                            "fechaAparicion": fecha_registro.strftime("%Y-%m-%d"),
                            "fechaRegistro": fecha_registro.strftime("%Y-%m-%d"),
                            "fechaBaja": None,
                            "observaciones": "",
                            "codigoCIE": allergy["codigo"],
                        }
                    )
        return allergies_list

    def _get_observation_value(
        self, code: str, template: dict, patient: Patient, data: dict, estado_info: dict, event_date: datetime
    ):
        valor_config = template.get("valor")
        if valor_config == "dinamico":
            if code == "ANT_PER_HIS_SICH_REH":
                alergias = [a["descripcion"] for a in data["allergies"] if a["idPaciente"] == patient.medicalRecord]
                patologias = list(patient.estado_patologias.keys())
                return (
                    f"Alergias: {', '.join(alergias) or 'No conocidas'}. AP: {', '.join(patologias) or 'Sin interés'}."
                )
            if code == "ANAM_ALTA_SICH_REH" or code == "EVO_ALTA_SICH_REH":
                return estado_info["info"]["estados"][estado_info["estado"]].get("texto_evolucion", "Sin incidencias.")
        return valor_config() if callable(valor_config) else valor_config
