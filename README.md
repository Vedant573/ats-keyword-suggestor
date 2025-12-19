# 🚀 ATS Optimizer – Keyword Suggestor

An **Applicant Tracking System (ATS) keyword optimization tool** that analyzes resume PDFs and suggests relevant keywords to improve ATS matching scores.

This project supports:
- Local execution using Python  
- Packaging into a **Windows executable (.exe)** for easy distribution  

---

## 📌 Features

- 📄 Extracts text from resume PDFs  
- 🔍 Suggests ATS-friendly keywords  
- 🤖 Optional AI integrations:
  - OpenAI
  - Anthropic (Claude)
  - Google Gemini
- 📦 Can be packaged as a standalone `.exe`

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **PyPDF2** – PDF text extraction
- **LLM APIs (Optional)**
  - OpenAI
  - Anthropic
  - Google Generative AI
- **PyInstaller** – Executable creation

---

## 📂 Project Structure
```bash
ats-keyword-suggestor/
├── ATS_Keyword_Suggestor.py
├── requirements.txt
├── README.md
└── venv/ (optional)
```

---

## 🚀 Running the Project (Step-by-Step)

---

### **Step 1: Install Python**

Download **Python 3.8 or later** from:

🔗 https://www.python.org/downloads/

⚠️ **IMPORTANT:**  
Check **“Add Python to PATH”** during installation.

Verify installation:

```bash
python --version
```

### **Step 2: Create Project Directory**
```bash
mkdir ATS_Optimizer
cd ATS_Optimizer
```

### **Step 3: Create a Virtual Environment (Recommended)**
For windows:
```bash 
python -m venv venv
venv\Scripts\activate
```
for macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 4: Install Dependencies**

Create a file named requirements.txt: (or if you have cloned this repository, install the dependency via command in the next section)
```bash
PyPDF2==3.0.1
openai==1.12.0
anthropic==0.18.1
google-generativeai==0.3.2
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## **⚠️ API keys are not included.**
Add your own API keys as environment variables or configuration values.


## **Step 6: Run the Application**
```bash
python ATS_Keyword_Suggestor.py
```

## **📦 Creating a Windows Executable (.exe)**
Method 1: PyInstaller (Recommended)
Step 1: Install PyInstaller
pip install pyinstaller

Step 2: Create Executable

Basic Command
```bash
pyinstaller --onefile --windowed ATS_Keyword_Suggestor.py
```

**Advanced Command (Recommended)**
```bash
pyinstaller --onefile ^
            --windowed ^
            --name "ATS_Optimizer" ^
            --icon=app_icon.ico ^
            --add-data "README.txt;." ^
            ATS_Keyword_Suggestor.py
```

## **Step 3: Locate the Executable**
cd dist


Your executable will be available as:
```bash
ATS_Optimizer.exe
```
## **Step 4: Test**

Double-click ATS_Optimizer.exe to run the application.

## **🧯 Common PyInstaller Issues & Fixes**
**Issue 1: Failed to execute script**

Solution:
Build without --onefile to see detailed errors:
```bash
pyinstaller --windowed ATS_Keyword_Suggestor.py
```
**Issue 2: Missing Modules**

Solution: Add hidden imports:
```bash
pyinstaller --onefile ^
            --windowed ^
            --hidden-import=PyPDF2 ^
            --hidden-import=tkinter ^
            ATS_Keyword_Suggestor.py
```
**Issue 3: Large Executable Size**

Solution: Use UPX compression:
```bash
pip install upx
pyinstaller --onefile --windowed --upx-dir=/path/to/upx ATS_Keyword_Suggestor.py
```
## **🧰 Method 2: Auto-py-to-exe (GUI Tool)**
**Step 1: Install**
```bash
pip install auto-py-to-exe
```
**Step 2: Launch**
```bash
auto-py-to-exe
```
**Step 3: Configure**

Script Location: ATS_Keyword_Suggestor.py
One File: Enabled
Console Window: Window Based (hide console)
Icon: Optional (.ico file)
Click CONVERT .PY TO .EXE

## **🔐 Security Notes**

Do not hard-code API keys
Use environment variables or config files
Never commit secrets to GitHub

## **📄 License**

This project is for educational and demonstration purposes.
You may adapt or extend it for personal or professional use.
