# -*- coding: utf-8 -*-

import pandas as pd

# Διαβάζουμε το αρχείο αποτελεσμάτων
input_file = "spechmmer_results.txt"  # Το όνομα του αρχείου .txt
output_file = "spechmmer_results.xlsx"  # Το όνομα του αρχείου .xlsx

# Φορτώνουμε το .txt αρχείο 
# Χρησιμοποιούμε το πρώτο row ως κεφαλίδες (columns)
data = pd.read_csv(input_file, delim_whitespace=True)

# Αποθηκεύουμε σε αρχείο Excel
data.to_excel(output_file, index=False)

print("Το Excel αρχείο δημιουργήθηκε επιτυχώς: {}".format(output_file))


