from validadorclave.modelo.validador import (
    Validador,
    ReglaValidacionGanimedes,
    ReglaValidacionCalisto
)

def validar_clave(clave, reglas_validacion):
    for regla_cls in reglas_validacion:
        validador = Validador(regla_cls())
        try:
            if validador.es_valida(clave):
                print(f"La clave es válida para {regla_cls.__name__}")
        except Exception as e:
            print(f"Error: {regla_cls.__name__}: {str(e)}")

# Ejemplo de uso
if __name__ == "__main__":
    reglas = [ReglaValidacionGanimedes, ReglaValidacionCalisto]
    clave = input("Ingrese una clave para validar: ")
    validar_clave(clave, reglas)