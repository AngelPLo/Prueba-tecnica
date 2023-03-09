# Apertura de archivo y extracción de linea
# Para ahorrar memoria se procesa cada línea 
import argparse
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pdb
#FUNCIONES
def graficar(time,sensor_data,sensor_names, sensor_units,infusion_data,infusion_names, infusion_units, n_infusion):
    t = time[1:len(time),:];
    s_data = sensor_data[1:len(sensor_data),:]
    i_data = infusion_data[1:len(infusion_data),:]
    s_names = sensor_names
    s_units = sensor_units
    i_names = infusion_names
    i_units = infusion_units
    

    sensor_data_max = np.empty([1,18])
    infusion_data_max = np.empty([1,4])

    #Normalizamos los vectores de los datos para que sean de aproximadamente el mismo tamaño
    for i in range(18):
        max = np.max(s_data[:,i])
        min = np.min(s_data[:,i])
        sensor_data_max[0,i] = max
        if abs(min) > abs(max):
            sensor_data_max[0,i] = abs(min)
            
        if sensor_data_max[0,i] == 0:
            s_data[:,i] = s_data[:,i]*0
            continue
        s_data[:,i] = s_data[:,i]/sensor_data_max[0,i]
    #Generamos un título para la gráfica y para los ejes
    temperature_title = "Temperaturas"
    motor_title = "Estados del motor"
    ADCs_rate_title = "Frecuencia de los ADC"
    infusion_tube_title = "Estado del tubo"
    data1_title = i_names[0]
    data2_title = i_names[1]
    data3_title = i_names[2]
    data4_title = i_names[3]
    data_figure_title = "Datos de la infusion {infusion}".format(infusion=n_infusion)
    sensor_figure_title = "Datos de sensores en la infusion {infusion}".format(infusion=n_infusion)
    sensor_figure, ((temp, motor),(ADCs, tube)) = plt.subplots(2,2)
    data_figure, ((data1, data2),(data3, data4)) = plt.subplots(2,2)
    sensor_figure.suptitle(sensor_figure_title)
    data_figure.suptitle(data_figure_title)
    temp_legends = []
    motor_legends = []
    ADCs_legends = []
    tube_legends = []
    for i in range(8):
        multi = sensor_data_max[0,i]
        legend = s_names[i] + " x{multiplicador}".format(multiplicador=multi)
        temp_legends.append(legend)
        temp.plot(t,s_data[:,i])
    temp.legend(temp_legends)
    temp.set_ylabel("°C")
    temp.set_title("Temperaturas")
    
    for i in range(8,12):
        multi = sensor_data_max[0,i]
        legend = s_names[i] + " x{multiplicador}{unidades}".format(unidades=s_units[i], multiplicador=multi)
        motor_legends.append(legend)
        motor.plot(t,s_data[:,i])
    motor.legend(motor_legends)
    motor.set_title("Estados del motor")
    
    for i in range(12,14):
        multi = sensor_data_max[0,i]
        legend = s_names[i] + " x{multiplicador}{unidades}".format(unidades=s_units[i], multiplicador=multi)
        tube_legends.append(legend)
        tube.plot(t,s_data[:,i])
    tube.legend(tube_legends)
    tube.set_title("Estado del tubo")
    tube.set_xlabel("segundos")
    for i in range(14,18):
        multi = sensor_data_max[0,i]
        legend = s_names[i] + " x{multiplicador}".format(multiplicador=multi)
        ADCs_legends.append(legend)
        ADCs.plot(t,s_data[:,i])
    ADCs.legend(ADCs_legends)
    ADCs.set_ylabel("Hertz (1/s)")
    ADCs.set_title("Frecuencia de los ADC")
    ADCs.set_xlabel("segundos")
    plt.show(block=False)
    data1.plot(t,i_data[:,0])
    data1.set_title(data1_title)
    data1.set_ylabel(i_units[0])
    data2.plot(t,i_data[:,1])
    data2.set_ylabel(i_units[1])
    data2.set_title(data2_title)
    data3.plot(t,i_data[:,2])
    data3.set_ylabel(i_units[2])
    data3.set_title(data3_title)
    data3.set_xlabel("segundos")
    data4.plot(t,i_data[:,3])
    data4.set_title(data4_title)
    data4.set_ylabel(i_units[3])
    data4.set_xlabel("segundos")
    plt.show(block=True)


#MAIN
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help= "ruta de archivo de registro")
    args = parser.parse_args()

    #abrimos el archhvo de la ruta especificada
    log = open(args.name)
    matplotlib.use('TkAgg')
    #log = open("Fika_2023_03_06_143.txt")
    #log.readline()
    nl = 0;
    #Arreglo de los datos que vamos a graficar
    #Sensores
    Sensor_names = ["ex1","ex2",
                    "up","mup",
                    "mdn","dn",
                    "tube","valv",
                    "pos","speed",
                    "m_pow","current",
                    "bh_pow","p_r",
                    "0_r","1_r",
                    "2_r","3_r"]

    Sensor_data = np.empty([1,18])
    Sensor_data_max = np.empty([1,18])
    buffer_sensor_data = np.zeros([1,18])
    Sensor_units = [" °C"," °C",
                    " °C"," °C",
                    " °C"," °C",
                    " °C"," °C",
                    " °"," °/s",
                    " mW"," A",
                    " W"," Pa/s",
                    " 1/s"," 1/s",
                    " 1/s"," 1/s"]
    #Datos
    Data_names = ["Data1", "Data2",
                  "Data3", "Data4"]
    infusion_data = np.empty([1,4])
    infusion_data_max = np.empty([1,4])
    buffer_infusion_data = np.zeros([1,4])
    Data_units = ["a","b",
                  "c","d"]

    status_change_name = []
    status_change_time = []

    status_line_style = []
    #Tiempo en segundos
    time = np.empty([1,1])
    #Número de cafés procesados
    coffee_count = 0
    graph_data_count = 0
    while True:
        nl += 1;
        #Obtenemos la información del archivo linea por linea
        line = log.readline()
        #Finalizamos la lectura del registro cuando se deba
        if not line:
            graficar(time,Sensor_data,Sensor_names,Sensor_units,infusion_data,Data_names,Data_units,coffee_count)
            break;

        #Separamos los parametros que conforman cada línea
        #[FECHA Y HORA, CLASIFICACION, DATOS...]
        parametros = line.split(",")
        #Revisamos la cadena devuelta para "CLASIFICACION"
        #Si coincide con la cadena " Estoy en START" se acaba de iniciar
        #un proceso de infusión
        if len(parametros)< 2:
            continue
        
        if parametros[1] == " Estoy en START\n":

            if coffee_count > 0:
                graficar(time,Sensor_data,Sensor_names,Sensor_units,infusion_data,Data_names,Data_units,coffee_count)
                Sensor_data = np.empty([1,18])
                Sensor_data_max = np.empty([1,18])
                infusion_data = np.empty([1,4])
                infusion_data_max = np.empty([1,4])
                time = np.empty([1,1])

            #guardamos el tiempco en el que empezó el proceso
            time_txt = parametros[0].split()
            time_txt = time_txt[1].split(":")
            time[0,0] = 3600*float(time_txt[0]) + 60*float(time_txt[1]) + float(time_txt[2])

            coffee_count += 1

            #Como las lineas vienen por pares, encontrar una línea de Datos asegura que la siguiente es una línea de sensores
        if parametros[1] == " Data" and coffee_count > 0 and parametros[7] == "UI\n":
            nl +=1
            #Obtenemos el tiempo del registro respecto al inicio del proceso
            time_txt = parametros[0].split()
            time_txt = time_txt[1].split(":")
            buffer_time = np.zeros([1,1])
            buffer_time[0,0] = 3600*float(time_txt[0]) + 60*float(time_txt[1]) + float(time_txt[2])
            buffer_time[0,0] = buffer_time[0,0] - time[0,0]

            #Por si algún wey se hace un café a media noche >:v
            if buffer_time[0,0] < 0:
                buffer_time[0,0] = 3600*float(time_txt[0]) + 60*float(time_txt[1]) + float(time_txt[2])
                buffer_time[0,0] += (3600*24 - time[0,0])
            time = np.vstack([time,buffer_time])

            #Obtenemos los datos de la infusión
            for i in range(2,6):
                buffer_infusion_data[0,i-2] = float(parametros[i])
            infusion_data = np.vstack([infusion_data, buffer_infusion_data])
            buffer_infusion_data = np.zeros([1,4])

            #Obtenemos de una vez la siguiente línea del archivo
            sensor_data_txt = log.readline()
            sensor_params = sensor_data_txt.split(",")
            sensor_params = sensor_params[2].split()

            #Quitamos la primera parte de los códigos CSI
            for i in range(1,19):
                string = Sensor_names[i-1] + "\x1b[0m"
                sensor_params[i] = sensor_params[i].split(string)

            #Quitamos la segunda parte
            string = "\x1b[1;31m"
            sensor_params[1] = sensor_params[1][1].split(string)
            string = "\x1b[1;33m"
            sensor_params[7] = sensor_params[7][1].split(string)
            sensor_params[18] = sensor_params[18][1].split(string)

            for i in [2,3,4,5,6]:
                string = "\x1b[1;32m"
                sensor_params[i] = sensor_params[i][1].split(string)

            for i in [8,9]:
                string = "\x1b[1;34m"
                sensor_params[i] = sensor_params[i][1].split(string)

            for i in [10,11,12]:
                string = "\x1b[1;36m"
                sensor_params[i] = sensor_params[i][1].split(string)

            for i in [13,14,15,16,17]:
                string = "\x1b[1;35m"
                sensor_params[i] = sensor_params[i][1].split(string)
            for i in range(1,19):
                sensor_params[i] = sensor_params[i][0]
                buffer_sensor_data[0,i-1] = float(sensor_params[i])

            #buffer_sensor_data[0,18] = float(sensor_params[18])

            Sensor_data = np.vstack([Sensor_data,buffer_sensor_data])
            buffer_sensor_data = np.zeros([1,18])


    #Cerramos el archivo
    log.close()