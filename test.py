import urllib.request

try:
    urllib.request.urlopen("https://www.google.com", timeout=5)
    print("Internet is available")
except:
    print("No internet access")
