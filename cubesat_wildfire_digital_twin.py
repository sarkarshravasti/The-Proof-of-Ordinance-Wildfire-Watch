import time
import threading
import numpy as np
from skyfield.api import load, EarthSatellite
from flask import Flask
import matplotlib.pyplot as plt
import os


# CONFIGURATION
MISSION_BUDGET_USD = 2500
TEMP_THRESHOLD_CELSIUS = 45          # realistic wildfire threshold
SENSOR_GSD_M = 100                   # meters
TEMP_MIN = 20                        # °C (healthy vegetation)
TEMP_MAX = 60                        # °C (active fire)


# DASHBOARD STATE (GLOBAL)
dashboard_state = {
    "fire_detected": False,
    "latitude": "N/A",
    "longitude": "N/A",
    "confidence": "N/A",
    "payout_status": "Not Triggered"
}


# OUTPUT DIRECTORY

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# CUBESAT DIGITAL TWIN

class CubeSatDigitalTwin:
    def __init__(self):
        self.ts = load.timescale()
        line1 = '1 25544U 98067A   23001.50000000  .00000000  00000-0  00000-0 0  9998'
        line2 = '2 25544  51.6416  24.7712 0006703 130.5360 325.0288 15.50000000215754'
        self.satellite = EarthSatellite(line1, line2, 'WILDFIRE_WATCH_1', self.ts)

        self.veg_baseline_temp = 25.0
        self.fire_already_reported = False

        
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.colorbar_added = False

    def get_current_location(self):
        t = self.ts.now()
        subpoint = self.satellite.at(t).subpoint()
        return subpoint.latitude.degrees, subpoint.longitude.degrees

    def capture_thermal_data(self):
        grid = np.random.normal(27, 1.0, (64, 64))

        
        if np.random.rand() > 0.7:
            grid[28:36, 28:36] += 25

        return grid

    def apply_ai_noise_filter(self, grid):
        ys, xs = np.where(grid > TEMP_THRESHOLD_CELSIUS)
        return [(y, x) for y, x in zip(ys, xs)
                if 28 <= x <= 36 and 28 <= y <= 36]

    def calculate_confidence(self, fire_pixels):
        if not fire_pixels:
            return 0
        return min(95, 60 + len(fire_pixels) * 2)

    def compute_fire_location(self, fire_pixels, sat_lat, sat_lon):
        ys, xs = zip(*fire_pixels)
        cx, cy = np.mean(xs), np.mean(ys)

        dx_m = (cx - 32) * SENSOR_GSD_M
        dy_m = (cy - 32) * SENSOR_GSD_M

        lat_offset = dy_m / 111_320
        lon_offset = dx_m / (111_320 * np.cos(np.radians(sat_lat)))

        return sat_lat + lat_offset, sat_lon + lon_offset

    def visualize_thermal_map(self, grid, timestep):
        self.ax.clear()

        im = self.ax.imshow(
            grid,
            cmap="inferno",
            vmin=TEMP_MIN,
            vmax=TEMP_MAX
        )

        self.ax.set_title(f"Thermal IR Map | Time Step {timestep}")
        self.ax.set_xlabel("Pixel X")
        self.ax.set_ylabel("Pixel Y")

        if not self.colorbar_added:
            cbar = self.fig.colorbar(im, ax=self.ax)
            cbar.set_label("Temperature (°C)")
            self.colorbar_added = True

        plt.pause(0.1)
        plt.savefig(f"{OUTPUT_DIR}/thermal_map.png", dpi=200)

    def trigger_payout(self, lat, lon, confidence):
        print("\n WILDFIRE CONFIRMED")
        print(f"Location → Lat {lat:.4f}, Lon {lon:.4f}")
        print(f"Confidence → {confidence}%")
        print("Smart Contract: Insurance payout executed (Simulated)")

        dashboard_state.update({
            "fire_detected": True,
            "latitude": f"{lat:.4f}",
            "longitude": f"{lon:.4f}",
            "confidence": f"{confidence}%",
            "payout_status": "Executed"
        })

    def run_simulation(self):
        print(f"\nStarting Mission | Budget ${MISSION_BUDGET_USD}")

        for step in range(10):
            print(f"\n--- Time Step {step} ---")

            sat_lat, sat_lon = self.get_current_location()
            grid = self.capture_thermal_data()
            fires = self.apply_ai_noise_filter(grid)

            self.visualize_thermal_map(grid, step)

            if fires and not self.fire_already_reported:
                confidence = self.calculate_confidence(fires)

                if confidence >= 85:
                    fire_lat, fire_lon = self.compute_fire_location(
                        fires, sat_lat, sat_lon
                    )
                    self.trigger_payout(fire_lat, fire_lon, confidence)
                    self.fire_already_reported = True

            time.sleep(1)

        print("\nSimulation Complete")

# WEB DASHBOARD (FLASK)
app = Flask(__name__)

@app.route("/")
def dashboard():
    return f"""
    <h2> Wildfire Insurance Dashboard</h2>
    <p><b>Fire Detected:</b> {dashboard_state['fire_detected']}</p>
    <p><b>Latitude:</b> {dashboard_state['latitude']}</p>
    <p><b>Longitude:</b> {dashboard_state['longitude']}</p>
    <p><b>Confidence:</b> {dashboard_state['confidence']}</p>
    <p><b>Payout Status:</b> {dashboard_state['payout_status']}</p>
    """

def run_dashboard():
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start dashboard FIRST
    threading.Thread(target=run_dashboard, daemon=True).start()
    time.sleep(1)  # allow server to start

    # Run satellite simulation
    CubeSatDigitalTwin().run_simulation()

