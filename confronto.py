import multiprocessing as mp
import threading as th
import time
import os

nm = 4 #numero di processi / thread

def we_rallenta_cap_e_provola():
    '''funzione che aspetta un secondo
    '''
    PID = os.getpid()
    pro = mp.current_process().name
    thr = th.current_thread().name
    print(f"PID: {PID}, Process Name: {pro}, Thread Name: {thr}")

    time.sleep(1)

def we_rallenta_cap_e_provola2():
    '''funzione che fa cacloli
       come semplice esempio si limita a contare
    '''
    PID = os.getpid()
    pro = mp.current_process().name
    thr = th.current_thread().name
    print(f"PID: {PID}, Process Name: {pro}, Thread Name: {thr}")

    x = 0
    N = int(1e7)
    while x < N:
        x += 1

def benchmark():

    print("esecuzione sleep")

    #esecuzione seriale
    start = time.time()
    for _ in range(nm):
        we_rallenta_cap_e_provola()
    end = time.time()

    print("Tempo di esecuzione seriale = ", end - start)
    print("\n")

    #esecuzione con thread
    start = time.time()

    thr = [th.Thread(target=we_rallenta_cap_e_provola) for _ in range(nm)]
    for t in thr: t.start()
    for t in thr: t.join()

    end = time.time()

    print("Tempo di esecuzione con thread = ", end - start)
    print("\n")

    #esecuzione con i processi
    start = time.time()

    pro = [mp.Process(target=we_rallenta_cap_e_provola) for _ in range(nm)]
    for p in pro: p.start()
    for p in pro: p.join()

    end = time.time()

    print("Tempo di esecuzione con processi = ", end - start)
    print("\n")

    print("esecuzione con calcoli")

    #esecuzione seriale
    start = time.time()
    for _ in range(nm):
        we_rallenta_cap_e_provola2()
    end = time.time()

    print("Tempo di esecuzione seriale = ", end - start)
    print("\n")

    #esecuzione con thread
    start = time.time()

    thr = [th.Thread(target=we_rallenta_cap_e_provola2) for _ in range(nm)]
    for t in thr: t.start()
    for t in thr: t.join()

    end = time.time()

    print("Tempo di esecuzione con thread = ", end - start)
    print("\n")

    #esecuzione con i processi
    start = time.time()

    pro = [mp.Process(target=we_rallenta_cap_e_provola2) for _ in range(nm)]
    for p in pro: p.start()
    for p in pro: p.join()

    end = time.time()

    print("Tempo di esecuzione con processi = ", end - start)

if __name__ == "__main__":

    benchmark()