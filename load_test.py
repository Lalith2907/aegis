import requests
import threading
import time
import random

URL = "http://aegis-alb-1122660298.ap-southeast-2.elb.amazonaws.com/api"
TOTAL_REQUESTS = 50
CONCURRENCY = 20

def hit_request(i):
    priority = random.choice(["HIGH", "LOW"])

    try:
        response = requests.get(
            f"http://aegis-alb-1122660298.ap-southeast-2.elb.amazonaws.com/api?priority={priority}"
        )
        print(f"Request {i} ({priority}): {response.status_code}")
    except Exception as e:
        print(f"Request {i}: ERROR - {e}")

def run_load_test():
    threads = []
    start_time = time.time()

    for i in range(TOTAL_REQUESTS):
        t = threading.Thread(target=hit_request, args=(i, ))
        threads.append(t)

    for i in range(0, TOTAL_REQUESTS, CONCURRENCY):
        batch = threads[i:i + CONCURRENCY]
        for t in batch:
            t.start()
        for t in batch:
            t.join()

    end_time = time.time()
    print(f"\nTotal time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    run_load_test()