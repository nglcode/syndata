# core/patient.py (Versión Final y Verificada)
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
from faker.exceptions import UniquenessException

fake = Faker('es_ES')

def _generate_random_date(start, end):
    if isinstance(start, str): start = datetime.strptime(start, '%Y-%m-%d')
    if isinstance(end, str): end = datetime.strptime(end, '%Y-%m-%d')
    if start > end: return start
    delta = end - start
    random_delta = random.randint(0, delta.days)
    return start + relativedelta(days=random_delta)

class Patient:
    """Representa a un paciente sintético con todos sus datos y estado evolutivo."""
    def __init__(self, config):
        self.config = config
        self._set_profile()
        self._generate_demographics()
        self.servicios_visitados = set()
        self.estado_patologias = {}
        if self.profile_key == "sano":
            self.diagnose_condition("chequeo", self.fechaNacimiento + relativedelta(years=18))

    def _set_profile(self):
        profiles = list(self.config.PERFILES.keys())
        probabilities = [p['probabilidad'] for p in self.config.PERFILES.values()]
        self.profile_key = random.choice(profiles)
        self.profile = self.config.PERFILES[self.profile_key]

    def _generate_demographics(self):
        centros_nombres = list(self.config.CENTROS_INFO.keys())
        self.sexo = random.choice(["Hombre", "Mujer"])
        self.nombre = fake.first_name_female() if self.sexo == "Mujer" else fake.first_name_male()
        self.apellido = f"{fake.last_name()} {fake.last_name()}"
        self.fechaNacimiento = _generate_random_date(self.config.FECHA_NACIMIENTO_MIN, self.config.FECHA_NACIMIENTO_MAX)
        try:
            self.medicalRecord = fake.unique.random_number(digits=6)
            self.numExpediente = fake.unique.random_number(digits=7)
        except UniquenessException:
            print("ERROR: Se han agotado los IDs únicos. Intenta generar menos pacientes.")
            raise
        self.centroRef = random.choice(centros_nombres)
        self.regimenSS = random.choice(self.config.REGIMENES_SS)
        self.paisResidencia = "ESPAÑA"
        self.nacionalidad = "ESPAÑA"

    def diagnose_condition(self, condition_key: str, diagnosis_date: datetime):
        condition_info = self.config.CONDICIONES_CLINICAS[condition_key]
        if condition_info["nombre"] not in self.estado_patologias:
            initial_state = next(iter(condition_info["estados"]))
            self.estado_patologias[condition_info["nombre"]] = {
                "estado": initial_state,
                "desde_fecha": diagnosis_date,
                "info": condition_info
            }

    def get_age_at_date(self, event_date: datetime) -> int:
        return event_date.year - self.fechaNacimiento.year - ((event_date.month, event_date.day) < (self.fechaNacimiento.month, self.fechaNacimiento.day))

    def to_dict(self) -> dict:
        return {"medicalRecord": self.medicalRecord, "centroRef": self.centroRef, "fechaNacimiento": self.fechaNacimiento, "regimenSS": self.regimenSS, "numExpediente": self.numExpediente, "sexo": self.sexo, "paisResidencia": self.paisResidencia, "nacionalidad": self.nacionalidad, "nombre": self.nombre, "apellido": self.apellido}