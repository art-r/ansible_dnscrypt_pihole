import requests

response = requests.get("https://api.github.com/repos/dnscrypt/dnscrypt-proxy/releases/latest")
assets = response.json()['assets']

urlBinary = ""

for asset in assets:
    if "dnscrypt-proxy-linux_x86_64" in asset['name']:
        binaryName = asset['name']
        urlBinary = asset['browser_download_url']
        break

if urlBinary != "":
    binary = requests.get(urlBinary)
    open(binaryName, "wb").write(binary.content)
    