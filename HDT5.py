#librerias importadas
import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

#Variables de la simulación y menú de opciones
print("Configuración del simulador")
RANDOM_SEED = 42
INTERVAL = int(input("Ingrese el intervalo de llegada de procesos: "))
RAM_CAPACITY = int(input("Ingrese la capacidad de la RAM: "))
CPU_SPEED = int(input("Ingrese la velocidad del CPU: "))
CPU_NUM = int(input("Ingrese el numero de CPUS para llevar a cabo el proceso: "))

#Mejor configuracion para reducir el tiempo de proceso.
#RANDOM_SEED = 42
#INTERVAL = 5
#RAM_CAPACITY = 200
#CPU_SPEED = 6
#CPU_NUM = 2

class Process:

    #Constructor con sus respectivos parametros utilizando self para acceder a atributos y metodos en una misma instancia de la clase Process
    def __init__(self, environment, name, ram, cpu):
        self.environment = environment
        self.name = name
        self.ram = ram
        self.cpu = cpu
        #representa la cantidad de  instrucciones que debe ejecutarse antes de terminar de compilar
        self.instructions = random.randint(1, 10)
        #Selecciona de manera la memoria usada.
        self.memory = random.randint(1, 10) 
        #instruccion para que termine el tiempo en que inicia y termine el programa.
        self.start_time = environment.now
        environment.process(self.run())
    
    #Funcion para ejecutar el proceso, solicitando la ram, instrucciones y gestionar los posibles errores.
    def run(self):
        #Solicita la memoria RAM que se utilizara
        #"yield" tiene la funcion de realizar una pausa por un tiempo antes de continuar con los siguientes procesos.
        yield self.ram.get(self.memory)

        #Preparacion para que se ejecute la CPU, al tener la RAM se considera en un estado listo o "Ready"
        while self.instructions > 0:
            #Evalua si se puede utilizar la cpu.
            with self.cpu.request() as req:
                yield req
                #Obtiene lo minimo de la velocidad de CPU para posteior ejecutarlo.
                execute_time = min(CPU_SPEED, self.instructions)
                yield self.environment.timeout(1)
                self.instructions -= execute_time
            
            #Al ser nulo, el programa termina con un break.
            if self.instructions == 0:
                break
            #El numero al ser igual a 1, empieza una operacion I/O, con la posibilidad de tardar de 1 a 3 unidades de tiempo para volver al estado normal "Ready"
            elif random.randint(1, 21) == 1:
                yield self.environment.timeout(random.randint(1, 3))
        
        #Libera la memoria RAM despues de terminar de ejecutar
        yield self.ram.put(self.memory)
        process_times.append(self.environment.now - self.start_time) 

#Funcion para la inicializacion de la simulacion y sus procesos
def setup(environment, num_processes, ram, cpu):
    for i in range(num_processes):
        Process(environment, f'Proceso{i}', ram, cpu)
        #Genera tiempos de llegada exponenciales que simula un proceso realista.
        yield environment.timeout(random.expovariate(1.0/INTERVAL))

random.seed(RANDOM_SEED)
num_processes_list = [25, 50, 100, 150, 200]
time_r = []

def run_simu():
    #Itera las cantidades de procesos a simular, en est caso: 25, 50, 100, 150, 200.
    for num_processes in num_processes_list:
        global process_times
        process_times = []
        #creacion del entorno donde se simula.
        environment = simpy.Environment()
        #Encargado de iniciar la RAM y manejar su capacidad maxima.
        ram = simpy.Container(environment, init = RAM_CAPACITY, capacity = RAM_CAPACITY)
        #Encargado de manejar la cpu como cuantoos se pueden utilzar al mismo tiempo o limitarla.
        cpu = simpy.Resource(environment, capacity = CPU_NUM)
        #inica la creacion de un proceso llamando la clase y teniendo como parametro la funcion setup con sus respectivos parametros.
        environment.process(setup(environment, num_processes, ram, cpu))
        #Ejecucion de la simulacion
        environment.run()
        #Calcula el promedio del tiempo que se ejecuta
        avg_t = np.mean(process_times)
        #Calcula la desviacion estandar del tiempo que se ejecuta
        std_t = np.std(process_times)
        #Agrega los resultados (num_procesos, promedio_tiempo, desviacion_estandar) a la lista time_r
        time_r.append((num_processes, avg_t, std_t))
        print(time_r)

run_simu()

#Funcion de grafica de resultado.
def plot_r():
    x, y, yerr = zip(*time_r)
    plt.errorbar(x, y, yerr=yerr, fmt='o', label = f'Intervalo {INTERVAL}')
    plt.xlabel('Num de procesos')
    plt.ylabel('Tiempo promedio (s)')
    plt.title('proceso de simulacion')
    plt.legend()
    plt.show()

plot_r()









