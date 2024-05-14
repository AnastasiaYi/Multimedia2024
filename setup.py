import subprocess

def install_packages():
    print("Setting up Python environment...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("Environment setup complete.")

if __name__ == "__main__":
    install_packages()