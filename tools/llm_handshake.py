import requests
import json
import sys

def check_ollama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen3:4b",
        "prompt": "Hello",
        "stream": True
    }
    
    print(f"Testing connection to {url} (Streaming)...")
    
    try:
        with requests.post(url, json=payload, stream=True, timeout=30) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        print(f"[OK] Connection Successful! Received chunk: {data['response']}")
                        return True
                    if data.get("done") is True:
                        break
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"[!] HTTP Error: {e}")
        print(f"Server Response: {response.text}")
        return False
    except requests.exceptions.ConnectionError:
        print("[!] Error: Could not connect to Ollama. Is it running on port 11434?")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[!] Error during request: {e}")
        return False

if __name__ == "__main__":
    success = check_ollama()
    if not success:
        sys.exit(1)
