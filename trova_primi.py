import time
import numpy as np
import scipy.special as sc
import multiprocessing as mp
import matplotlib.pyplot as plt

def isPrime(n):
    '''test di primalità
    '''
    if n == 1 or n%2 == 0 and n != 2:
         return False

    for i in range(3, n//2, 2):
        if(n%i == 0):
             return False

    return True


def process_output(numbers, out_pro):
    '''funzione che restituisce una lista contenente i numeri primi
       come parametri prende la lista di numeri di cui controllare la primalità
       e l'output per poter comunicare con la funzione process_prime
    '''
    x = []
    for i in numbers:
        if(isPrime(i)):
            x.append(i)

    out_pro.put(x)


def process_prime(numbers, npro):
    '''funzione che crea i processi che verranno utilizzati
       i parametri sono la lista di numeri di cui controllare la primalità e
       il numero di processi da eseguire
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

def g(x):
    '''approssimazione della funzione enumerativa
    '''
    return x/np.log(x)

def Li(x):
    '''approssimazione della funzione enumerativa, migliore della precedente
    '''
    return sc.expi(np.log(x))


def plot(a):
    '''grafico della funzione enunumerativa
       prende in imput la "lista" dei primi
    '''
    #inserisco i primi in una lista, a è una lista di liste
    x = []
    for i in range(len(a)):
         for j in a[i]:
             x.append(j)

    #array per il plot
    y = np.linspace(0, len(x)-1, len(x)) #array numero primi minori di
    t = np.linspace(2, x[-1], 10000)

    plt.figure(1)
    plt.grid()
    plt.title('Funzione enumerativa dei numeri primi')
    plt.plot(x, y, color='black', label=r'$ \pi(x) $')
    plt.plot(t, Li(t), color='red', label='Li(x)')
    plt.plot(t, g(t), color='blue', label=r'$\frac{x}{\lnx} $')
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":

    N = int(1e4)
    #lista di numeri di cui controllare la primalità
    numbers = range(N)

    npro = 4 #numero processi da eseguire

    start = time.time()

    a = process_prime(numbers, npro)

    end = time.time() - start

    #ordino la lista perchè non so di principio in che ordine i processi finiscono
    a.sort()

    plot(a) #grafico della funzione enunumerativa

    print(f"time: {end:.3f}")
