import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Function to create the "etc" folder if it doesn't exist
def create_etc_folder():
    if not os.path.exists("etc"):
        os.makedirs("etc")
        print("Created 'etc' folder.")
    else:
        print("'etc' folder already exists.")

# Function to create or update the config.ini file with default values
def create_or_update_config_ini():
    config_path = "etc/config.ini"
    if not os.path.exists(config_path):
        with open(config_path, "w") as config_file:
            config_file.write("""[DEFAULT]
max_ms = 3000
host = https://google.com
thread = 30
export = latency.txt
import = proxies.txt
""")
        print("Created 'config.ini' with default values.")
    else:
        print("'config.ini' already exists.")

# Function to create or update the README.md file with instructions
def create_or_update_readme():
    readme_path = "etc/README.md"
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as readme_file:
            readme_file.write("Proxies.txt syntax: regular [IP]:[PORT]")
        print("Created 'README.md' with instructions.")
    else:
        print("'README.md' already exists.")

# Function to create proxies.txt if it doesn't exist
def create_proxies_txt():
    proxies_path = "etc/proxies.txt"
    if not os.path.exists(proxies_path):
        with open(proxies_path, "w"):
            pass
        print("Created 'proxies.txt'.")
        print("----------------------")
        input("Navigate to [currentfolder]/etc/proxies.txt, and add all proxy servers to be tested.")
    else:
        
        print("'proxies.txt' already exists.")
        input("Press any key to begin latency test...")

# Function to check the latency of a single proxy
def check_latency(proxy):
    try:
        cmd = f"ping -c 5 {proxy}"
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        min_latency = float("inf")
        for line in output.split("\n"):
            if "time=" in line:
                latency = float(line.split("time=")[1].split(" ms")[0])
                min_latency = min(min_latency, latency)
        with open(os.path.join("etc", "latency.txt"), "a") as f:
            f.write(f"{proxy}: {min_latency} ms\n")
        print(f"Measured latency for {proxy}: {min_latency} ms")
    except Exception as e:
        print(f"Error measuring latency for {proxy}: {e}")

# Main function to execute all setup tasks
def main():
    create_etc_folder()
    create_or_update_config_ini()
    create_or_update_readme()
    create_proxies_txt()

    # Perform latency measurements
    with open("etc/proxies.txt", "r") as f:
        proxies = f.read().splitlines()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for proxy in proxies:
            executor.submit(check_latency, proxy)

if __name__ == "__main__":
    main()
