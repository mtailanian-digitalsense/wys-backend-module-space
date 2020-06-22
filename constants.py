################ string constants #########################

CAT_SALA_REU = "Sala Reunión"
CAT_OF_PRIVADA = "Ofincina Privada"
CAT_SOPORTE = "Soporte"
CAT_RECEPCION = "Recepción"
CAT_INDIVIDUAL = "Individual"
CAT_COLABORATIVO = "Colaborativo"
CAT_COFFEE_COM =  "Coffee/Comedor"
CAT_PUESTO_TRABAJO = "Puesto de Trabajo"

SUBCAT_PEQUENIA = "Pequeña"
SUBCAT_PEQUENIO = "Pequeño"
SUBCAT_MEDIANA = "Mediana"
SUBCAT_MEDIANO = "Mediano"
SUBCAT_GRANDE = "Grande"
SUBCAT_BANIO = "Baño Individual"
SUBCAT_BANIO_ACC = "Baño Accesibilidad"
SUB_CAT_RECEP_P = "Pequeña (más Lounge Pequeño)"
SUB_CAT_RECEP_G = "Grande (más Lounge Grande)"
SUBCAT_KITCH = "Kitchenette"
SUBCAT_SERVIDOR_P = "Servidor Pequeño"
SUBCAT_SERVIDOR_M = "Servidor Mediano"
SUBCAT_SERVIDOR_G = "Servidor Grande"
SUBCAT_PRINT_P = "Print Pequeño"
SUBCAT_PRINT_G = "Print Grande"
SUBCAT_PEQUENIO_Q = "Pequeño (Quiet Room)"
SUBCAT_PEQUENIO_P = "Pequeño (Phonebooth)"
SUBCAT_PT_OPEN_PLAN = "Open Plan"

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
    CAT_OF_PRIVADA :{
        SUBCAT_PEQUENIO:{
            "SUPERFICIE" : 11.93,
            "PERSONAS": 1,
            "SUPERFICIE_U": 11.93,
            "PORC_USO": None
        },
        SUBCAT_GRANDE : {
            "SUPERFICIE" : 11.93,
            "PERSONAS": 1,
            "SUPERFICIE_U": 11.93,
            "PORC_USO": None
        }
    },
    CAT_SOPORTE :{
        SUBCAT_BANIO :{
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_KITCH : {
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_SERVIDOR_P: {
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_SERVIDOR_M:{
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_SERVIDOR_G:{
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_BANIO_ACC : {
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_PRINT_P : {
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        },
        SUBCAT_PRINT_G : {
            "SUPERFICIE" : None,
            "PERSONAS": PERS_SOPORTE,
            "SUPERFICIE_U": None,
            "PORC_USO": PORC_USO_SOPORTE
        }
    },
    CAT_RECEPCION :{
        SUB_CAT_RECEP_P : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUB_CAT_RECEP_G : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        }
    },
    CAT_INDIVIDUAL :{
        SUBCAT_PEQUENIO_Q :{
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": 3.04,
            "PORC_USO": None
        },
        SUBCAT_PEQUENIO_P : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": 3.04,
            "PORC_USO": None
        }
    },
    CAT_COLABORATIVO :{
        SUBCAT_PEQUENIO : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": 1.51,
            "PORC_USO": 0.65
        },
        SUBCAT_MEDIANO : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": 1.70,
            "PORC_USO": 1.0
        },
        SUBCAT_GRANDE : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": 2.08,
            "PORC_USO": 0.35
        }
    },
    CAT_COFFEE_COM :{
        SUBCAT_MEDIANO : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        },
        SUBCAT_GRANDE : {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        }
    },
    CAT_PUESTO_TRABAJO: {
        SUBCAT_PT_OPEN_PLAN: {
            "SUPERFICIE" : None,
            "PERSONAS": None,
            "SUPERFICIE_U": None,
            "PORC_USO": None
        }
    }
}