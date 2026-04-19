<h1 align="center">⚡ PyPort — Offline Python Environment Manager ⚡</h1>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00e5ff,100:ff00e5&height=120&section=header&text=PyPort&fontSize=32&fontColor=ffffff&animation=fadeIn"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt"/>
  <img src="https://img.shields.io/badge/Offline-Ready-purple?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge"/>
</p>

---

## 🧠 Overview

PyPort is a powerful GUI-based tool designed to manage Python environments in **offline or air-gapped systems**. It allows seamless transfer of dependencies between online and offline machines, eliminating the need for internet access during installation.

Built with a modern **Neon UI using PyQt6**, PyPort simplifies package management, automation, and deployment workflows for engineers working in restricted environments.

---

## ✨ Features

🚀 **Package Management**

* 📦 Install Python packages (Online & Offline)
* 📋 View installed modules
* 🧹 Clean environment (full reset)

⚙️ **Offline Workflow**

* 📤 Export `requirements.txt`
* 📥 Download packages for offline use
* 📦 Generate complete Offline Kit (ZIP + installer)

🧠 **Smart Operations**

* ⚡ Smart install (only missing packages)
* 🔍 Smart export (only new dependencies)

📊 **User Experience**

* 📊 Real-time progress tracking
* 💻 Terminal-style live logs
* 🎨 Neon-themed modern UI

---

## ⚙️ Requirements

### 💻 Software

* Python 3.12+
* Windows OS (recommended)

### 📦 Libraries

* PyQt6

<p align="center">
  <img src="https://skillicons.dev/icons?i=python"/>
</p>

---

## ⚙️ How It Works

```mermaid
flowchart LR
A[Online PC] --> B[Export Requirements]
B --> C[Download Packages]
C --> D[Transfer via USB]
D --> E[Offline PC]
E --> F[Install Packages]
```

---

## 🔄 Workflow

### 🖥️ Online PC

* Export environment
* Download packages
* Create Offline Kit

### 💻 Offline PC

* Transfer files
* Install via PyPort
* Update environment

---

## 🎯 Use Case

PyPort is ideal for environments where internet access is restricted or unavailable, such as:

* 🔐 Secure labs (DRDO, defense systems)
* 🏢 Enterprise isolated networks
* 🧪 Testing & staging environments

It ensures reliable and controlled Python package deployment without external connectivity.

---

## 👨‍💻 Author

<p align="center">
  <b>Chiranjib Kar</b>
</p>

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff00e5,100:00e5ff&height=100&section=footer"/>
</p>
