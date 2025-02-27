# 🚀 LaunchDarkly

This project demonstrates how to implement feature flags using **LaunchDarkly** in a **Flask-based SaaS application**. It enables **instant rollbacks**, **targeted feature releases**, and **A/B testing** to safely deploy new features.

## ✨ Features
- 🔹 **Feature Flag Management** – Control feature rollouts dynamically.
- 🔹 **Instant Rollback** – Disable features without redeploying.
- 🔹 **Targeted Releases** – Deliver features to specific users.
- 🔹 **A/B Testing** – Measure feature impact using LaunchDarkly metrics.

  ## 🚀 Getting Started

### **1️⃣ Prerequisites**
Ensure you have the following installed:
- **Python 3.8+**
- **Flask**
- **LaunchDarkly Account** (Create one at [LaunchDarkly](https://launchdarkly.com))
- **Git & GitHub CLI**

### **2️⃣ Setup & Installation**
#### **Clone the Repository**
bash - 
git clone https://github.com/celinasilva99/launchdarkly.git
cd launchdarkly 

### ** Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### ** Install Dependencies

pip install -r requirements.txt

### ** Create a .env file for local testing

LD_SDK_KEY = Your SDK Key
FEATURE_FLAG_KEY = Your Feature Flag key
LD_API_KEY = Your API key
PROJECT_KEY = Your Project Key
ENVIRONMENT_KEY = Your Environment Key

🚀 Running the Application

Run Flask Locally

python app.py
Open http://127.0.0.1:5000/ in your browser.
Toggle feature flags in LaunchDarkly and see live updates.


