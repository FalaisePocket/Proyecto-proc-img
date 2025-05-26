

'''
1. Diagrama de flujo: Calcular el área de un triángulo

Inicio
→ Pedir base
→ Pedir altura
→ Calcular: área = (base × altura) / 2
→ Mostrar área
→ Fin


---

2. Diagrama de flujo: Convertir grados Celsius a Fahrenheit

Inicio
→ Pedir grados Celsius
→ Calcular: Fahrenheit = (Celsius × 9/5) + 32
→ Mostrar Fahrenheit
→ Fin

'''


def areaTriangulo(base, altura):
    area = (base * altura) / 2
    return area

def celsiusAFahrenheit(celsius):

    fahrenheit =(celsius * 9/5) + 32

    return fahrenheit


baseIngresada=int(input("Ingrese la base del triangulo:  "))
alturaIngresada=int(input ("Ingrese la altura del triangulo:  "))


resultado=areaTriangulo(baseIngresada,alturaIngresada)
print("El area del triangulo es",resultado)


gradosCelsius=0
gradosCelsius=int(input("Ingrese los grados celsius:  "))
resultado=celsiusAFahrenheit(gradosCelsius)
print("El resultado es:", resultado)