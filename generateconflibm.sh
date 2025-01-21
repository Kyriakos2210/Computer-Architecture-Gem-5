#!/bin/bash

# Ορισμός του directory που περιέχει τα αποτελέσματα
RESULTS_DIR="spec_results"
OUTPUT_FILE="conf_libm.ini"

# Αρχικοποίηση του αρχείου εξόδου
cat > "$OUTPUT_FILE" <<EOL
[Benchmarks]
EOL

# Προσθήκη όλων των φακέλων που ξεκινούν με "speclibm_"
for dir in "$RESULTS_DIR"/speclibm_*; do
  if [ -d "$dir" ]; then
    benchmark_name=$(basename "$dir")
    echo "$benchmark_name" >> "$OUTPUT_FILE"
  fi
done

# Προσθήκη των παραμέτρων και του αρχείου εξόδου
cat >> "$OUTPUT_FILE" <<EOL

[Parameters]
system.cpu.cpi
system.cpu.dcache.overall_miss_rate::total
system.cpu.icache.overall_miss_rate::total
system.l2.overall_miss_rate::total

[Output]
speclibm_results.txt
EOL

# Ενημέρωση χρήστη
echo "Το αρχείο $OUTPUT_FILE δημιουργήθηκε επιτυχώς."
