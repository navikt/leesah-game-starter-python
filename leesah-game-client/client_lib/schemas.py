from schema import Schema, Or

Spørsmål = Schema({
    "type": "SPØRSMÅL",
    "spørsmålId": str,
    "spørsmål": str,
    "kategorinavn": str,
    "svarFormat": str
})

Svar = Schema({
    "type": "SVAR",
    "kategorinavn": str,
    "lagnavn": str,
    "svar": str,
    "spørsmålId": str,
    "svarId": str,
    "opprettet": str,
})
