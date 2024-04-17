import csv
from time import localtime, asctime
from math import log

def analisis_archivos_datos(max_temp, min_temp, max_hum, min_hum, temp_promedio, humedad_promedio, punto_rocio, max_temp_time, min_temp_time, max_hum_time, min_hum_time, tiempo_fuera_temp, tiempo_fuera_hum):
    with open("analytics.csv", "w", newline='') as archivo_analisis:
        writer = csv.writer(archivo_analisis)
        writer.writerow(["Estadísticas:"])
        writer.writerow(["Temperatura máxima:", max_temp])
        writer.writerow(["Temperatura mínima:", min_temp])
        writer.writerow(["Humedad máxima:", max_hum])
        writer.writerow(["Humedad mínima:", min_hum])
        writer.writerow(["Promedio de temperatura:", temp_promedio])
        writer.writerow(["Promedio de humedad:", humedad_promedio])
        writer.writerow(["Hora de mayor temperatura:", asctime(localtime(max_temp_time))])
        writer.writerow(["Hora de menor temperatura:", asctime(localtime(min_temp_time))])
        writer.writerow(["Hora de mayor humedad:", asctime(localtime(max_hum_time))])
        writer.writerow(["Hora de menor humedad:", asctime(localtime(min_hum_time))])
        writer.writerow(["Tiempo fuera de los límites de temperatura establecidos:", tiempo_fuera_temp, "segundos"])
        writer.writerow(["Tiempo fuera de los límites de humedad establecidos:", tiempo_fuera_hum, "segundos"])
        writer.writerow(["El punto de rocío es:", punto_rocio])


class Sample:
    def __init__(self, temperatura, humedad):
        self.temperatura = temperatura
        self.humedad = humedad

def calcular_promedio(samples):
    suma_temp = sum(sample.temperatura for sample in samples)
    suma_hum = sum(sample.humedad for sample in samples)
    return suma_temp / len(samples), suma_hum / len(samples)

def calcular_tiempo_fuera_limites(temp_limite, hum_limite, samples):
    tiempo_fuera_temp = sum(1 for sample in samples if sample.temperatura > temp_limite or sample.temperatura < temp_limite)
    tiempo_fuera_hum = sum(1 for sample in samples if sample.humedad > hum_limite or sample.humedad < hum_limite)
    return tiempo_fuera_temp, tiempo_fuera_hum

def calcular_punto_rocio(temperatura, humedad):
    B = 17.67
    C = 243.5
    gamma = (B * temperatura) / (C + temperatura) + log(humedad / 100.0)
    punto_rocio = (C * gamma) / (B - gamma)
    return punto_rocio

def main():
    num_samples = 0
    samples = []

    temp_limite = float(input("Ingrese el límite de temperatura: "))
    hum_limite = float(input("Ingrese el límite de humedad: "))

    with open("datosSensor.txt", "r") as datos:
        datos.readline() 

        for line in datos:
            tiempo, temp, humd = map(float, line.strip().split(','))
            num_samples += 1
            fecha = localtime(tiempo)
            print(asctime(fecha), "- muestra leida => timestamp:", tiempo, ", temperatura:", temp, ", humedad:", humd)
            samples.append(Sample(temp, humd))

    max_temp = max(sample.temperatura for sample in samples)
    min_temp = min(sample.temperatura for sample in samples)
    max_hum = max(sample.humedad for sample in samples)
    min_hum = min(sample.humedad for sample in samples)

    max_temp_time = min_temp_time = max_hum_time = min_hum_time = samples[0]
    for sample in samples:
        if sample.temperatura > max_temp:
            max_temp = sample.temperatura
            max_temp_time = sample

        if sample.temperatura < min_temp:
            min_temp = sample.temperatura
            min_temp_time = sample

        if sample.humedad > max_hum:
            max_hum = sample.humedad
            max_hum_time = sample

        if sample.humedad < min_hum:
            min_hum = sample.humedad
            min_hum_time = sample

    temp_promedio, humedad_promedio = calcular_promedio(samples)
    tiempo_fuera_temp, tiempo_fuera_hum = calcular_tiempo_fuera_limites(temp_limite, hum_limite, samples)
    punto_rocio = calcular_punto_rocio(temp, humd)

    print("\nEstadísticas:")
    print("Temperatura máxima:", max_temp)
    print("Temperatura mínima:", min_temp)
    print("Humedad máxima:", max_hum)
    print("Humedad mínima:", min_hum)
    print("Promedio de temperatura:", temp_promedio)
    print("Promedio de humedad:", humedad_promedio)
    print("Hora de mayor temperatura:", asctime(localtime(max_temp_time)))
    print("Hora de menor temperatura:", asctime(localtime(min_temp_time)))
    print("Hora de mayor humedad:", asctime(localtime(max_hum_time)))
    print("Hora de menor humedad:", asctime(localtime(min_hum_time)))
    print("Tiempo fuera de los límites de temperatura establecidos:", tiempo_fuera_temp, "segundos")
    print("Tiempo fuera de los límites de humedad establecidos:", tiempo_fuera_hum, "segundos")

    analisis_archivos_datos(max_temp, min_temp, max_hum, min_hum, temp_promedio, humedad_promedio, punto_rocio, max_temp_time, min_temp_time, max_hum_time, min_hum_time, tiempo_fuera_hum, tiempo_fuera_temp)

if __name__ == "__main__":
    main()
