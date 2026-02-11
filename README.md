#  Wildfire Watch-1: CubeSat Digital Twin

A Python-based **Digital Twin** for a wildfire-monitoring CubeSat. This system integrates orbital mechanics (TLE tracking), synthetic thermal IR data generation, and an automated parametric insurance trigger.

##  Overview

This simulation demonstrates an end-to-end satellite mission workflow:

1. **Orbital Propagation:** Real-time tracking of satellite coordinates using TLE data.
2. **Thermal Imaging:** Generation of synthetic 64x64 thermal grids with noise and fire anomalies.
3. **AI Edge Processing:** Noise filtering and confidence scoring for fire detection.
4. **Parametric Trigger:** Automated "Smart Contract" payout simulation once confidence exceeds 85%.

##  Installation

Ensure you have Python 3.8+ installed, then install the dependencies:

```bash
pip install numpy skyfield flask matplotlib

```

## How to Run

1. Clone the repository.
2. Execute the simulation:
```bash
python main.py

```


3. Open your browser to `http://127.0.0.1:5001` to view the **Mission Dashboard**.
4. Check the `/outputs` directory for generated thermal heatmaps.

## Technical Specs

* **Sensor Resolution:** 100m Ground Sample Distance (GSD).
* **Thermal Threshold:**  for wildfire flagging.
* **Orbital Data:** ISS TLE (International Space Station) as a proxy.
* **Confidence Logic:** Payouts trigger only when cluster size and temperature intensity meet the AI filter criteria.

## Configuration

Modify the following constants in the source code to change simulation behavior:

* `MISSION_BUDGET_USD`: Simulated financial cap.
* `TEMP_THRESHOLD_CELSIUS`: Sensitivity of the fire sensor.
* `SENSOR_GSD_M`: Spatial resolution adjustment.

---

**License:** MIT
**Disclaimer:** This is a digital twin simulation for educational and prototyping purposes only.
