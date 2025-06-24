# II142X_VT2025

This repository contains the implementation for the thesis project:
**"Enabling Cold-Start Recommendation Systems Using LLM-Generated Synthetic Data: Developing a Stock Basket Recommendation System in Data-Sparse Investment Environments"**, conducted at KTH Royal Institute of Technology in collaboration with Zenon AB.

---

## 📖 Overview

This project aims to solve the **cold-start problem** in financial recommendation systems—specifically for stock basket investment platforms with no historical user data. The approach utilizes **Large Language Models (LLMs)** to generate **synthetic user interaction data**, enabling **collaborative filtering** techniques that would otherwise be infeasible in cold-start scenarios.

---

## 🧠 Core Concepts

- **Cold-start problem** in recommender systems
- **Synthetic user data generation** using LLMs
- **Collaborative filtering models**: SVD, KNN, Deep Learning
- **Content-based filtering** using basket financial metadata
- Evaluation using **Precision@K**, **Recall@K**, and **F1@K**

---
## ⚙️ Installation
- Install dependencies using Poetry:
```
poetry install
```
- Activate the virtual environment
```
poetry shell
```
- Set up environment variables:
add LLM API key to **.env** file as:
```
OPENROUTER_API_KEY=
```
---
## 🧪 How to Run the Experiments
- Jupyter Notebook:
```
poetry run jupyter notebook 
```
- Content-Based Filtering:
```
final/content_based_filtering.py
```
- Collaborative Filtering with Synthetic Data:
1. SVD/KNN: `final/KNN + SVD binary label.ipynb`
2. Deep Learning: `final/ DL binary label.ipynb`

---
## 📊 Data
- `data/`: Contains **stock-level** metadata like closing prices, EBITDA, market cap, TRV, etc and **basket** metadata.
- `basket_features.csv`: Cleaned and encoded features used for content-based similarity and synthetic data generation.
- `syntheticData/`: Includes files for generating user profiles and LLM-generated investment behaviors.
---
## 📈 Results
Key finding: Collaborative filtering models trained on synthetic data **outperformed** content-based filtering, with **deep learning models** achieving up to **60%** precision under cold-start conditions.

Metrics used:

Precision@K, Recall@K, F1-Score@K

---
## 🤖 Technologies
- Python 3.10+

- Pandas, NumPy, Matplotlib

- scikit-learn, Surprise

- PyTorch

- Poetry

## 🧑‍🔬 Authors
Alexander Barhado

Siyu Lu

Supervised by:
Chuan Huang, Mitra Ghourchian, Per Hagström, Isabel Ghourchian
Examiner: Ki Won Sung
📍 KTH Royal Institute of Technology / Zenon AB




