# 🚀 LaunchDarkly Integration for Flask-based SaaS

This project demonstrates how to implement feature flags using **LaunchDarkly** in a **Flask-based SaaS application**. It enables **instant rollbacks**, **targeted feature releases**, and **A/B testing**

## 🚀 Getting Started

Follow the instructions below to set up the project and run it locally.

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Flask**
- **LaunchDarkly Account** – [Sign up here](https://launchdarkly.com)
- **Git & GitHub CLI**

### Setup & Installation

#### 1. Clone the Repository

Start by cloning the repository:

```bash
git clone https://github.com/celinasilva99/launchdarkly.git
cd launchdarkly
```

#### 2. Create a Virtual Environment

Create a virtual environment to manage your dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

Install all the required dependencies:

```bash
pip install -r requirements.txt
```

#### 4. Configure LaunchDarkly Keys

Create a `.env` file in the root of your project and add the following details (you can find this information in your LaunchDarkly account):

```bash
LD_SDK_KEY = Your SDK Key
FEATURE_FLAG_KEY = Your Feature Flag Key
LD_API_KEY = Your API Key
PROJECT_KEY = Your Project Key
ENVIRONMENT_KEY = Your Environment Key
```

### 🚀 Running the Application

You can run the Flask application by executing the following commands for the specific tasks:

#### Task 1: Release and Remediate

```bash
python release_and_remediate.py
```

#### Task 2 & 3: Targeted Releases and Optimisation (Metrics/Experiments) 

```bash
python target.py
```

Once the application is running, open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Toggle Feature Flags

You can toggle feature flags in the LaunchDarkly dashboard, and see live updates on your local Flask application.


### 📊 Measuring Experiment Performance

1. To measure the impact of an experiment in LaunchDarkly:

2. Create a Metric – Define what you want to track (e.g., button clicks, page views, conversions).

3. Set Up an Experiment – Link the metric to a feature flag and configure an A/B test.

Run and Analyze – Launch the experiment and review data in LaunchDarkly to make data-driven decisions.


# LaunchDarkly Code References Integration

## Overview
This repository integrates **GitHub Actions** with **LaunchDarkly Code References** to track feature flag usage within the codebase. This setup improves visibility, maintainability, and traceability of feature flags in your application.

## Prerequisites

1. **LaunchDarkly Account:** Ensure you have an active LaunchDarkly account with API access.
2. **GitHub Repository:** The repository should have necessary permissions to execute workflows.
3. **Install `ld-find-code-refs`:** Ensure `ld-find-code-refs` is installed or included in your workflow.

## Step-by-Step Setup Guide

### 1. Configure GitHub Actions Workflow

1. Open your GitHub repository.
2. Navigate to the `.github/workflows/` directory. If it doesn’t exist, create it.
3. Create a new file named `launchdarkly.yml`.
4. Copy and paste the following configuration:

```yaml
name: LaunchDarkly Code References

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  update-code-references:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Run LaunchDarkly Code References
        uses: launchdarkly/find-code-references-action@v2
        with:
          accessToken: ${{ secrets.LD_ACCESS_TOKEN }}
          projKey: "your-project-key"
          repoName: "your-repo-name"
```

5. Save and commit the file.

### 2. Set Up Secret Keys in GitHub

1. Open your GitHub repository.
2. Click on the **Settings** tab at the top of the repository.
3. In the left sidebar, go to **Secrets and variables > Actions**.
4. Click on **New repository secret**.
5. Add the following secrets one by one:
   - **`LD_ACCESS_TOKEN`**: Your LaunchDarkly **personal access token**.
   - **`projKey`**: The LaunchDarkly **project key** where your feature flags reside.
   - **`repoName`**: The name of your **GitHub repository** to track code references.
6. Click **Add secret** after entering each value.
7. Ensure all secrets are listed in **Actions > Secrets**.

### 3. Ensure Your Codebase Contains Your Feature Flag Keys

All keys are stored in .env, but this is not detected by ld-find-code-refs. To work around this, I created **test_integration.py** with feature flag keys hardcoded to ensure they are detected.

### 4. Verify in LaunchDarkly 

1. Log in to your **LaunchDarkly** account.
2. Navigate to **Feature Flags**.
3. Select the feature flag you want to track.
4. Click on the **Code References** tab.
5. Choose your **repository and branch**.
6. You should now see all code references related to that feature flag.

## Troubleshooting

- **Authentication Issues:** Ensure the `LD_ACCESS_TOKEN` is set correctly in GitHub Secrets.
- **No Code References Found:** Make sure your repository follows standard feature flag naming conventions.
- **Workflow Failing:** Check the GitHub Actions logs for detailed error messages.

## References

- [LaunchDarkly Code References](https://docs.launchdarkly.com/home/code/code-references)
- [GitHub Actions](https://docs.github.com/en/actions)

  
**LaunchDarkly Documentation**: [Link to docs](https://docs.launchdarkly.com)
-**Flask Documentation**: [Link to docs](https://flask.palletsprojects.com/)

---

### Contributors

- **Celina** - Initial implementation

For questions or issues, please create a GitHub issue in this repository.






