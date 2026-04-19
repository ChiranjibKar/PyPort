<h1 align="center">⚡ Telemetry Frame Range Investigator ⚡</h1>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00f5ff,100:7c3cff&height=120&section=header&text=Telemetry%20Analyzer&fontSize=30&fontColor=ffffff&animation=fadeIn"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-Custom%20No--Modification-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt"/>
  <img src="https://img.shields.io/badge/Telemetry-Engineering-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

---

> 🚫 Modification of this source code is strictly prohibited.

---

## 🧠 Overview

This application is a powerful Python-based GUI tool designed for extracting, analyzing, and validating telemetry frame data from structured documents such as PDF, DOCX, and TXT files. It intelligently parses frame numbers and associated word sequences, applies configurable offsets, and detects irregularities in data ordering.

Built with a visually enhanced Neon Circuit interface using PyQt6, the tool provides an intuitive and efficient environment for engineers to inspect complex telemetry mappings. With support for visualization and structured export, it bridges the gap between raw telemetry logs and actionable engineering insights.

---

## ✨ Features

🚀 **Smart Data Extraction**

* 📂 Load PDF, DOCX, and TXT files
* 🔍 Automatic frame & word parsing

⚙️ **Data Processing**

* 🔧 Adjustable frame and word offsets
* ⚠️ Irregular sequence detection

📊 **Visualization**

* 📊 Interactive frame visualizer
* 📈 Frame distribution chart

📁 **Export & Reporting**

* 🧾 Generate detailed reports
* 📤 Export structured CSV files

---

## ⚙️ Requirements

### 💻 Software

* Visual Studio Code
* Python 3.13.12

### 📦 Libraries

* PyQt6
* PyMuPDF (fitz)
* python-docx

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,vscode"/>
</p>

---

## ⚙️ How It Works

```mermaid
flowchart LR
A[Load File] --> B[Extract Frames]
B --> C[Apply Offsets]
C --> D[Validate Data]
D --> E[Visualize]
E --> F[Export Report/CSV]
```

---

## 🎯 Use Case

This tool is ideal for telemetry engineers and developers who need to validate frame-word mappings, detect missing or inconsistent values, and generate structured datasets for further processing. It is particularly useful in environments where data integrity and precise mapping are critical, such as aerospace, defense, and embedded systems.

---

## 👨‍💻 Author

<p align="center">
  <b>Chiranjib Kar</b><br>
  Co-Developer: Biswajit Das  
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3cff,100:00f5ff&height=100&section=footer"/>
</p>

## 📜 License & Usage

This project is licensed under a **Custom Source-Available License**.

### ✅ You are allowed to:
- Use the software for personal or commercial purposes
- Run and distribute the software in its original form

### ❌ You are NOT allowed to:
- Modify, alter, or create derivative works from the source code
- Redistribute modified versions of this software
- Rebrand or sell this software as your own

### ⚠️ Note:
This is **not an open-source license**. The source code is provided for transparency and usage, but not for modification.

For full terms, see the [LICENSE](./License) file.
