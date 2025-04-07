import csv
import subprocess
import time

def send_urls_via_curl(csv_file, max_requests):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        sent_count = 0
        
        for row in reader:
            if sent_count >= max_requests:
                break  
            
            url = row['URL']
            
            
            curl_command = [
                'curl',
                '-x', '10.0.2.15:8080',
                '-X', 'POST',
                '-H', 'Content-Type: application/json',
                '-d', f'{url}',
                'https://10.0.2.15:8000'  
            ]
            
            
            subprocess.run(curl_command)
            print(f"Sent URL #{sent_count + 1}: {url}")
            sent_count += 1
            time.sleep(0.1)

if __name__ == "__main__":
    send_urls_via_curl('test_data.csv', max_requests=600)