# HyperAutomata Simulator

The **HyperAutomata Simulator** is a Python-based tool designed for simulating asynchronous hyperautomata. The project provides a user-friendly graphical interface to define automata, simulate their behavior, and analyze their properties. It integrates backend logic, a GUI built with `tkinter`, and a database for saving and loading simulation data.
Made by Raz Kessel & Nevo Gottlieb
---

## **Project Overview**

### Features:
- Define automata with customizable states and transitions.
- Simulate asynchronous hyperautomata with interactive controls.
- Save and load automata and simulation history using a database.
- Visualize automata and transitions dynamically.

### Technologies Used:
- **Backend**: Python (with SQLAlchemy for database integration).
- **GUI**: Tkinter.
- **Database**: SQLite.
- **Graphics**: Pillow for icon and image processing.

---

## **Branch Structure**

The repository is divided into two main branches:

### **1. `master` Branch**
- **Contents**:
  - Complete project source code.
  - Backend logic for automata simulation.
  - GUI implementation.
  - Test scripts.
  - Required assets and configuration files.
- **Purpose**:
  - To host the complete implementation of the simulator.
  - Provides the operational environment for running the application.

### **2. `main` Branch**
- **Contents**:
  - Theoretical documentation:
    - Project books.
    - Poster for Phase B and Slides presentation for Phase A, summarizing the project.
  - A demo video showcasing the simulator in action.
- **Purpose**:
  - To provide theoretical and supporting materials for understanding the project.
  - For academic or presentation purposes.

---

## **Getting Started**

### Prerequisites:
- Python 3.9 or higher.
- Required libraries (install using `pip`):
  ```bash
  pip install -r requirements.txt
  ```

### Running the Application:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name/hyperautomata-simulator.git
   ```
2. Switch to the `master` branch:
   ```bash
   git checkout master
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Viewing Documentation and Demo:
1. Switch to the `main` branch:
   ```bash
   git checkout main
   ```
2. Explore the following files:
   - **Project Book Phase A**: `Capstone Project Phase A- 24-2-R-20.pdf`
   - **Project Book Phase B**: `Capstone Project Phase B- 24-2-R-20.pdf`
   - **Presentation slides Phase A**: `Capstone Project Phase A- 24-2-R-20.pptx`
   - **Poster Phase B**: `poster.pdf`
   - **Demo Video**: `demo.mp4`

---

## **Folder Structure (Master Branch)**

```
├── assets/                 # Icons and images used in the GUI
├── backend/                # Core logic for automata and simulation
├── components/             # GUI components and managers
├── tests/                  # Unit tests for validating functionality
├── automata.db             # SQLite database file
├── main.py                 # Entry point of the application
├── requirements.txt        # Python dependencies
```

---


Enjoy exploring the world of asynchronous hyperautomata with our simulator!
