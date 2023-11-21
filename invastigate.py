import subprocess
from Wappalyzer import Wappalyzer, WebPage
import shodan
import os
import shutil
import json


def scan_and_save_to_file(url, nmap_file):
    try:
        print(f"{url}\t\t\t{nmap_file}")
        # Run Nmap with the provided URL and save the output to the specified file
        cmd = f'nmap --script nmap-vulners/ -oN {nmap_file} -sV -A -T4 {url} '
        subprocess.run(cmd, shell=True, check=True)
        print(f'Nmap scan for {url} completed and results saved to {nmap_file}')
        return nmap_file
    except subprocess.CalledProcessError:
        print(f'Nmap scan for {url} failed. Please make sure Nmap is installed.')


def check_url_technology(url):
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_url(f'https://{url}')
    return wappalyzer.analyze(webpage)


def get_shodan_info(api_key, target_url):
    api = shodan.Shodan(api_key)

    try:
        # Perform a Shodan search for the target URL
        results = api.search(f"hostname:{target_url}")

        # Print the results
        for result in results['matches']:
            return f"IP: {result['ip_str']}, Port: {result['port']},Banner: {result['data']} "

    except shodan.APIError as e:
        return f"Error: {e}"


def create_url_json(url, nmap, technologies, shodan):
    url_data = {
        "url": url,
        "nmap": nmap,
        "technologies from wappalyzer": technologies,
        "shodan info": shodan
    }
    return url_data

def save_json_file(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=2)


def main(file_path):

    with open(file_path, "r") as file:
        urls = file.read().splitlines()

    # Creating files data
    for url in urls:
        api_key = input("Please enter your API")

        file_name = f'results_{url.replace("://", "_").replace("/", "_")}.json'
        technology = check_url_technology(url)
        technology_list = list(technology)
        technology_info = {"technology": technology_list}
        with open(scan_and_save_to_file(url, file_name), "r") as file:
            nmap = file.read()
        shodan_info = get_shodan_info(api_key, url)
        data = create_url_json(url, nmap, technology_info, shodan_info)
        save_json_file(data, file_name)

        folder_path = r'sites_info'
        os.makedirs(folder_path, exist_ok=True)  # Ensure the directory exists
        output_file = os.path.basename(file_name)
        shutil.move(output_file, folder_path)
        print("JSON files created successfully.")


if __name__ == '__main__':
    input_file = 'output1.txt'
    main(input_file)
