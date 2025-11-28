SkySense AQI — Air Quality Estimation from Smartphone Sky Images
Predict PM2.5 / Air Quality Index (AQI) using only a smartphone camera — Model Development Track (Edge AI Global Hackathon)

Project Overview
SkySense AQI is a vision-based regression model that predicts PM2.5 concentration (AQI category) from smartphone images of the sky.

Traditional AQI sensors are expensive, unavailable in many regions, or slow to update.
But the color, scattering, haze density, and clarity of the sky correlate strongly with particulate pollution.

This project builds a high-quality dataset + multiple ML experiments inside Edge Impulse Studio to develop a robust, optimized model suitable for on-device edge inference.

✔ No hardware needed (camera only)
✔ High-impact environmental use-case
✔ Strong dataset and research focus → Perfect for Model Development Track

Table of Contents

Problem Statement

Dataset (Collection + Labeling)

Model Architecture (Regression + Classification)

Experiments & Research

Edge Impulse Implementation

Evaluation & Benchmarking

Folder Structure

Results

Future Work

Credits

1. Problem Statement

Air pollution (especially PM2.5) is a global health hazard.
But AQI stations are limited, costly, and not real-time in many areas.

Goal:
Build a vision-based machine learning model that estimates AQI / PM2.5 using only smartphone sky photos.

Why this matters:

Affordable

Accessible everywhere

Low-power edge deployment

Useful in rural areas, travel, drones, education, and smart city apps

2. Dataset

2.1 Data Sources
A) Custom Smartphone Dataset (Primary)

Collected using Android phone:

10–20 images per day

Different times: morning, afternoon, evening

Different weather: clear, cloudy, hazy

Different angles & brightness

Goal: 300–500 images minimum (higher = better)

B) Public Datasets (Secondary)

Sources used (all open-source/permissive):

Sky haze / pollution datasets

Atmospheric scattering datasets

Cloud/sky image datasets

Urban haze classification datasets

You may include attribution inside /docs/dataset.md.

2.2 Labeling (How AQI is Assigned)

Every sky image is labeled with real PM2.5 value using AQI APIs:

World Air Quality Index (WAQI) API

OpenAQ API

Local government AQI API

PurpleAir (optional)

Store metadata:

Field	Description
Timestamp	When the image was captured
Location	City-level only (to avoid personal data)
PM2.5	Numeric value
AQI Category	“Good”, “Moderate”… based on EPA scale
Weather	(optional) cloud %, humidity

2.3 Data Preprocessing

Resize to 128×128 (or 96×96 for faster model)

Normalize

Remove images with too many buildings/trees

Keep only upper 50–70% of the sky (optional cropping experiment)

3. Model Architecture

Two versions:

3.1 Regression Model (Recommended)

Predict PM2.5 value (continuous number).

Pipeline:

Image Input → 128×128

Image Preprocessing Block

MobileNetV2 / EfficientNet-Lite backbone

Dense Layer → Output = 1 value (PM2.5)

Loss function:

MAE (Mean Absolute Error)

MSE (secondary metric)

3.2 Classification Model

Predict AQI Category:

Good

Moderate

Unhealthy for Sensitive Groups

Unhealthy

Very Unhealthy

Hazardous

Architecture similar but final layer = Softmax(6).

3.3 Custom Hybrid Feature Model (Innovation Bonus)

Add custom DSP features:

Sky hue histogram

Brightness features

Saturation curve

Haze index (brightness gradient)

Then feed into:

Small CNN

Dense layers

Regression head

This can dramatically improve performance.

4. Experiments & Research

Experiment 1 — Backbone Comparison

MobileNetV2

EfficientNet-Lite

Small CNN (baseline)

Measure accuracy, MAE, model size.

Experiment 2 — 96×96 vs 128×128 Input

Analyze improvement vs inference speed.

Experiment 3 — Classification vs Regression

Compare:

Accuracy

Consistency

Interpretability

Experiment 4 — Weather-based Evaluation

Group test set by weather:

Clear

Cloudy

Rainy

Hazy

Analyze generalization.

Experiment 5 — Quantization Effects

Compare:

Float32

Int8 quantized

EON Compiler optimized model

Experiment 6 — Cropped Sky vs Full Image

Analyze how image composition affects performance.

5. Edge Impulse Implementation

Steps:

Create Edge Impulse project

Upload dataset (or use mobile phone to capture images)

Build Image regression pipeline

Adjust preprocessing (resize, normalize)

Train

Tune hyperparameters

Run test set

Export model (TFLite, WASM, C++ SDK)

Document results

6. Evaluation & Benchmarking

Key metrics for regression:

MAE

RMSE

R² score

Scatter plot: Predicted vs Actual

Key metrics for classification:

Confusion matrix

Per-class F1 score

Precision/recall

7. Project Folder Structure
SkySense-AQI/
│
├── data/
│   ├── images/
│   ├── labels.csv
│
├── docs/
│   ├── dataset.md
│   ├── experiments.md
│   ├── architecture.png
│
├── edgeimpulse/
│   ├── exported-models/
│   ├── project-snapshots/
│
├── results/
│   ├── regression/
│   ├── classification/
│
└── README.md

8. Results

You will fill these after training.

Regression Example

MAE: ±7.9 µg/m³

R²: 0.81

Latency: 27ms

Classification Example

Accuracy: 91.3%

F1 Score: 0.90

Model Size

Quantized: ~600 KB

Float: 3.8 MB

9. Future Work

Include humidity / temperature metadata

Use lightweight fusion model (Vision + Weather API)

Night-time sky modeling

Use transformer vision backbone

Train with global multi-city datasets

Build real-time Android inference app

10. Credits

HackerEarth
Edge Impulse Studio
WAQI APIs
Collected data with Android phone
