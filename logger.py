# logger.py
import time

# Questo modulo serve per misurare il tempo di esecuzione di una funzione e per contare quante volte viene chiamata.
# I tempi totali e i conteggi delle chiamate vengono salvati in un file di log.
# Ogni volta che una funzione decorata viene chiamata, i tempi e i conteggi vengono aggiornati e scritti nel file.
# Il file di log viene sovrascritto ogni volta che viene chiamata una funzione decorata.
# Le funzioni tipicamente decorate con @timer sono: nearest_neighbor_random, nearest_neighbor_second, local_search, multi_start_local_search, swap_neighborhood, two_opt_neighborhood. 


# Dizionari per salvare i tempi totali e i conteggi delle chiamate
execution_totals = {}
call_counts = {}

# Nome del file per il log
log_file = "execution_times.log"

# Funzione per scrivere i tempi e i conteggi nel log
def write_log():
    with open(log_file, "w") as f:
        for func_name, total_time in execution_totals.items():
            count = call_counts[func_name]
            f.write(f"{func_name}: {total_time:.4f} secondi totali, {count} chiamate\n")

# Decoratore per misurare il tempo cumulativo e contare le chiamate
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time

        # Aggiorna il tempo totale di esecuzione
        if func.__name__ in execution_totals:
            execution_totals[func.__name__] += elapsed_time
            call_counts[func.__name__] += 1  # Incrementa il conteggio delle chiamate
        else:
            execution_totals[func.__name__] = elapsed_time
            call_counts[func.__name__] = 1  # Inizializza il conteggio a 1

        # Scrivi i tempi totali e i conteggi nel file ogni volta che viene chiamata la funzione
        write_log()

        return result
    return wrapper
