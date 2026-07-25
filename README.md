# Solar Cooling System Design for Artisanal Fishing 🎣🧊

This repository contains a Python tool for sizing and thermal design of an **off-grid solar vapor-compression refrigeration system** integrated with **Phase Change Materials (PCM)**, specifically designed for preservation in artisanal fishing.

---

## 📌 Features & Calculations
The script performs comprehensive engineering sizing based on physical parameters and thermal properties:

* **Thermal Load Estimation:** Calculates transmission losses (PUR insulation), product cooling loads (fish & ice balancing), and total daily energy requirements ($MJ/day$).
* **PCM Thermal Storage:** Sizes the required PCM mass (`E-3 PlusIce Eutectic`) and its relative volume inside the cabinet.
* **Thermodynamic Cycle:** Determines evaporator/condenser thermal capacities ($W$) and refrigerant mass flow rate ($R600a$).
* **Heat Exchanger Sizing (LMTD Method):**
  * **Finned-Tube Condenser:** Overall heat transfer coefficient ($U$), cross-flow correction factor ($F$), total tube length, and cut segment counts.
  * **Bare-Tube Submerged Evaporator:** Overall heat transfer coefficient ($U$) and required tube length.
* **Photovoltaic Array Sizing:** Determines daily electrical energy demand and total solar panels required based on peak sun hours (HSP).
* **Automated Visual Report:** Generates and saves a publication-ready summary table using `matplotlib`.

---

## 🛠️ Inputs & Outputs

### Key Inputs
* **Cabinet Geometry:** Length, width, height, and insulation specs ($k_{PUR}$, thickness).
* **Product Parameters:** Fish mass ($300\text{ kg}$), ice mass ($100\text{ kg}$), target temperatures.
* **Tube Geometries:** Condenser ($3/8"$) and Evaporator ($1/2"$) copper diameters.
* **Solar Parameters:** HSP ($4.5\text{ hours}$), panel wattage ($630\text{ W}$), system efficiencies.

### Expected Outputs
* Required mass and volume fraction of PCM.
* Total required copper tube lengths ($m$) for both evaporator and condenser.
* Number of required solar panels ($630\text{ W}$).
* Formatted summary image (`tabla_resultados_diseno.png`).

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone [https://github.com/TuUsuario/design_solar_cooling_fishing.git](https://github.com/TuUsuario/design_solar_cooling_fishing.git)
   
2. Install required dependencies:   
   pip install matplotlib
   import math

4. Run the script:
   python "Calculo Termico Diseño de forma.py"
