ATS Optimizer – Keyword Suggestor

An Applicant Tracking System (ATS) keyword optimization tool that analyzes resumes (PDF) and suggests relevant keywords to improve ATS matching.
The project supports local execution and Windows executable (.exe) packaging for easy distribution.

📌 Features

Extracts text from resume PDFs

Suggests ATS-friendly keywords

Optional integration with multiple LLM providers

OpenAI

Anthropic (Claude)

Google Gemini

Can be packaged as a standalone Windows executable

🛠️ Tech Stack

Python 3.8+

PyPDF2 – PDF text extraction

LLM APIs (Optional)

OpenAI

Anthropic

Google Generative AI

PyInstaller – Executable creation

📂 Project Structure
ATS_Optimizer/
├── ATS_Keyword_Suggestor.py
├── requirements.txt
├── README.md
└── venv/ (optional)

🚀 Running the Project (Step-by-Step)
Step 1: Install Python

Download Python 3.8 or later from:

https://www.python.org/downloads/


⚠️ Important:
During installation, make sure to check “Add Python to PATH”

Verify installation:

python --version

Step 2: Create Project Directory
mkdir ATS_Optimizer
cd ATS_Optimizer

Step 3: Create a Virtual Environment (Recommended)
Windows
python -m venv venv
venv\Scripts\activate

macOS / Linux
python3 -m venv venv
source venv/bin/activate


Why use a virtual environment?

Isolates project dependencies

Prevents conflicts with system Python packages

Makes the project portable and reproducible

Step 4: Install Dependencies

Create a file named requirements.txt:

PyPDF2==3.0.1
openai==1.12.0
anthropic==0.18.1
google-generativeai==0.3.2


Install dependencies:

pip install -r requirements.txt

Dependency Breakdown
Package	Purpose
PyPDF2	PDF text extraction (required)
openai	OpenAI API integration (optional)
anthropic	Claude API integration (optional)
google-generativeai	Gemini API integration (optional)

⚠️ API keys are not included.
Add your own API keys as environment variables or configuration values.

Step 5: Save the Code

Save the application file as:

ATS_Keyword_Suggestor.py

Step 6: Run the Application
python ATS_Keyword_Suggestor.py

📦 Creating a Windows Executable (.exe)
Method 1: PyInstaller (Recommended)
Step 1: Install PyInstaller
pip install pyinstaller

Step 2: Create Executable

Basic Command

pyinstaller --onefile --windowed ATS_Keyword_Suggestor.py


Advanced Command (Recommended)

pyinstaller --onefile ^
            --windowed ^
            --name "ATS_Optimizer" ^
            --icon=app_icon.ico ^
            --add-data "README.txt;." ^
            ATS_Keyword_Suggestor.py

Flags Explained
Flag	Description
--onefile	Packages everything into a single .exe
--windowed	Hides console window (GUI only)
--name	Output executable name
--icon	Custom application icon
--add-data	Include extra files
Step 3: Locate the Executable
cd dist


Your executable will be available as:

ATS_Optimizer.exe

Step 4: Test

Double-click ATS_Optimizer.exe to run the application.

🧯 Common PyInstaller Issues & Fixes
Issue 1: Failed to execute script

Solution:
Build without --onefile to see detailed errors:

pyinstaller --windowed ATS_Keyword_Suggestor.py

Issue 2: Missing Modules

Solution: Add hidden imports:

pyinstaller --onefile ^
            --windowed ^
            --hidden-import=PyPDF2 ^
            --hidden-import=tkinter ^
            ATS_Keyword_Suggestor.py

Issue 3: Large Executable Size

Solution: Use UPX compression:

pip install upx
pyinstaller --onefile --windowed --upx-dir=/path/to/upx ATS_Keyword_Suggestor.py

🧰 Method 2: Auto-py-to-exe (GUI Tool)
Step 1: Install
pip install auto-py-to-exe

Step 2: Launch
auto-py-to-exe

Step 3: Configure

Script Location: ATS_Keyword_Suggestor.py

One File: Enabled

Console Window: Window Based (hide console)

Icon: Optional (.ico file)

Click CONVERT .PY TO .EXE

🔐 Security Notes

Do not hard-code API keys

Use environment variables or config files

Never commit secrets to GitHub

📄 License

This project is for educational and demonstration purposes.
You may adapt or extend it for personal or professional use.
