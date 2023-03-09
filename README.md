# README
## Ejecución
Este script es apto para ser llamado desde la consola, *(o su terminal favorita)*. Para ser llamado debe ejecutarse el siguiente comando

> python graph_log.py path-del-archivo

Si el archivo se encuentra en la misma carpeta, basta con escribir su nombre (del archivo [sé que no es necesario, per vale la pena aclararlo ]) sin olvidar su extensión

> python graph_log.py path-del-archivo

### Ejemplo

> python greph_log.py "Fika_2023_03_06_143.txt"


## Graficado
Respecto a las sugerencias de cómo mostrar las gráficas, preferí cambiarlo un poco ya que realmente se mostraban súper amontonados al estar todas en una gráfica así que preferí hacerlo de la sig. manera:
Se generan figuras en pares, cada par por "café hecho"

### Figura 1
en una figura se muestran los datos de los sensores en 4 gráficas agrupados casi por clasificación (temperaturas, motor, tubo de infusión y ADCs), todas con sus leyendas que explican el color y un multiplicador para conocer el dato real ya que se normalizaron los datos. Las leyendas traen las unidades del valor que representan a menos que toda la gráfica use las mismas unidades, en ese caso las unidades se presentan en el eje Y

### Figura 2
En la segunda figura se muestran en gráficas separadas los valores de los "datos de infusión", aquellos que me comentaste se muestran en la pantalla de la cafetera. Olvidé preguntar por el nombre de los datos es por eso que los manejé con titulos genéricos y no presentan unidades.

## Ejercicio al lector
En la parte superior del código se encuentran en forma de listas los nombres de los datos así como sus unidades. Por lo que desde ahí pueden cambiarse los nombres genéricos de la segunda figura. **Se deja como ejercicio al lector**

## Ejemplo de figuras
A continuación se muestran como ejemplo de ejecución del programa, las gráficas generadas para el archivo de prueba 

## Figura con datos de sensores
![infusion 6. Datos de sensores][def]

## Figura con datos de infusión
![infusion 6. Datos de pantalla][def2]

## NOTA
Las gráficas no avanzan a la siguiente infusión hasta que cierre el par de figuras

*Sin más por el momento. **Muchas gracias por su tiempo** y espero escuchar de vuelta. Cualquier comentario o recomendación es bienvenido, mientras me ayude a seguir mejorando. Que tengan un excelente día*

[def]: /infusion6_sensores.png "Datos de los sensores en la infusión 6"
[def2]: /infusion6_pantalla.png "Datos de la infusion 6"