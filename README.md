# 🌿 Graph Leaf Disease Detector

An intelligent system to detect diseases in graph leaves using a Convolutional Neural Network (CNN). This project includes a **React + TypeScript frontend** and a **Flask + TensorFlow backend**. It also smartly rejects irrelevant images like bikes, buses, or any non-leaf photos during testing.

---

## 📌 Features

- ✅ **Graph leaf disease classification** using trained CNN model
- ❌ **Rejects irrelevant images** (e.g., vehicles, random objects)
- 🧠 Built with **TensorFlow (CNN)** for accuracy
- ⚛️ Interactive **ReactJS + TypeScript UI**
- 🌐 API integration using **Flask backend**
- 🎯 Real-time prediction system with image preview and result display

---

## 📸 Sample Use-Cases

| Input Image         | Prediction Result            |
|---------------------|------------------------------|
| `graph_leaf.jpg`    | ✅ Detected: "Powdery Mildew" |
| `bus.png`           | ❌ Error: "Not a graph leaf"  |
| `random_object.jpg` | ❌ Error: "Not a graph leaf"  |

---

## 🚀 Getting Started

### 🧾 Prerequisites

- React.js (for frontend)
- Typescript 
- Python 3.7+ (for backend)
- pip (Python package manager)
- TensorFlow, Flask

---

### 🔧 Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py

---

