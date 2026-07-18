import requests

def check():
    url = "https://vighgvgxeqmpzossxxjr.supabase.co"
    try:
        r = requests.get(url)
        print(f"Status Code: {r.status_code}")
        print(f"Headers: {r.headers}")
        print(f"Body: {r.text[:300]}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    check()
