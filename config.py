# config.py (Versión 7.0 - Definitiva con Variabilidad Total)
import random

# fmt: off
# --- CONFIGURACIÓN PRINCIPAL ---
NUM_PACIENTES = 50
FECHA_NACIMIENTO_MIN = "1940-01-01"
FECHA_NACIMIENTO_MAX = "2005-12-31"
FECHA_MINIMA_EVENTOS = "1990-01-01"
FECHA_MAXIMA_EVENTOS = "2025-06-09"
MESES_FUTURO_CITAS = 6
PROBABILIDAD_ALERGIA = 0.50
PROBABILIDAD_INFORME_CLINICO = 0.10

# --- DICCIONARIO DE CENTROS DE SALUD ---
CENTROS_INFO = {
    "C.S. Goya": {
        "direccion": "Calle de Goya, 99",
        "municipio": "Madrid",
        "provincia": "Madrid",
        "codigo_postal": "28009",
    },
    "C.S. Manso": {
        "direccion": "Carrer de Manso, 19",
        "municipio": "Barcelona",
        "provincia": "Barcelona",
        "codigo_postal": "08015",
    },
    "C.S. El Cachorro": {
        "direccion": "Calle de la Arquitectura, s/n",
        "municipio": "Sevilla",
        "provincia": "Sevilla",
        "codigo_postal": "41018",
    },
    "C.S. Torrent I": {
        "direccion": "Carrer de Sant Domènec, 10",
        "municipio": "Torrent",
        "provincia": "Valencia",
        "codigo_postal": "46900",
    },
    "C.S. Deusto": {
        "direccion": "Plaza de San Pedro, 1",
        "municipio": "Bilbao",
        "provincia": "Vizcaya",
        "codigo_postal": "48014",
    },
    "C.S. Actur Sur": {
        "direccion": "Calle de Pablo Ruiz Picasso, 60",
        "municipio": "Zaragoza",
        "provincia": "Zaragoza",
        "codigo_postal": "50018",
    },
    "C.S. La Rosaleda": {
        "direccion": "Avenida de la Palmilla, 17",
        "municipio": "Málaga",
        "provincia": "Málaga",
        "codigo_postal": "29011",
    },
    "C.S. San Andrés": {
        "direccion": "Plaza de San Agustín, 3",
        "municipio": "Murcia",
        "provincia": "Murcia",
        "codigo_postal": "30005",
    },
    "C.S. Can Misses": {
        "direccion": "Carrer de la Corona, s/n",
        "municipio": "Eivissa",
        "provincia": "Islas Baleares",
        "codigo_postal": "07800",
    },
    "C.S. Schamann": {
        "direccion": "Calle de Don Pío Coronado, 115",
        "municipio": "Las Palmas de Gran Canaria",
        "provincia": "Las Palmas",
        "codigo_postal": "35012",
    },
}

# --- GRUPOS DE OBSERVACIONES PARA FACILITAR LA ASIGNACIÓN ---
OBS_VITALES = ["TAS_GEN", "TAD_GEN", "FC_GEN", "TEM_GEN", "SAT_O2"]
OBS_HEMOGRAMA = ["100", "102", "104", "106", "108", "110", "112", "114", "130", "140", "148"]
OBS_BIOQUIMICA_BASICA = ["4022", "1419", "GLUC"]
OBS_PERFIL_TIROIDEO = ["3036", "3039"]
OBS_PERFIL_FERRICO = ["104", "108", "FERRITINA"]
OBS_PERFIL_LIPIDICO = ["COLESTEROL_TOTAL", "LDL", "HDL", "TRIGLICERIDOS"]
OBS_VALORACION_GENERAL = ["CUID_ENF_51", "CUID_ENF_53", "CUID_ENF_16", "CUID_ENF_8", "ALT_PESO_3_MESES", "DET_FUN_6_MESES", "HAB_TOX_GEN", "ALERGIAS_GEN"]
OBS_ESCALA_DOWNTON = ["ALTERAUDI_DOWNTON", "PCAI_PREVIAS_DOWNTON", "DIURET_DOWNTON"]
OBS_URGENCIAS_ADMIN = ["PACIENTE_URGENCIAS", "RAD_F_ACCES", "TRIA_NIV_C_URG"]
OBS_TEXTO_LIBRE = ["ANAM_ALTA_SICH_REH", "EVO_ALTA_SICH_REH", "ANT_PER_HIS_SICH_REH", "OBJ_ALTA_SICH_REH"]


# fmt: on
# --- MODELO DE CONDICIONES CLINICAS NARRATIVO (10+ CONDICIONES) ---
CONDICIONES_CLINICAS = {
    "chequeo": {
        "nombre": "Chequeo General",
        "servicios_predominantes": ["Medicina de Familia", "Medicina Interna"],
        "estados": {
            "SEGUIMIENTO_GENERAL": {
                "procedimientos": [
                    {
                        "nombre": "Analítica General de rutina",
                        "tipo_acto": "ANALITICA",
                        "observaciones": OBS_HEMOGRAMA + OBS_BIOQUIMICA_BASICA,
                    }
                ],
                "frecuencia_anual": (0, 1),
                "transiciones": [],
                "texto_evolucion": "Acude para revisión general de salud. Asintomático.",
                "tratamiento_recomendado": "Mantener estilo de vida saludable.",
            }
        },
        "observaciones_clave": OBS_VITALES,
    },
    "hipertension": {
        "nombre": "Hipertensión Arterial",
        "servicios_predominantes": ["Cardiología", "Medicina de Familia"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [
                    {
                        "nombre": "Consulta inicial por sospecha de HTA",
                        "tipo_acto": "CONSULTA EXTERNA",
                        "observaciones": OBS_TEXTO_LIBRE + OBS_VITALES,
                    }
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [{"al_estado": "TRATAMIENTO_ACTIVO", "tras_meses": 3}],
                "texto_evolucion": "Cifras de TA elevadas. Se solicita MAPA para confirmar HTA.",
                "tratamiento_recomendado": "Iniciar medidas higiénico-dietéticas.",
            },
            "TRATAMIENTO_ACTIVO": {
                "procedimientos": [
                    {
                        "nombre": "Consulta de ajuste de tratamiento HTA",
                        "tipo_acto": "CONSULTA EXTERNA",
                        "observaciones": OBS_VITALES,
                    }
                ],
                "frecuencia_anual": (2, 4),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 12}],
                "texto_evolucion": "Seguimiento por HTA. Se ajusta dosis de tratamiento.",
                "tratamiento_recomendado": "Aumentar dosis de antihipertensivo.",
            },
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [
                    {"nombre": "Revisión anual HTA", "tipo_acto": "CONSULTA EXTERNA", "observaciones": OBS_VITALES}
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [],
                "texto_evolucion": "HTA bien controlada. Acude a revisión anual.",
                "tratamiento_recomendado": "Mantener tratamiento.",
            },
        },
        "observaciones_clave": [],
    },
    "diabetes": {
        "nombre": "Diabetes Mellitus Tipo 2",
        "servicios_predominantes": ["Endocrinología", "Medicina de Familia"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [
                    {
                        "nombre": "Analítica con Hemoglobina Glicosilada (HbA1c)",
                        "tipo_acto": "ANALITICA",
                        "observaciones": ["GLUC", "HBA1C"],
                    }
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [{"al_estado": "TRATAMIENTO_ACTIVO", "tras_meses": 3}],
                "texto_evolucion": "Hiperglucemia en analítica rutinaria. Se confirma DM2.",
                "tratamiento_recomendado": "Iniciar Metformina.",
            },
            "TRATAMIENTO_ACTIVO": {
                "procedimientos": [
                    {
                        "nombre": "Consulta de ajuste de tratamiento DM2",
                        "tipo_acto": "CONSULTA EXTERNA",
                        "observaciones": ["GLUC"],
                    }
                ],
                "frecuencia_anual": (3, 5),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 24}],
                "texto_evolucion": "Mal control glucémico. Se añade segundo antidiabético oral.",
                "tratamiento_recomendado": "Añadir iDPP4 al tratamiento.",
            },
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [
                    {"nombre": "Revisión anual DM2", "tipo_acto": "CONSULTA EXTERNA", "observaciones": OBS_VITALES},
                    {"nombre": "Revisión de fondo de ojo", "tipo_acto": "OFTALMOLOGIA"},
                ],
                "frecuencia_anual": (1, 3),
                "transiciones": [],
                "texto_evolucion": "DM2 estable con buen control metabólico.",
                "tratamiento_recomendado": "Mantener misma pauta.",
            },
        },
        "observaciones_clave": [],
    },
    "dislipidemia": {
        "nombre": "Dislipidemia",
        "servicios_predominantes": ["Medicina de Familia", "Cardiología"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [
                    {
                        "nombre": "Analítica con perfil lipídico",
                        "tipo_acto": "ANALITICA",
                        "observaciones": OBS_PERFIL_LIPIDICO,
                    }
                ],
                "frecuencia_anual": (1, 1),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 6}],
                "texto_evolucion": "Cifras de Colesterol LDL elevadas.",
                "tratamiento_recomendado": "Recomendaciones dietéticas.",
            },
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [
                    {
                        "nombre": "Control analítico de lípidos",
                        "tipo_acto": "ANALITICA",
                        "observaciones": OBS_PERFIL_LIPIDICO,
                    }
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [],
                "texto_evolucion": "Seguimiento de dislipidemia con estatinas.",
                "tratamiento_recomendado": "Continuar con Atorvastatina.",
            },
        },
        "observaciones_clave": [],
    },
    "anemia": {
        "nombre": "Anemia Ferropénica",
        "servicios_predominantes": ["Medicina de Familia", "Hematología Clínica"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [
                    {
                        "nombre": "Analítica con perfil férrico",
                        "tipo_acto": "ANALITICA",
                        "observaciones": OBS_HEMOGRAMA + OBS_PERFIL_FERRICO,
                    }
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [{"al_estado": "TRATAMIENTO_ACTIVO", "tras_meses": 1}],
                "texto_evolucion": "Astenia y fatiga. Analítica con Hb baja.",
                "tratamiento_recomendado": "Iniciar tratamiento con hierro oral.",
            },
            "TRATAMIENTO_ACTIVO": {
                "procedimientos": [
                    {
                        "nombre": "Control analítico de respuesta a hierro",
                        "tipo_acto": "ANALITICA",
                        "observaciones": OBS_HEMOGRAMA,
                    }
                ],
                "frecuencia_anual": (2, 3),
                "transiciones": [{"al_estado": "RESUELTO", "tras_meses": 6}],
                "texto_evolucion": "Revisión tras inicio de ferroterapia.",
                "tratamiento_recomendado": "Continuar con hierro oral.",
            },
            "RESUELTO": {
                "procedimientos": [],
                "frecuencia_anual": (0, 0),
                "transiciones": [],
                "texto_evolucion": "Anemia resuelta.",
                "tratamiento_recomendado": "Alta.",
            },
        },
        "observaciones_clave": [],
    },
    "migrana": {
        "nombre": "Migraña Crónica",
        "servicios_predominantes": ["Neurología", "Medicina de Familia"],
        "estados": {
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [{"nombre": "Consulta de seguimiento por Cefalea", "tipo_acto": "CONSULTA EXTERNA"}],
                "frecuencia_anual": (2, 5),
                "transiciones": [{"al_estado": "AGUDIZACION", "probabilidad_anual": 0.2}],
                "texto_evolucion": "Seguimiento por migraña. Refiere 3-4 crisis al mes.",
                "tratamiento_recomendado": "Ajustar tratamiento profiláctico.",
            },
            "AGUDIZACION": {
                "procedimientos": [
                    {"nombre": "Atención por crisis migrañosa", "tipo_acto": "URGENCIAS", "observaciones": OBS_VITALES}
                ],
                "frecuencia_anual": (0, 2),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 1}],
                "texto_evolucion": "Acude a urgencias por crisis migrañosa intensa.",
                "tratamiento_recomendado": "Se administra tratamiento intravenoso.",
            },
        },
        "observaciones_clave": [],
    },
    "ansiedad": {
        "nombre": "Trastorno Mixto Ansioso-Depresivo",
        "servicios_predominantes": ["Psiquiatría", "Psicología Clínica", "Medicina de Familia"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [{"nombre": "Entrevista clínica estructurada", "tipo_acto": "CONSULTA EXTERNA"}],
                "frecuencia_anual": (2, 4),
                "transiciones": [{"al_estado": "TRATAMIENTO_ACTIVO", "tras_meses": 2}],
                "texto_evolucion": "Refiere clínica de ansiedad y ánimo bajo.",
                "tratamiento_recomendado": "Iniciar tratamiento con ISRS.",
            },
            "TRATAMIENTO_ACTIVO": {
                "procedimientos": [{"nombre": "Sesión de Psicoterapia", "tipo_acto": "CONSULTA EXTERNA"}],
                "frecuencia_anual": (8, 15),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 12}],
                "texto_evolucion": "Seguimiento en psicoterapia con buena evolución.",
                "tratamiento_recomendado": "Continuar con psicoterapia y tratamiento.",
            },
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [{"nombre": "Consulta de seguimiento psiquiátrico", "tipo_acto": "CONSULTA EXTERNA"}],
                "frecuencia_anual": (1, 3),
                "transiciones": [],
                "texto_evolucion": "Paciente estable. Refiere mejoría anímica.",
                "tratamiento_recomendado": "Mantener misma pauta.",
            },
        },
        "observaciones_clave": ["CUID_ENF_56"],
    },
    "artrosis": {
        "nombre": "Artrosis",
        "servicios_predominantes": ["Traumatología", "Rehabilitación"],
        "estados": {
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [
                    {"nombre": "Radiografía de control", "tipo_acto": "PRUEBA DE IMAGEN"},
                    {"nombre": "Infiltración intraarticular", "tipo_acto": "PROCEDIMIENTO MENOR"},
                    {"nombre": "Sesiones de Fisioterapia", "tipo_acto": "REHABILITACION"},
                ],
                "frecuencia_anual": (1, 3),
                "transiciones": [],
                "texto_evolucion": "Dolor articular crónico de carácter mecánico.",
                "tratamiento_recomendado": "Analgesia a demanda y ejercicios.",
            }
        },
        "observaciones_clave": OBS_ESCALA_DOWNTON,
    },
    "epoc": {
        "nombre": "EPOC",
        "servicios_predominantes": ["Neumología", "Medicina Interna"],
        "estados": {
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [
                    {
                        "nombre": "Espirometría de control",
                        "tipo_acto": "PRUEBA DIAGNOSTICA",
                        "observaciones": ["PEF", "SAT_O2"],
                    }
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [{"al_estado": "AGUDIZACION", "probabilidad_anual": 0.15}],
                "texto_evolucion": "EPOC estable con su tratamiento broncodilatador.",
                "tratamiento_recomendado": "Continuar con misma pauta.",
            },
            "AGUDIZACION": {
                "procedimientos": [
                    {
                        "nombre": "Atención en Urgencias por agudización de EPOC",
                        "tipo_acto": "URGENCIAS",
                        "observaciones": OBS_VITALES,
                    }
                ],
                "frecuencia_anual": (0, 2),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 1}],
                "texto_evolucion": "Aumento de disnea y expectoración.",
                "tratamiento_recomendado": "Pauta corta de corticoides.",
            },
        },
        "observaciones_clave": [],
    },
    "cataratas": {
        "nombre": "Cataratas",
        "servicios_predominantes": ["Oftalmología"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [{"nombre": "Biometría ocular", "tipo_acto": "PRUEBA DIAGNOSTICA"}],
                "frecuencia_anual": (1, 2),
                "transiciones": [{"al_estado": "PREQUIRURGICO", "tras_meses": 2}],
                "texto_evolucion": "Disminución de agudeza visual.",
                "tratamiento_recomendado": "Valorar cirugía de cataratas.",
            },
            "PREQUIRURGICO": {
                "procedimientos": [{"nombre": "Consulta preoperatoria", "tipo_acto": "CONSULTA EXTERNA"}],
                "frecuencia_anual": (1, 1),
                "transiciones": [{"al_estado": "CIRUGIA", "tras_meses": 6}],
                "texto_evolucion": "Apto para cirugía. En lista de espera.",
                "tratamiento_recomendado": "Esperar fecha de intervención.",
            },
            "CIRUGIA": {
                "procedimientos": [{"nombre": "Cirugía de Facoemulsificación", "tipo_acto": "CIRUGIA"}],
                "frecuencia_anual": (1, 1),
                "transiciones": [{"al_estado": "RESUELTO", "tras_meses": 3}],
                "texto_evolucion": "Intervención de cataratas sin incidencias.",
                "tratamiento_recomendado": "Tratamiento postoperatorio con colirios.",
            },
            "RESUELTO": {
                "procedimientos": [],
                "frecuencia_anual": (0, 0),
                "transiciones": [],
                "texto_evolucion": "Mejoría de agudeza visual.",
                "tratamiento_recomendado": "Alta.",
            },
        },
        "observaciones_clave": [],
    },
    "asma": {
        "nombre": "Asma Bronquial",
        "servicios_predominantes": ["Neumología", "Alergología"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [
                    {
                        "nombre": "Espirometría forzada",
                        "tipo_acto": "PRUEBA DIAGNOSTICA",
                        "observaciones": ["PEF", "SAT_O2"],
                    }
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 6}],
                "texto_evolucion": "Clínica de disnea y sibilancias. Espirometría compatible con asma.",
                "tratamiento_recomendado": "Iniciar corticoides inhalados.",
            },
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [{"nombre": "Consulta de seguimiento de Asma", "tipo_acto": "CONSULTA EXTERNA"}],
                "frecuencia_anual": (0, 2),
                "transiciones": [{"al_estado": "AGUDIZACION", "probabilidad_anual": 0.10}],
                "texto_evolucion": "Paciente asmático estable.",
                "tratamiento_recomendado": "Continuar con misma pauta.",
            },
            "AGUDIZACION": {
                "procedimientos": [
                    {"nombre": "Atención por crisis asmática", "tipo_acto": "URGENCIAS", "observaciones": OBS_VITALES}
                ],
                "frecuencia_anual": (1, 1),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 1}],
                "texto_evolucion": "Acude a urgencias por crisis asmática.",
                "tratamiento_recomendado": "Pauta corta de corticoides.",
            },
        },
        "observaciones_clave": [],
    },
    "hipotiroidismo": {
        "nombre": "Hipotiroidismo Subclínico",
        "servicios_predominantes": ["Endocrinología", "Medicina de Familia"],
        "estados": {
            "DIAGNOSTICO": {
                "procedimientos": [
                    {
                        "nombre": "Analítica con Perfil Tiroideo",
                        "tipo_acto": "ANALITICA",
                        "observaciones": OBS_PERFIL_TIROIDEO,
                    }
                ],
                "frecuencia_anual": (1, 1),
                "transiciones": [{"al_estado": "SEGUIMIENTO_CRONICO", "tras_meses": 3}],
                "texto_evolucion": "Resultados de analítica de rutina muestran TSH ligeramente elevada con T4 normal. Compatible con hipotiroidismo subclínico.",
                "tratamiento_recomendado": "Vigilar evolución. Repetir analítica en 6 meses. No iniciar tratamiento por el momento.",
            },
            "SEGUIMIENTO_CRONICO": {
                "procedimientos": [
                    {
                        "nombre": "Control analítico de TSH",
                        "tipo_acto": "ANALITICA",
                        "observaciones": OBS_PERFIL_TIROIDEO,
                    }
                ],
                "frecuencia_anual": (1, 2),
                "transiciones": [],
                "texto_evolucion": "Paciente en seguimiento por hipotiroidismo subclínico. Se mantiene eutiroideo sin tratamiento.",
                "tratamiento_recomendado": "Continuar vigilancia analítica anual.",
            },
        },
        "observaciones_clave": [],
    },
}

# --- PERFILES DE PACIENTES (AMPLIADOS Y DIVERSOS) ---
PERFILES = {
    "sano": {
        "probabilidad": 0.15,
        "posibles_condiciones": [CONDICIONES_CLINICAS["chequeo"]],
    },
    "riesgo_cardiovascular": {
        "probabilidad": 0.25,
        "posibles_condiciones": [
            CONDICIONES_CLINICAS["hipertension"],
            CONDICIONES_CLINICAS["diabetes"],
            CONDICIONES_CLINICAS["dislipidemia"],
        ],
    },
    "adulto_mayor_complejo": {
        "probabilidad": 0.25,
        "posibles_condiciones": [
            CONDICIONES_CLINICAS["artrosis"],
            CONDICIONES_CLINICAS["cataratas"],
            CONDICIONES_CLINICAS["hipertension"],
        ],
    },
    "respiratorio_cronico": {
        "probabilidad": 0.20,
        "posibles_condiciones": [
            CONDICIONES_CLINICAS["epoc"],
            CONDICIONES_CLINICAS["asma"],
        ],
    },
    "joven_con_patologias": {
        "probabilidad": 0.15,
        "posibles_condiciones": [
            CONDICIONES_CLINICAS["migrana"],
            CONDICIONES_CLINICAS["anemia"],
            CONDICIONES_CLINICAS["ansiedad"],
            CONDICIONES_CLINICAS["hipotiroidismo"],
        ],
    },
}

# --- LISTAS DE DATOS (AMPLIADAS) ---
REGIMENES_SS = [
    "PENSIONISTAS CONTRIB. EXENCION FARMACIA",
    "PENSIONISTA TITULAR NORMAL",
    "ACTIVO NORMAL",
    "ACTIVO FAMILIAR",
    "DESEMPLEADO",
    "MUTUALIDAD GENERAL",
]
ALERGIAS_COMUNES = [
    {"descripcion": "PENICILINA", "codigo": "ALG-PEN"},
    {
        "descripcion": "AAS (Ácido acetilsalicílico)",
        "codigo": "ALG-AAS",
    },
    {
        "descripcion": "Intolerancia a Grupo AINES",
        "codigo": "ALG-AINES5",
    },
    {"descripcion": "YODO", "codigo": "ALG-YODO"},
    {"descripcion": "DICLOFENACO", "codigo": "ALG-132"},
    {"descripcion": "PÓLENES", "codigo": "ALG-POLEN"},
    {"descripcion": "ÁCAROS", "codigo": "ALG-ACAROS"},
    {"descripcion": "MARISCO", "codigo": "ALG-MARISCO"},
    {
        "descripcion": "FRUTOS SECOS",
        "codigo": "ALG-FRUTSECO",
    },
    {"descripcion": "SULFAMIDAS", "codigo": "ALG-SULFA"},
]
PRESTACIONES_CITA = [
    "PRIMERA VISITA",
    "SEGUNDA VISITA O SUCESIVAS",
    "PRUEBAS DE CARACTER ORDINARIO",
    "RESULTADOS",
    "CONSULTA TELEFÓNICA",
    "REVISIÓN ANUAL",
    "PRIMERA VISITA PREFERENTE",
]

# --- BASE DE DATOS DE OBSERVACIONES (BASADA EN TUS EJEMPLOS) ---
OBSERVACIONES_DB = {
    # Valoraciones Generales / Enfermería
    "CUID_ENF_51": {"nombre": "Movilidad", "valor": lambda: random.choice(["1. Normal", "2. Limitada", "3. Encamado"])},
    "CUID_ENF_53": {
        "nombre": "Baño",
        "valor": lambda: random.choice(["1. Independiente", "2. Ayuda parcial", "3. Ayuda total"]),
    },
    "CUID_ENF_16": {
        "nombre": "Estado de la piel",
        "valor": lambda: random.choice(["1. Sin alteraciones", "2. Alterada", "3. Úlcera por presión"]),
    },
    "CUID_ENF_8": {
        "nombre": "Ingesta de alimentos",
        "valor": lambda: random.choice(["1.Adecuada", "2.Inadecuada", "3.Nula"]),
    },
    "ALT_PESO_3_MESES": {
        "nombre": "Alteraciones en el peso en los últimos 3 meses",
        "valor": lambda: random.choice(["Sin cambios", "Aumento > 2kg", "Disminución > 2kg"]),
    },
    "DET_FUN_6_MESES": {
        "nombre": "Deterioro de la capacidad funcional en los últimos 6 meses",
        "valor": lambda: random.choice(["No", "Sí"]),
    },
    "HAB_TOX_GEN": {
        "nombre": "Hábitos Tóxicos",
        "valor": lambda: random.choice(["No refiere", "Fumador activo", "Ex-fumador", "Bebedor de riesgo"]),
    },
    "ALERGIAS_GEN": {"nombre": "Alergias conocidas", "valor": lambda: random.choice(["Sí", "No"])},
    "CUID_ENF_56": {
        "nombre": "Estado de ánimo",
        "valor": lambda: random.choice(["Tranquilo y colaborador", "Ansioso", "Apático", "Agitado"]),
    },
    # Signos Vitales
    "TAS_GEN": {
        "nombre": "Tensión Arterial Sistólica",
        "valor": lambda: random.randint(90, 180),
        "unidad": "mmHg",
        "codigoEstandar": "72313002",
        "valorAnormalMin": 90,
        "valorAnormalMax": 140,
    },
    "TAD_GEN": {
        "nombre": "Tensión Arterial Diastólica",
        "valor": lambda: random.randint(50, 100),
        "unidad": "mmHg",
        "valorAnormalMin": 60,
        "valorAnormalMax": 90,
    },
    "FC_GEN": {
        "nombre": "Frecuencia Cardiaca",
        "valor": lambda: random.randint(55, 110),
        "unidad": "lpm",
        "codigoEstandar": "364075005",
        "valorAnormalMin": 60,
        "valorAnormalMax": 100,
    },
    "TEM_GEN": {
        "nombre": "Temperatura",
        "valor": lambda: round(random.uniform(35.5, 38.5), 1),
        "unidad": "°C",
        "codigoEstandar": "703421000",
        "valorAnormalMax": 37.5,
    },
    "FIO2_GEN": {"nombre": "FIO2", "valor": lambda: 21, "unidad": "%"},
    "SAT_O2": {
        "nombre": "Saturación de Oxígeno",
        "unidad": "%",
        "valor": lambda: random.randint(92, 100),
        "valorAnormalMin": 94,
    },
    "VAL_IMC_GEN": {
        "nombre": "Índice de Masa Corporal (IMC)",
        "valor": lambda: round(random.uniform(18.5, 35.0), 2),
        "unidad": "kg/m2",
    },
    # Específicas de Urgencias
    "PACIENTE_URGENCIAS": {"nombre": "Localización Paciente Urgencias", "valor": lambda: f"BOX-{random.randint(1,10)}"},
    "RAD_F_ACCES": {
        "nombre": "Forma de Acceso a Urgencias",
        "valor": lambda: random.choice(["Propios medios", "Ambulancia", "Derivado de AP"]),
    },
    "TRIA_NIV_C_URG": {"nombre": "Nivel Previo en Triage", "valor": lambda: "VALORAR CONSTANTES VITALES"},
    # Escalas
    "ALTERAUDI_DOWNTON": {"nombre": "Alteraciones auditivas (Downton)", "valor": lambda: random.choice(["No", "Sí"])},
    "PCAI_PREVIAS_DOWNTON": {"nombre": "Caídas previas (Downton)", "valor": lambda: random.choice(["No", "Sí"])},
    "DIURET_DOWNTON": {"nombre": "Toma Diuréticos (Downton)", "valor": lambda: random.choice(["No", "Sí"])},
    # Texto Libre (Generado dinámicamente)
    "ANAM_ALTA_SICH_REH": {"nombre": "Anamnesis", "valor": "dinamico"},
    "ANT_PER_HIS_SICH_REH": {"nombre": "Antecedentes Personales", "valor": "dinamico"},
    "EVO_ALTA_SICH_REH": {"nombre": "Evolución", "valor": "dinamico"},
    "OBJ_ALTA_SICH_REH": {"nombre": "Objetivo inicio", "valor": "dinamico"},
    # Laboratorio: Bioquímica y otros
    "2751": {
        "nombre": "Sangre Oculta en heces",
        "valor": lambda: random.choice(["Negativo", "Positivo"]),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
    "3036": {
        "nombre": "T4 LIBRE (Suero)",
        "unidad": "ng/dL",
        "valor": lambda: round(random.uniform(0.7, 1.5), 2),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 0.7,
        "valorAnormalMax": 1.48,
    },
    "3039": {
        "nombre": "HORMONA TIREOESTIMULANTE (Suero)",
        "unidad": "uUI/mL",
        "valor": lambda: round(random.uniform(0.3, 5.5), 2),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 0.35,
        "valorAnormalMax": 5.0,
    },
    "4022": {
        "nombre": "PROTEINA C REACTIVA (Suero)",
        "unidad": "mg/L",
        "valor": lambda: round(random.uniform(0.1, 10.0), 2),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMax": 5,
        "posibles_comentarios": ["Elevación inespecífica. Valorar clínica.", "Dentro de la normalidad."],
    },
    "1419": {
        "nombre": "TRIGLICERIDOS (Suero)",
        "unidad": "mg/dL",
        "valor": lambda: random.randint(50, 250),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMax": 150,
    },
    "2105": {
        "nombre": "GLUCOSA (Orina)",
        "valor": lambda: "Negativo",
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
    "GLUC": {
        "nombre": "GLUCOSA BASAL (Suero)",
        "unidad": "mg/dL",
        "valor": lambda: random.randint(70, 180),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 70,
        "valorAnormalMax": 100,
    },
    "FERRITINA": {
        "nombre": "FERRITINA (Suero)",
        "unidad": "ng/mL",
        "valor": lambda: random.randint(10, 300),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 15,
        "valorAnormalMax": 200,
    },
    "COLESTEROL_TOTAL": {
        "nombre": "Colesterol Total",
        "unidad": "mg/dL",
        "valor": lambda: random.randint(150, 280),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMax": 200,
    },
    "LDL": {
        "nombre": "Colesterol LDL",
        "unidad": "mg/dL",
        "valor": lambda: random.randint(80, 190),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMax": 130,
    },
    "HDL": {
        "nombre": "Colesterol HDL",
        "unidad": "mg/dL",
        "valor": lambda: random.randint(30, 80),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 40,
    },
    # Laboratorio: Hemograma completo
    "100": {
        "nombre": "LEUCOCITOS",
        "unidad": "10E3/uL",
        "valor": lambda: round(random.uniform(3.5, 12.0), 2),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "codigoEstandar": "767002",
        "valorAnormalMin": 4.5,
        "valorAnormalMax": 11.0,
    },
    "102": {
        "nombre": "HEMATIES",
        "unidad": "10E6/uL",
        "valor": lambda: round(random.uniform(3.8, 5.8), 2),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
    "104": {
        "nombre": "HEMOGLOBINA",
        "unidad": "g/dL",
        "valor": lambda: round(random.uniform(9.0, 17.0), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 12.0,
        "posibles_interpretaciones": ["Normocitosis", "Normocromía", "Microcítica hipocrómica.", "Macrocítica."],
    },
    "106": {
        "nombre": "HEMATOCRITO",
        "unidad": "%",
        "valor": lambda: round(random.uniform(28.0, 50.0), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 36.0,
        "valorAnormalMax": 48.0,
    },
    "108": {
        "nombre": "VCM",
        "unidad": "fL",
        "valor": lambda: round(random.uniform(78.0, 100.0), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "valorAnormalMin": 80.0,
        "valorAnormalMax": 98.0,
    },
    "110": {
        "nombre": "HCM",
        "unidad": "pg",
        "valor": lambda: round(random.uniform(27.0, 34.0), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
    "112": {
        "nombre": "CHCM",
        "unidad": "g/dL",
        "valor": lambda: round(random.uniform(32.0, 36.0), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
    "114": {
        "nombre": "ADE",
        "unidad": "%",
        "valor": lambda: round(random.uniform(11.5, 15.0), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
    "118": {"nombre": "NRBC", "unidad": "10E3/uL", "valor": lambda: 0},
    "120": {"nombre": "% ERITR/LEUC", "unidad": "%", "valor": lambda: 0},
    "130": {
        "nombre": "PLAQUETAS",
        "unidad": "10E3/uL",
        "valor": lambda: random.randint(150, 450),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
        "codigoEstandar": "11111001",
        "valorAnormalMin": 150,
        "valorAnormalMax": 450,
    },
    "140": {
        "nombre": "NEUTROFILOS",
        "unidad": "10E3/uL",
        "valor": lambda: round(random.uniform(1.8, 7.7), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
    "148": {
        "nombre": "LINFOCITOS",
        "unidad": "10E3/uL",
        "valor": lambda: round(random.uniform(1.0, 4.8), 1),
        "codigoDepartamento": "LAB",
        "nombreDepartamento": "LABORATORIO",
    },
}
