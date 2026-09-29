while True:
    try:
        temperatura = float(input('Ingrese la temperatura actual: '))

        if temperatura < 22:
            print('Encender calefacción')

        elif temperatura > 22:
            print('Encender refrigeración')

        else:
            print('Mantener temperatura')

    except:
        break




