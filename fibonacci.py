import time
import numpy as np
import multiprocessing as mp


def fibonacci(n):
    '''restituisce l'n-esimo numero di fibonacci
    '''
    if n  in [0, 1]:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def process_output(numbers, out_pro):
    '''
    Funzione che chima si serialmente la funzione per
    trovare l'n-esimo numero di fibonacci, ma viene eseguita
    dai vari processi parallelamente

    Parameters
    ----------
    numbers : list
        lista di numeri di cui calcolare il numero
        di fibonaccci assegnata ad un processo

    out_pro : method
        coda degli output
    '''
    x = []
    for i in numbers:
        f = fibonacci(i)
        x.append(f)

    out_pro.put(x)


def process_fibo(numbers, npro):
    '''
    Funzione che crea i processi che verranno utilizzati

    Parameters
    ----------
    numbers : list
        lista completa di numeri di cui calcolare
        il numero di fibonaccci
    npro : int
        numero di processi da eseguire

    Returns
    ----------
    result : dict
        dizionario contenente tutti gli output
    '''

    out = mp.Queue() # coda degli output
    pro = [] #lista dei processi

    #dimesione del blocco che passo ad ogni processo
    dim = int(len(numbers)/npro + 1)

    #ciclo sul numero di processi per crearli
    for i in range(npro):
        #definisco i processi
        p = mp.Process(target=process_output, args=(numbers[dim*i : dim*(i + 1)], out))
        #li inserisco nella lista
        pro.append(p)
        #avvio i processi
        p.start()

    #racccolgo i risultati in una lista
    result = []
    for i in range(npro):
        result.append(out.get())

    #attendo la fine dei processi
    for p in pro:
        p.join()

    return result



if __name__ == "__main__":

    N = 30 #quanti numeri calcolare

    numbers = range(N)

    npro = 4 #numero processi da eseguire

    start = time.time()

    a = process_fibo(numbers, npro)

    end = time.time() - start

    #ordino la lista perchè non so di principio in che ordine i processi finiscono
    a.sort()
    print(a)

    print(f"time: {end:.3f}")
