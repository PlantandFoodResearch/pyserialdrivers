# -*- coding: utf-8 -*-
# Auto-generated file. Do not modify!
from enum import Enum, unique


class ParamUnits(Enum):
    TEMP_C = "°C"
    TEMP_F = "°F"
    TEMP_K = "°K"
    COND_MS = "mS/cm"
    COND_US = "μS/cm"
    SCOND_MS = "mS/cm"
    SCOND_US = "μS/cm"
    TDS_G = "g/L"
    SAL_P = "PPT"
    PH_MV = "mV"
    PH_PH = "pH"
    ORP_MV = "mV"
    PRESS_A = "psia"
    PRESS_G = "psig"
    DEPTH_M = "m"
    DEPTH_FT = "ft"
    BATT_V = "V"
    TURB_N = "NTU"
    NH3_MG = "mg/L"
    NH4_MG = "mg/L"
    DDMMYY = "DDMMYY"
    MMDDYY = "MMDDYY"
    YYMMDD = "YYMMDD"
    HHMMSS = "HHMMSS"
    TDS_KG = "kg/L"
    NO3_MV = "mV"
    NO3_MG = "mg/L"
    NH4_MV = "mV"
    TDS_MG = "mg/L"
    CHLORI_MG = "mg/L"
    CHLORI_MV = "mV"
    TSS_MG = "mg/L"
    TSS_G = "g/L"
    CHLORO_UG = "ug/L"
    CHLORO_RFU = "RFU"
    ODO_P = "%Sat"
    ODO_MG = "mg/L"
    ODO_PL = "%Sat Local"
    BGAPC_R = "RFU"
    BGAPE_R = "RFU"
    TURB_F = "FNU"
    TURB_RAW = "Raw"
    BGAPC_UG = "ug/L"
    BGAPE_UG = "ug/L"
    FDOM_R = "RFU"
    FDOM_Q = "QSU"
    WIPE_V = "V"
    VCC_V = "V"
    BGAPC_RAW = "Raw"
    BGAPE_RAW = "Raw"
    FDOM_RAW = "Raw"
    CHLORO_RAW = "Raw"
    NFLCO_MS = "mS/cm"
    NFLCO_US = "μS/cm"
    WIPE_MA = "mA"
    VERT_M = "m"
    VERT_FT = "ft"


class ParamNames(Enum):
    TEMP_C = "Temperature"
    TEMP_F = "Temperature"
    TEMP_K = "Temperature"
    COND_MS = "Conductivity"
    COND_US = "Conductivity"
    SCOND_MS = "Specific Conductance"
    SCOND_US = "Specific Conductance"
    TDS_G = "TDS"
    SAL_P = "Salinity"
    PH_MV = "pH"
    PH_PH = "pH"
    ORP_MV = "ORP"
    PRESS_A = "Pressure"
    PRESS_G = "Pressure"
    DEPTH_M = "Depth"
    DEPTH_FT = "Depth"
    BATT_V = "Battery"
    TURB_N = "Turbidity"
    NH3_MG = "NH3 (Ammonia)"
    NH4_MG = "NH4 (Ammonium)"
    DDMMYY = "Date"
    MMDDYY = "Date"
    YYMMDD = "Date"
    HHMMSS = "Time"
    TDS_KG = "TDS"
    NO3_MV = "NO3 (Nitrate)"
    NO3_MG = "NO3 (Nitrate)"
    NH4_MV = "NH4 (Ammonium)"
    TDS_MG = "TDS"
    CHLORI_MG = "Chloride"
    CHLORI_MV = "Chloride"
    TSS_MG = "TSS"
    TSS_G = "TSS"
    CHLORO_UG = "Chlorophyll"
    CHLORO_RFU = "Chlorophyll"
    ODO_P = "ODO"
    ODO_MG = "ODO"
    ODO_PL = "ODO"
    BGAPC_R = "BGA-PC"
    BGAPE_R = "BGA-PE"
    TURB_F = "Turbidity"
    TURB_RAW = "Turbidity"
    BGAPC_UG = "BGA-PC"
    BGAPE_UG = "BGA-PE"
    FDOM_R = "fDOM"
    FDOM_Q = "fDOM"
    WIPE_V = "Wiper Position"
    VCC_V = "External Power"
    BGAPC_RAW = "BGA-PC"
    BGAPE_RAW = "BGA-PE"
    FDOM_RAW = "fDOM"
    CHLORO_RAW = "Chlorophyll"
    NFLCO_MS = "nLF Conductivity"
    NFLCO_US = "nLF Conductivity"
    WIPE_MA = "Wiper Peak Current"
    VERT_M = "Vertical Position"
    VERT_FT = "Vertical Position"


@unique
class ParamCodes(Enum):
    @property
    def unit(self) -> str:
        return ParamUnits[self.name].value

    @property
    def description(self) -> str:
        return ParamNames[self.name].value

    TEMP_C = 1
    TEMP_F = 2
    TEMP_K = 3
    COND_MS = 4
    COND_US = 5
    SCOND_MS = 6
    SCOND_US = 7
    TDS_G = 10
    SAL_P = 12
    PH_MV = 17
    PH_PH = 18
    ORP_MV = 19
    PRESS_A = 20
    PRESS_G = 21
    DEPTH_M = 22
    DEPTH_FT = 23
    BATT_V = 28
    TURB_N = 37
    NH3_MG = 47
    NH4_MG = 48
    DDMMYY = 51
    MMDDYY = 52
    YYMMDD = 53
    HHMMSS = 54
    TDS_KG = 95
    NO3_MV = 101
    NO3_MG = 106
    NH4_MV = 108
    TDS_MG = 110
    CHLORI_MG = 112
    CHLORI_MV = 145
    TSS_MG = 190
    TSS_G = 191
    CHLORO_UG = 193
    CHLORO_RFU = 194
    ODO_P = 211
    ODO_MG = 212
    ODO_PL = 214
    BGAPC_R = 216
    BGAPE_R = 218
    TURB_F = 223
    TURB_RAW = 224
    BGAPC_UG = 225
    BGAPE_UG = 226
    FDOM_R = 227
    FDOM_Q = 228
    WIPE_V = 229
    VCC_V = 230
    BGAPC_RAW = 231
    BGAPE_RAW = 232
    FDOM_RAW = 233
    CHLORO_RAW = 234
    NFLCO_MS = 237
    NFLCO_US = 238
    WIPE_MA = 239
    VERT_M = 240
    VERT_FT = 241
