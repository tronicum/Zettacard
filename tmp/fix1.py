import json

path = "app/data/fuehrerschein/locales/es.json"
with open(path, encoding='utf-8') as f:
    es = json.load(f)

es['zeichen-68'] = {
    "question": "¿Qué prescribe esta señal de tráfico?",
    "options": {
        "a": "Debe continuar aquí recto o girar a la derecha.",
        "b": "Aquí solo puede girar a la derecha.",
        "c": "Aquí está prohibido seguir recto.",
        "d": "Aquí puede circular en cualquier dirección."
    },
    "explanation": "La señal 214 es una señal de obligación sobre el sentido de circulación prescrito: en este punto solo se puede continuar recto o girar a la derecha; el resto de direcciones (p. ej. girar a la izquierda o dar la vuelta) están prohibidas."
}

es['zeichen-132'] = {
    "question": "Bajo una señal de tráfico hay un panel adicional blanco con la inscripción «Fußgänger» (peatones). ¿Qué significa esto?",
    "options": {
        "a": "El panel adicional indica que la señal principal se aplica también a los peatones.",
        "b": "Los peatones quedan en principio exentos de cualquier regulación de la señal principal.",
        "c": "Se trata de una indicación de una zona peatonal.",
        "d": "El panel adicional solo es válido para usuarios de silla de ruedas, no para el resto de peatones."
    },
    "explanation": "El panel adicional 1010-53 «Fußgänger» precisa el ámbito de aplicación de la señal principal situada encima: aclara que la regulación también incluye a los peatones, en lugar de referirse únicamente a los vehículos, como suele suponerse cuando no hay panel adicional."
}

with open(path, 'w', encoding='utf-8') as f:
    json.dump(es, f, ensure_ascii=False, indent=2)
    f.write('\n')

print("done")
