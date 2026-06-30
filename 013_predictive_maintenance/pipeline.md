# Manufacturing: Predictive Maintenance & Failure Detection
## Metadata
| Field | Value |
|---|---|
| **Pipeline ID** | `predictive_maintenance` |
| **Domain** | Manufacturing / Industry 4.0 |
| **Steps** | 15 |
| **Type** | ML Pipeline (End-to-End) |

## Executive Summary
Predicts machine failures before they occur using IoT sensor data (temperature, vibration, pressure, RPM). Enables condition-based maintenance scheduling to minimize downtime.

## Business Context
Unplanned downtime costs manufacturers $50B+ annually. Emergency repairs are 3-9x more expensive than planned maintenance. ML-driven predictive maintenance reduces downtime by 30-50%, extends machine life by 20-40%, and cuts maintenance costs by 25-35%. For a factory with 500 machines, this saves $5-15M/year.

## Steps
### Step 1: Data Loading & Profiling
Load sensor readings CSV. Profile: reading distribution per machine, timestamp range, failure rate. Check for sensor gaps, anomalous readings. Visualize raw sensor trends.

### Step 2: Data Cleaning & Standardization
Handle missing sensor values with forward-fill then interpolation. Remove readings with impossible values (negative RPM, temperature > 500°C). Align timestamps to regular intervals. Flag sensor malfunction periods.

### Step 3: Feature Engineering: Time Domain
Create rolling window features (1h, 6h, 24h): mean, std, min, max, skew, kurtosis for each sensor. Create rate-of-change features. Compute sensor correlations. Create moving average convergence divergence (MACD).

### Step 4: Feature Engineering: Frequency Domain
Apply FFT to vibration signals. Extract dominant frequencies and amplitudes. Compute spectral entropy and power spectral density. Create frequency band energy ratios. These capture subtle patterns invisible in time domain.

### Step 5: Exploratory Data Analysis
Analyze failure distribution by machine, time of day, day of week. Compare sensor distributions for normal vs pre-failure periods. Identify which sensors are most predictive of failures.

### Step 6: Data Visualization: Sensor Health
Create dashboard: (1) Multi-sensor time series with failure markers, (2) Sensor correlation matrix heatmap, (3) Vibration spectrogram for failing machine, (4) Temperature vs pressure scatter colored by failure, (5) Failure count by machine bar chart, (6) RPM distribution by machine boxplot.

### Step 7: Data Visualization: Failure Patterns
Visualize: (1) Hours-to-failure histogram, (2) Feature importance from preliminary model, (3) PCA of sensor readings colored by failure proximity, (4) Remaining useful life degradation curves, (5) Sensor drift detection charts.

### Step 8: Statistical Analysis
Compute sensor baselines. Statistical process control: detect out-of-control conditions. Granger causality test: which sensors lead others. Change point detection for regime shifts. AD/Friedman tests for stationarity.

### Step 9: Data Preparation for Modeling
Create temporal train/test split (no future leakage). Define failure window (predict failure within N hours). Balance classes with time-aware sampling. Scale features per machine. Create sequence windows for deep learning.

### Step 10: Model Training: Classical ML
Train RandomForest and XGBoost classifiers. Use time series cross-validation. Optimize for precision (minimize false alarms) and recall (catch real failures). Feature importance analysis. Save best model.

### Step 11: Model Training: Deep Learning
Build LSTM sequence model (lookback=100 readings). Architecture: 2 LSTM layers (128, 64) + Dropout(0.3) + Dense(32) + Dense(1). Train with class weighting and early stopping. Compare with 1D-CNN approach.

### Step 12: Remaining Useful Life (RUL) Prediction
Train regression model to predict hours until failure. Use XGBoost and RandomForest regressors. Evaluate with RMSE and R². Create RUL degradation curves per machine. Set warning thresholds at 48h, 24h, 4h.

### Step 13: Model Evaluation & Alert System
Compare all models: precision, recall, F1, false alarm rate, detection lead time. Build alert logic: combine classifier probability with RUL estimate. Define alert severity levels. Simulate alert performance on test period.

### Step 14: Cost-Benefit Analysis
Calculate expected savings: (reduced downtime hours × hourly production value) + (reduced emergency repairs × premium cost) - (false alarm investigations × investigation cost). Optimize alert threshold for maximum net savings.

### Step 15: Final Synthesis & Maintenance Playbook
Compile: Model Performance Summary, Per-Machine Failure Predictors, Optimal Maintenance Scheduling Recommendations, Alert System Specification, Expected ROI Analysis, Integration Plan with CMMS/ERP, Operator Dashboard Design, Model Retraining Cadence (monthly).

