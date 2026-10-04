# 🔎 VerifyLens AI

### See the evidence. Understand the uncertainty. Keep humans in control.

VerifyLens AI is an AI-assisted visual verification and human review assistant built with **Streamlit** and **Google Gemini Vision**.

It helps users analyze images of physical objects or situations such as damaged packages, equipment issues, vehicles, inventory, and facility observations.

Instead of presenting uncertain AI guesses as facts, VerifyLens separates:

- 👁️ **Visible Observations** — what can actually be seen
- 💭 **Possible Interpretation** — what those observations may indicate
- 📌 **Evidence** — visual details supporting the interpretation
- ❓ **Unknown / Cannot Determine** — information that cannot be reliably established
- ⚠️ **Severity** — Low, Medium, High, or Unable to determine
- ➡️ **Recommended Next Step** — a practical follow-up action
- 👤 **Human Review Required** — whether human inspection is recommended

The final review can be sent as an email report through Gmail.

---

## ✨ Features

- 📷 AI-powered image analysis using Google Gemini
- 💬 Conversational follow-up questions about uploaded evidence
- 🔍 Evidence-based visual verification
- 🧠 Explicit uncertainty handling
- 👤 Human-in-the-loop decision support
- 📧 Email review reports through Gmail SMTP
- 🔄 Start a new visual review without restarting the app
- 🔐 API credentials stored securely using Streamlit Secrets
- ☁️ Ready for deployment on Streamlit Community Cloud

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Google Gemini**
- **Google GenAI SDK**
- **Gmail SMTP**
- **GitHub**
- **Streamlit Community Cloud**

---

## 📁 Project Structure

```text
VerifyLens-AI/
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml.example```
The real .streamlit/secrets.toml file is intentionally excluded from Git.

---

**## 🚀 Run Locally**
1. Clone the repository
git clone https://github.com/manav122005/VerifyLens-AI.git
cd VerifyLens-AI
2. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure secrets

Create:

.streamlit/secrets.toml

Add:

GEMINI_API_KEY = "your_gemini_api_key"

GMAIL_ADDRESS = "your_email@gmail.com"

GMAIL_APP_PASSWORD = "your_16_character_gmail_app_password"

For Gmail, use a Google App Password rather than your normal Gmail password.

Never commit the real secrets.toml file.

5. Start the application
streamlit run app.py

The application will open in your browser.

---

**## ☁️ Streamlit Community Cloud**

The application can be deployed directly from the GitHub repository using Streamlit Community Cloud.

After deployment, configure the following secrets in the Streamlit app settings:

GEMINI_API_KEY = "your_gemini_api_key"
GMAIL_ADDRESS = "your_email@gmail.com"
GMAIL_APP_PASSWORD = "your_16_character_gmail_app_password"

---

**## 🔐 Responsible AI**

VerifyLens is designed as a decision-support tool, not an autonomous decision maker.

The system:

Does not claim to physically inspect objects.
Does not invent measurements, serial numbers, labels, damage, causes, or documentation.
Distinguishes observations from interpretations.
Explicitly identifies information that cannot be determined.
Recommends human review when evidence is insufficient.
Does not make final safety, legal, financial, medical, or compliance decisions.

Human judgment remains responsible for the final decision.

---

**## 🎯 Example Use Cases**

VerifyLens can assist with preliminary visual review of:

📦 Damaged packages
🚗 Vehicle condition
🔧 Equipment observations
📋 Inventory verification
🏢 Facility observations
🧰 Physical asset review

The system should be used as an initial evidence-review assistant rather than a replacement for qualified inspection.

---

**## 👨‍💻 Project**

VerifyLens AI

See the evidence. Understand the uncertainty. Keep humans in control.