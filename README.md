# 🏎️ F1 Driver Comparison Tool

An interactive Streamlit dashboard to visualize and compare the fastest laps between two Formula 1 drivers using real telemetry data. Built with FastF1, Plotly, and Streamlit, this app displays a broadcast-style map of speed dominance and a speed-over-distance trace. Experince it [here](https://f1-devanalysis.streamlit.app/).

---

## 🔧 Features

- 📊 Speed trace comparison (distance vs. speed)
- 🗺️ Track dominance map (who's faster where)
- 📍 Sector annotations on the map
- 🎛️ Clean interactive UI via Streamlit
- ✅ Filters out future/unavailable sessions
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/0476b9c9-4ba5-439f-8700-ff04c1d6f4c4" />
<img width="1439" alt="image" src="https://github.com/user-attachments/assets/a593e5f7-9069-4f5a-a819-edd8c9b86e05" />



---

## 🚀 How to Run

### 1. Install Python (≥ 3.9)

Use `python --version` to verify.

### 2. Install Dependencies

You can use a virtual environment (recommended):

```bash
pip install fastf1 streamlit plotly matplotlib pandas numpy
```

### 3. Run the App

```bash
streamlit run app.py
```

It'll open your browser at `http://localhost:8501`

---

## 🕹️ How to Use

1. Use the **sidebar** to:
   - Select the year (2019–2025)
   - Pick a Grand Prix and a session type (FP1, FP2, FP3, Q, or R)
   - Choose two drivers from the session
2. View:
   - The **Speed Trace** chart comparing both laps
   - The **Track Dominance Map** showing who was faster at each part of the track
3. Hover over segments for more info

> App will only show completed events with available telemetry data

---

## 🧠 How It Works

- Pulls session data via `FastF1`
- Extracts fastest laps for both drivers
- Interpolates telemetry to a shared distance base
- Calculates speed delta and renders visual dominance
- Displays map with sector markers and interactive labels

---

## 📂 File Overview

```bash
app.py          # Main Streamlit application file
f1_cache/       # Auto-generated FastF1 cache
README.md       # This file
```

---

## 💡 Example Improvements

You can extend this tool with:
- Dark mode toggle
- More telemetry overlays (braking, throttle, gear)
- Corner-by-corner comparison
- Delta time graph (gap over distance)

---

## 📜 License

MIT — free to use, modify, distribute. Just credit original authors if you publish.

---

## 🙏 Credits

- Telemetry via [`FastF1`](https://github.com/theOehrly/Fast-F1)
- Visualization via Plotly + Streamlit
- F1 Data sourced legally from official timing feeds
