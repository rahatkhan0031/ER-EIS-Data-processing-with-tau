# ER-EIS Processing with Tau

This repository contains a Python script for processing ER-EIS measurement data exported from EC-Lab text files.

## Features

- Reads ER-EIS `.txt` files
- Converts measurement data into numeric format
- Removes invalid rows
- Calculates recombination lifetime `τ`
- Calculates `Ket`
- Converts electrochemical potential to vacuum energy scale
- Calculates DOS in `cm^-3 eV^-1`
- Exports processed data to Excel

## Parameters used

- Film thickness `L`
- Electrolyte factor `A`
- Active surface fraction `Vf`
- Electrode area `S`
- Elementary charge `e`

## Calculations included

- Recombination lifetime: `τ = Rct × Cμ`
- Charge transfer rate constant: `Ket = L / (Vf × A × Rct × Cμ)`
- Energy conversion: `E_vac = -4.66 - Ewe`
- DOS calculation in `cm^-3 eV^-1`

## Requirements

- Python 3
- pandas
- openpyxl

## Installation

Install the required packages:

```bash
pip install pandas openpyxl
