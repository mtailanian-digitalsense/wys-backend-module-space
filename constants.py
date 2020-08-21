################ string constants #########################

CAT_SALA_REU = "Sala Reunión"
CAT_OF_PRIVADA = "Puestos Trabajo Privado"
CAT_AREA_SERVICIOS = "Area Servicios"
CAT_AREA_SOPORTE = "Area Soporte"
CAT_AREA_SOPORTE_REU_INF = "Area Soporte Reuniones Informales"
CAT_PUESTO_TRABAJO = "Puestos Trabajo"
CAT_ESPECIALES = "Especiales"

SUBCAT_PEQUENIA = "Pequeña"
SUBCAT_PEQUENIO = "Pequeño"
SUBCAT_MEDIANA = "Mediana"
SUBCAT_MEDIANO = "Mediano"
SUBCAT_GRANDE = "Grande"
SUBCAT_WC_M = "Workcoffee/Comedor Mediano"
SUBCAT_WC_G = "Workcoffee/Comedor Grande"
SUBCAT_PRIV_P = "Privado Pequeño"
SUBCAT_PRIV_G = "Privado Grande"
SUBCAT_BANIO = "Baños"
SUBCAT_BANIO_ACC = "Baño Accesibilidad Universal"
SUB_CAT_RECEP_P = "Recepción Pequeña (más Lounge Pequeño)"
SUB_CAT_RECEP_G = "Recepción Grande (más Lounge Grande)"
SUBCAT_KITCH = "Kitchenette"
SUBCAT_SERVIDOR_P = "Servidor 1 Gabinete"
SUBCAT_SERVIDOR_M = "Servidor 2 Gabinetes"
SUBCAT_SERVIDOR_G = "Servidor 3 Gabinetes"
SUBCAT_PRINT_P = "Print Pequeño"
SUBCAT_PRINT_G = "Print Grande"
SUBCAT_QUIET = "Quiet Room"
SUBCAT_PHONE = "Phonebooth"
SUBCAT_PT_OPEN_SPACE = "Open Space"

SUBCAT_SALA_LAC = "Sala Lactancia"
SUBCAT_BODEGA = "Bodega"
SUBCAT_COFFEE = "Coffee point"
SUBCAT_GUARDADO_SB = "Guardado Simple Bajo"
SUBCAT_GUARDADO_SA = "Guardado Simple Alto"
SUBCAT_LOCKER = "Locker"
SUBCAT_ESPECIALES = "Sala capacitación/Taller/mindbreak/Brainstorming/Espacio Personalizable/Tarima"

PERS_SOPORTE = 0.15
PORC_USO_SOPORTE = (PERS_SOPORTE*100)/(100-(PERS_SOPORTE*100))

############### by default values ##########################

SEED_DATA = {
    CAT_SALA_REU : {
        SUBCAT_PEQUENIA : {
            "SUPERFICIE" : 8.64,
            "PERSONAS": 5,
            "SUPERFICIE_U": 1.73,
            "PORC_USO": 0.45
        },
        SUBCAT_MEDIANA:{
            "SUPERFICIE" : 17.29,
            "PERSONAS": 8,
            "SUPERFICIE_U": 2.16,
            "PORC_USO": 0.35
        },
        SUBCAT_GRANDE: {
            "SUPERFICIE" : 27.30,
            "PERSONAS": 12,
            "SUPERFICIE_U": 2.28,
            "PORC_USO": 0.20
        }
    },
    CAT_PUESTO_TRABAJO: {
        SUBCAT_PT_OPEN_SPACE: {
            "SUPERFICIE" : 3.26,
            "PERSONAS": 1,
            "SUPERFICIE_U": 3.26,
            "PORC_USO": None
        }
    },
    CAT_OF_PRIVADA :{
        SUBCAT_PRIV_P:{
            "SUPERFICIE" : 9.1,
            "PERSONAS": 1,
            "SUPERFICIE_U": 9.1,
            "PORC_USO": None
        },
        SUBCAT_PRIV_G : {
            "SUPERFICIE" : 18.56,
            "PERSONAS": 1,
            "SUPERFICIE_U": 18.56,
            "PORC_USO": None
        }
    },
    CAT_AREA_SERVICIOS :{
        SUBCAT_BANIO :{
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": 1.96,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_KITCH : {
            "SUPERFICIE" : 3.68,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_SERVIDOR_P: {
            "SUPERFICIE" : 3.6,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_SERVIDOR_M:{
            "SUPERFICIE" : 5.04,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_SERVIDOR_G:{
            "SUPERFICIE" : 6.48,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_BANIO_ACC : {
            "SUPERFICIE" : 1.96,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_PRINT_P : {
            "SUPERFICIE" : 1.95,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_PRINT_G : {
            "SUPERFICIE" : 3.978,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_SALA_LAC : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_BODEGA : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_COFFEE : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        }
    },
    CAT_AREA_SOPORTE :{
        SUB_CAT_RECEP_P : {
            "SUPERFICIE" : 8.775,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUB_CAT_RECEP_G : {
            "SUPERFICIE" : 13.735,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_QUIET :{
            "SUPERFICIE" : 3.895,
            "PERSONAS": None,
            "SUPERFICIE_U": 3.04,
            "PORC_USO": None
        },
        SUBCAT_PHONE : {
            "SUPERFICIE" : 4.1205,
            "PERSONAS": None,
            "SUPERFICIE_U": 3.04,
            "PORC_USO": None
        },
        SUBCAT_WC_M : {
            "SUPERFICIE" : 28,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_WC_G : {
            "SUPERFICIE" : 45.44,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_GUARDADO_SB : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_GUARDADO_SA : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_LOCKER : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        }
    },
    CAT_AREA_SOPORTE_REU_INF :{
        SUBCAT_PEQUENIO : {
            "SUPERFICIE" : 4.71,
            "PERSONAS": None,
            "SUPERFICIE_U": 1.51,
            "PORC_USO": 0.65
        },
        SUBCAT_MEDIANO : {
            "SUPERFICIE" : 6.54,
            "PERSONAS": None,
            "SUPERFICIE_U": 1.70,
            "PORC_USO": 1.0
        },
        SUBCAT_GRANDE : {
            "SUPERFICIE" : 45.44,
            "PERSONAS": None,
            "SUPERFICIE_U": 2.08,
            "PORC_USO": 0.35
        }
    },
    CAT_ESPECIALES : {
        SUBCAT_ESPECIALES : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        }
    }
}