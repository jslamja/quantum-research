````markdown
# Project Setup & Usage Guide

Overview
This document explains how to set up the environment and run the application on your local machine.

---

## 1. Open the Project

1. Clone or download the repository.
2. Open the **main project folder** using a code editor (e.g., VS Code).

---

## 2. Ensure Python is Installed

Check that Python is installed:

```bash
python --version
````

If Python is not installed, download it from:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

---

## 3. Create a Virtual Environment

Inside the main project folder, run:

```bash
python -m venv .venv
```

### Activate the Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

---

## 4. Install Required Libraries

After activating the virtual environment, install dependencies:

```bash
python -m pip install numpy matplotlib
```

---

## 5. Run the Application

Open the file:

```
app.py
```

Then run:

```bash
python app.py
```

The main interface of the application will appear.

---

## 6. Using the Interface

* You can create new folders directly from the interface.
* Inside each folder, you can create new files.
* To ensure a file appears inside the application, it must have one of the following extensions:

  * `.py`
  * `.pdf`

---

## Important Notes

* Always activate the virtual environment before running the application.
* If errors occur, make sure all required libraries are installed correctly.
* If you encounter bugs or issues, open an Issue in the repository.

```
```
