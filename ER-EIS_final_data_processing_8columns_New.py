import pandas as pd
import re

def process_data_from_txt(input_file):
    # --- 1. Constants in SI units ---
    L = 300 * 10**(-9)      # 175 nm film thickness ->ITO
    A = 6 * 10**(25)        # Electrolyte factor in m^-3 
    Vf = 1                  # Active surface fraction
    
    # Additional constants
    e = 1.602176634e-19     # Elementary charge [C]
    S = 12 * 10**(-6)       # Electrode area: 12 mm^2 -> 1.2e-5 m^2 

    # --- 2. Read the text file ---
    # Using 'delimiter' consistent with your file format
    data = pd.read_csv(input_file, delimiter='\t', skiprows=1,
                       names=['Ewe/V', 'Re(Z)/Ohm', 'Cs/µF', 'Cp/µF'], encoding='utf-8')

    # --- 3. Convert string numbers to floats ---
    cols_to_fix = ['Ewe/V', 'Re(Z)/Ohm', 'Cs/µF', 'Cp/µF']
    for col in cols_to_fix:
        # Use simple string replace; assuming consistent format
        data[col] = data[col].astype(str).str.replace(',', '.').astype(float)

    # --- 4. Remove invalid rows (Re(Z)=0) ---
    filtered_data = data[data['Re(Z)/Ohm'] != 0].copy()

    # --- 5. Compute Ket in SI units (m^4/s) ---
    # Convert Cp/µF -> Cµ (Farads)
    Cmu_F = filtered_data['Cp/µF'] * 1e-6
    
    # --- Recombination lifetime tau (s): tau = Rct * Cmu ---
    filtered_data['Recombination lifetime τ (s)'] = filtered_data['Re(Z)/Ohm'] * Cmu_F

    valid = Cmu_F != 0
    # [cite_start]Eq 16: ket = L / (Vf * A * Rct * Cmu) [cite: 271]
    Ket_series = L / (Vf * A * filtered_data.loc[valid, 'Re(Z)/Ohm'] * Cmu_F[valid])

    filtered_data.loc[valid, 'Ket'] = Ket_series
    Ket_avg = Ket_series.mean()
    filtered_data['Ket'].fillna(Ket_avg, inplace=True)

    # --- 6. Energy axis conversion ---
    # [cite_start]E_vac = -(eU + 4.66) [cite: 235]
    filtered_data['-4.66 - Ewe'] = -4.66 - filtered_data['Ewe/V']

    # --- 7. DOS calculation (CORRECTED) ---
    # Step A: DOS in SI units (states per m^3 per Joule)
    # [cite_start]derived from Eq 17 [cite: 278]
    dos_SI_Joule = 1 / (e**2 * S * A * Vf * filtered_data['Re(Z)/Ohm'] * filtered_data['Ket'])

    # Step B: Convert units to cm^-3 eV^-1
    # 1. m^-3 -> cm^-3 : Multiply by 10^-6
    # 2. J^-1 -> eV^-1 : Multiply by e (1.602e-19)
    filtered_data["DOS (cm^-3 eV^-1)"] = dos_SI_Joule * e * 10**(-6)

    # Restore original units for capacitance columns if needed
    filtered_data['Cs/µF'] = filtered_data['Cs/µF']
    filtered_data['Cp/µF'] = filtered_data['Cp/µF']

    # --- 8. Save to Excel ---
    pattern = r'^(.*)\.txt$'
    match = re.match(pattern, input_file)
    file_name = match.group(1)

    output_file = file_name + ".xlsx"
    filtered_data.to_excel(output_file, index=False)
    print(f"File saved: {output_file}")


# Example usage
process_data_from_txt(
    r"C:\Users\rahat\OneDrive\Desktop\New2026\ITO+ZnO+HDMS\LUMO\LUMO_ZRI964_C01.txt")