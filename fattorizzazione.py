import time
import multiprocessing as mp



def fattori(n):
    '''
    Calcolo brutale dei fattori primi di un numero
    Parameters
    ----------
    n : int
        numero di cui calcolare i fattori primi

    Returns
    ----------
    f : list
        lista dei fattori primi di n
    '''
    i = 2
    f = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            f.append(i)
    if n > 1:
        f.append(n)
    return f


def seriale(nft):
    '''
    Funzione che chima serialmente la funzione per
    fattorizzare dei numeri

    Parameters
    ----------
    nft : list
        lista dei numeri da fattorizzare

    Returns
    ----------
    dizionario contenente le fattorizzazzione
    '''
    return {n: fattori(n) for n in nft}


def process_output(ntf, out_pro):
    '''
    Funzione che chima si serialmente la funzione per
    fattorizzare dei numeri, ma viene eseguita
    dai vari processi parallelamente

    Parameters
    ----------
    ntf : list
        lista di numeri da fattorizzare assegnata ad un processo
    out_pro : method
        coda degli output
    '''
    out = {}

    for n in ntf:
        out[n] = fattori(n)

    out_pro.put(out)


def process_factor(ntf, npro):
    '''
    Funzione che crea i processi che verranno utilizzati

    Parameters
    ----------
    ntf : list
        lista completa dei numeri da fattorizzare
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
    dim = int(len(ntf)/npro + 1)

    #ciclo sul numero di processi per crearli
    for i in range(npro):
        #definisco i processi
        p = mp.Process(target=process_output, args=(ntf[dim*i : dim*(i + 1)], out))
        #li inserisco nella lista
        pro.append(p)
        #avvio i processi
        p.start()

    #racccolgo i risultati in un dizionanrio
    result = {}
    for i in range(npro):
        result.update(out.get())

    #attendo la fine dei processi
    for p in pro:
        p.join()

    return result


def test(ntf):
    '''
    test delle prestazioni di calcolo seriale e parallelo
    stampa su shell il tempo impiegato per il calcolo

    Parameters
    ----------
    ntf : list
        lista completa dei numeri da fattorizzare

    '''
    #test seriale
    start = time.time()
    seriale(ntf)
    end = time.time() - start
    print(f"serial time: {end:.3f}")

    #ciclo sul numero di processi
    for npro in [2, 4, 8]:
        start = time.time()
        process_factor(ntf, npro)
        end = time.time() - start
        print(f"process time: {end:.3f} with {npro} processes")


if __name__ == "__main__":

    #quanti numeri fattorizzare
    N = 300

    #creao la lista di numeri da fattorizzare
    ntf = [999999999999]
    for i in range(N):
        ntf.append(ntf[-1] + 2)

    #benchmark
    test(ntf)
