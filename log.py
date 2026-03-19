import os
import re
import csv

def extract_values():
    base_dir = "computations"
    output_file = "results.csv"
    h_to_kcal = 627.509
    
    zpe_pattern = re.compile(r"Zero point energy.*?\s([\d.]+)\skcal/mol")
    spe_pattern = re.compile(r"FINAL SINGLE POINT ENERGY\s+(-?[\d.]+)")

    existing_labels = set()

    # 1. Check which labels we've already processed
    if os.path.exists(output_file):
        with open(output_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                existing_labels.add(row['label'])

    # 2. Determine if we need to write a header (only if file is new/empty)
    file_exists = os.path.exists(output_file) and os.path.getsize(output_file) > 0

    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} directory not found.")
        return

    # 3. Open in append mode
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['label', 'zpe_kcal_mol', 'spe_kcal_mol']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()

        for label in os.listdir(base_dir):
            subdir_path = os.path.join(base_dir, label)
            
            # Skip if it's not a directory or if we've already logged this label
            if not os.path.isdir(subdir_path) or label in existing_labels:
                continue

            zpe_val = "N/A"
            spe_val_kcal = "N/A"

            # Parse freq.log
            freq_path = os.path.join(subdir_path, "freq.log")
            if os.path.exists(freq_path):
                with open(freq_path, 'r') as f:
                    match = zpe_pattern.search(f.read())
                    if match:
                        zpe_val = match.group(1)

            # Parse calc.log
            calc_path = os.path.join(subdir_path, "calc.log")
            if os.path.exists(calc_path):
                with open(calc_path, 'r') as f:
                    match = spe_pattern.search(f.read())
                    if match:
                        spe_val_hartree = float(match.group(1))
                        spe_val_kcal = round(spe_val_hartree * h_to_kcal, 6)

            # Write the new row immediately
            writer.writerow({
                "label": label,
                "zpe_kcal_mol": zpe_val,
                "spe_kcal_mol": spe_val_kcal
            })
            print(f"Processed new entry: {label}")

    print("Update complete.")

if __name__ == "__main__":
    extract_values()