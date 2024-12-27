'''
"""
This module provides a decorator to measure the execution time of functions and count how many times they are called.
The total times and call counts are saved in a log file. Each time a decorated function is called, the times and counts
are updated and written to the file. The log file is overwritten each time a decorated function is called.
Attributes:
    execution_totals (dict): Dictionary to store the total execution times of functions.
    call_counts (dict): Dictionary to store the call counts of functions.
    log_file (str): The name of the log file where execution times and call counts are saved.
Functions:
    write_log(): Writes the total execution times and call counts to the log file.
    timer(func): Decorator to measure the cumulative execution time and count the calls of a function.
"""

'''
import time

# Dizionari per salvare i tempi totali e i conteggi delle chiamate
execution_totals = {}
call_counts = {}

# Nome del file per il log
log_file = "TSP/outputs/logs/execution_times.log"

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
