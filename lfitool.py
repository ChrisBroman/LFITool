#!/usr/bin/python3

import requests
import argparse
import random

parser = argparse.ArgumentParser(description="Local File Inclusion Tester")
parser.add_argument("-u", "--url", help="URL", required=True)
parser.add_argument("-p", "--payloads", help="Payload File", required=True)
args = parser.parse_args()

def main():
    with open('useragents.txt', 'r') as file:
        user_agents = [line.strip() for line in file.readlines()]
        
    
    url = args.url
    payload_list = args.payloads

    with open(payload_list, "r") as file:
        lines = file.readlines()

    try:
        error_user_agent = random.choice(user_agents)
        error_header = {'User-Agent': error_user_agent}
        error_request = requests.get(url + "klsenaieovnanksehr", headers=error_header)
        error_size = len(error_request.content)
        print(f"Size of error: {error_size}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return

    threshold = 500

    for line in lines:
        random_user_agent = random.choice(user_agents)
        headers = {'User-Agent': random_user_agent}
        payload = line.strip()
        query = url + payload
        
        try:
            response = requests.get(query, headers=headers)
            if abs(len(response.content) - error_size) > threshold:
                print(f"Possible LFI Payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Error for payload {payload}: {e}")

if __name__ == "__main__":
    main()
