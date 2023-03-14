import argparse
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

#FUNCIONES
def createFolder(fileName):
    Name = fileName.split('\\')
    Name = Name[len(Name)-1]
    Name = Name.split('.')
    Name = Name[0]
    currentDir = os.getcwd()
    foldername = "\\"+ Name
    FolderPath = currentDir+foldername
    if not os.path.exists(FolderPath):
        os.makedirs(FolderPath, exist_ok=True)
    return FolderPath

def graficar(time,sensor_data,sensor_names, sensor_units,infusion_data,infusion_names, infusion_units, n_infusion,fileName):
    i_color = 0;
    colors = ['b','g','r','c','m','y','k','brown']
    t = time[1:len(time),:];
    s_data = sensor_data[1:len(sensor_data),:]
    i_data = infusion_data[1:len(infusion_data),:]
    s_names = sensor_names
    s_units = sensor_units
    i_names = infusion_names
    i_units = infusion_units
    
    sensor_data_max = np.empty([1,18])

    temperature_title = "Temperaturas"
    motor_title = "Estados del motor"
    ADCs_rate_title = "Frecuencia de los ADC"
    infusion_tube_title = "Estado del tubo"

    data_title = i_names

    data_figure_title = "Datos de la infusion {infusion}".format(infusion=n_infusion)
    sensor_figure_title = "Datos de sensores en la infusion {infusion}".format(infusion=n_infusion)

    sensor_figure, ((internal_temp, motor),(ADCs, potencia)) = plt.subplots(2,2)
    external_temp = internal_temp.twinx()
    p_r = ADCs.twinx()

    data_figure, preassure = plt.subplots()
    flow = preassure.twinx()
    temp = preassure.twinx()
    weight = preassure.twinx()
    weight.tick_params(bottom=False,left=True,right=False,top=False,labelbottom=False,labelleft=True,labelright=False,labeltop=False)
    weight.yaxis.set_label_position('left')
    temp.spines.right.set_position(("outward",70))
    weight.spines.left.set_position(("outward",70))
    data_plots = [preassure, flow, weight, temp]    
    
    current = motor.twinx()

    sensor_figure.suptitle(sensor_figure_title)
    data_figure.suptitle(data_figure_title)

    legends = []
    lineas = []

    for internal_temps in range(2,8):
        legend = s_names[internal_temps] #+ " x{multiplicador}".format(multiplicador=multi)
        lineas += internal_temp.plot(t,s_data[:,internal_temps],label=legend,color=colors[i_color])
        i_color+=1

    for external_temps in range(0,2):
        legend = s_names[external_temps] #+ " x{multiplicador}".format(multiplicador=multi)
        lineas += external_temp.plot(t,s_data[:,external_temps], linestyle = "dashed", label=legend,color=colors[i_color])
        i_color+=1

    i_color = 0
    for lin in lineas:
        legends.append(lin.get_label())

    internal_temp.legend(lineas, legends)
    internal_temp.set_ylabel("internal temps °C")
    internal_temp.set_title("Temperaturas")
    external_temp.set_ylabel("external temps °C \n (dashed)")
    legends = []
    lineas = []
    
    for sensor in [8,9]:
        legend = s_names[sensor] + " {unidades}".format(unidades=s_units[sensor],color = colors[i_color])
        lineas += motor.plot(t,s_data[:,sensor],label=legend)
        i_color +=1
    legend = s_names[11] + " {unidades}".format(unidades=s_units[11])
    lineas += current.plot(t,s_data[:,11],linestyle = "dashed",label=legend,color=colors[i_color])
    i_color=0

    for lin in lineas:
        legends.append(lin.get_label())

    motor.legend(lineas,legends)
    motor.set_title("Estados del motor")
    current.set_ylabel("(dashed)")
    legends = []
    lineas = []

    for sensor in [10,12]:
        legend = s_names[sensor] + " {unidades}".format(unidades=s_units[i_color])
        lineas += potencia.plot(t,s_data[:,sensor],label=legend)
        i_color +=1
    
    i_color=0
    for lin in lineas:
        legends.append(lin.get_label())

    potencia.legend(lineas, legends)
    potencia.set_title("Potencia")
    potencia.set_xlabel("segundos")
    legends = []
    lineas = []

    multi = sensor_data_max[0,13]
    legend = s_names[13]
    lineas += p_r.plot(t,s_data[:,13], linestyle = "dashed", label=legend, color=colors[0])

    for i in range(14,18):
        i_color +=1
        multi = sensor_data_max[0,i]
        legend = s_names[i] #+ " x{multiplicador}".format(multiplicador=multi)
        lineas += ADCs.plot(t,s_data[:,i],label=legend,color = colors[i_color])
    i_color = 0

    for lin in lineas:
        legends.append(lin.get_label())

    ADCs.legend(lineas,legends)
    ADCs.set_ylabel("ADC freq (Hertz)")
    p_r.set_ylabel("preassure rate \n (dashed)")
    ADCs.set_title("Frecuencia de los ADC")
    ADCs.set_xlabel("segundos")

    lineas = []
    legends = []

    folderPath = createFolder(fileName)
    _figName = folderPath+"\\"+sensor_figure_title+".png"
    sensor_figure.set_size_inches(19.2,10.8)
    sensor_figure.savefig(_figName,dpi=100,format="png")
    plt.close(sensor_figure)

    data = 0
    for plot in data_plots:
        legend = data_title[data] + " {unidades}".format(unidades=i_units[data])
        if data > 1 :
            lineas += plot.plot(t,i_data[:,data],label=legend,linestyle="dashed",color=colors[data])
            data +=1
            continue
        lineas += plot.plot(t,i_data[:,data],label=legend,color=colors[data])
        data +=1
    preassure.set_ylabel(i_names[0])
    flow.set_ylabel(i_names[1])
    weight.set_ylabel(i_names[2])
    temp.set_ylabel(i_names[3])
    i_color = 0

    for lin in lineas:
        legends.append(lin.get_label())

    preassure.legend(lineas,legends)
    preassure.set_xlabel("segundos")
    data_figure.set_size_inches(19.2,10.8)
    _figName = folderPath+"\\"+ data_figure_title+".png"
    data_figure.savefig(_figName,dpi=100,format="png")
    plt.close(data_figure)



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
                    " Hz"," Hz",
                    " Hz"," Hz"]
    #Datos
    Data_names = ["Pressure", "Flow",
                  "Weight", "Temp"]
    infusion_data = np.empty([1,4])
    infusion_data_max = np.empty([1,4])
    buffer_infusion_data = np.zeros([1,4])
    Data_units = ["Pa","ml/s",
                  "g","°C"]

    #Tiempo en segundos
    time = np.empty([1,1])
    #Número de cafés procesados
    coffee_count = 0

    while True:
        nl += 1;
        #Obtenemos la información del archivo linea por linea
        line = log.readline()
        #Finalizamos la lectura del registro cuando se deba
        if not line:
            graficar(time,Sensor_data,Sensor_names,Sensor_units,infusion_data,Data_names,Data_units,coffee_count,args.name)
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
                graficar(time,Sensor_data,Sensor_names,Sensor_units,infusion_data,Data_names,Data_units,coffee_count,args.name)
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