# validadorclave/modelo/validador.py

from abc import ABC, abstractmethod
from validadorclave.modelo.errores import (
    NoCumpleLongitudMinimaError,
    NoTieneLetraMayusculaError,
    NoTieneLetraMinusculaError,
    NoTieneNumeroError,
    NoTieneCaracterEspecialError,
    NoTienePalabraSecretaError
)


class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave):
        return len(clave) > self._longitud_esperada

    def _contiene_mayuscula(self, clave):
        return any(c.isupper() for c in clave)

    def _contiene_minuscula(self, clave):
        return any(c.islower() for c in clave)

    def _contiene_numero(self, clave):
        return any(c.isdigit() for c in clave)

    @abstractmethod
    def es_valida(self, clave):
        pass


class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada=8)

    def contiene_caracter_especial(self, clave):
        caracteres_especiales = {'@', '_', '#', '$', '%'}
        return any(c in caracteres_especiales for c in clave)

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La clave debe tener una longitud de más de 8 caracteres")

        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError("La clave debe tener al menos una letra mayúscula")

        if not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError("La clave debe tener al menos una letra minúscula")

        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave debe tener al menos un número")

        if not self.contiene_caracter_especial(clave):
            raise NoTieneCaracterEspecialError("La clave debe tener al menos un caracter especial (@, _, #, $, %)")

        return True


class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(longitud_esperada=6)

    def contiene_calisto(self, clave):
        clave_lower = clave.lower()
        if "calisto" not in clave_lower:
            return False

        # Encuentra todas las ocurrencias de 'calisto' en cualquier casing
        indices = []
        start = 0
        while True:
            idx = clave_lower.find("calisto", start)
            if idx == -1:
                break
            indices.append(idx)
            start = idx + 1

        # Verifica cada ocurrencia
        for idx in indices:
            substring = clave[idx:idx + 7]  # 'calisto' tiene 7 letras
            mayusculas = sum(1 for c in substring if c.isupper())
            if 2 <= mayusculas < 7:
                return True

        return False

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La clave debe tener una longitud de más de 6 caracteres")

        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave debe tener al menos un número")

        if not self.contiene_calisto(clave):
            raise NoTienePalabraSecretaError(
                "La palabra calisto debe estar escrita con al menos dos letras en mayúscula y no todas")

        return True


class Validador:
    def __init__(self, regla):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)