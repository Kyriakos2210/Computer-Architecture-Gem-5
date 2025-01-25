#!/bin/bash

# Ορισμός των τιμών για κάθε παράμετρο
L1I_SIZES=(32kB 64kB)
L1I_ASSOCS=(1 2 4)
L1D_SIZES=(64kB 128kB)
L1D_ASSOCS=(1 2 4)
L2_SIZES=(2MB 3MB 4MB)
L2_ASSOCS=(8 16)
CACHELINE_SIZES=(32 64 128)

# Επανάληψη μέσω όλων των συνδυασμών
for l1i_size in "${L1I_SIZES[@]}"; do
  for l1i_assoc in "${L1I_ASSOCS[@]}"; do
    for l1d_size in "${L1D_SIZES[@]}"; do
      for l1d_assoc in "${L1D_ASSOCS[@]}"; do
        for l2_size in "${L2_SIZES[@]}"; do
          for l2_assoc in "${L2_ASSOCS[@]}"; do
            for cacheline_size in "${CACHELINE_SIZES[@]}"; do

              # Δημιουργία μοναδικού ονόματος για τον φάκελο αποθήκευσης αποτελεσμάτων
              output_dir="spec_results/specmcf_icache_${l1i_size}_${l1i_assoc}assoc_\
dcache_${l1d_size}_${l1d_assoc}assoc_l2_${l2_size}_${l2_assoc}assoc_line_${cacheline_size}"

              # Έλεγχος αν υπάρχει ήδη αποτέλεσμα
              result_file="${output_dir}/results.txt"  # Υποθέτουμε ότι το αρχείο results.txt είναι η έξοδος
              if [ -e "$result_file" ] && [ -s "$result_file" ]; then
                echo "Skipping existing simulation: $output_dir"
                continue
              fi

              # Δημιουργία φακέλου αποτελεσμάτων
              mkdir -p "$output_dir"

              # Εκτέλεση της εντολής
              echo "Running simulation for ICache=$l1i_size, ICacheAssoc=$l1i_assoc, \
DCache=$l1d_size, DCacheAssoc=$l1d_assoc, L2=$l2_size, L2Assoc=$l2_assoc, Cacheline=$cacheline_size"
              ./build/ARM/gem5.opt -d "$output_dir" \
                configs/example/se.py \
                --cpu-type=MinorCPU \
                --caches \
                --l2cache \
                --l1i_size="$l1i_size" \
                --l1i_assoc="$l1i_assoc" \
                --l1d_size="$l1d_size" \
                --l1d_assoc="$l1d_assoc" \
                --l2_size="$l2_size" \
                --l2_assoc="$l2_assoc" \
                --cacheline_size="$cacheline_size" \
                --cpu-clock=1GHz \
                -c spec_cpu2006/429.mcf/src/specmcf \
                -o "spec_cpu2006/429.mcf/data/inp.in" \
                -I 100000000

            done
          done
        done
      done
    done
  done
done
