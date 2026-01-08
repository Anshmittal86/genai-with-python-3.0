# Python Environment Commands

# Check Python version

python --version

# Install a Python package

pip install package_name

# Create virtual environment

python -m venv venv

# Activate virtual environment (Windows)

venv\Scripts\activate

# Activate virtual environment (Linux / Mac)

source venv/bin/activate

# Deactivate virtual environment

deactivate

# Save installed packages to requirements.txt

pip freeze > requirements.txt

# Install packages from requirements.txt

pip install -r requirements.txt

# docker compose

docker compose up -d
