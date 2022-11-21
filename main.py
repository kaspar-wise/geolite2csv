from secrets import LICENSE_KEY
import zipfile
import requests
import io

API_URL = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country-CSV&license_key={LICENSE_KEY}&suffix=zip"
COUNTRIES_FILE_NAME = "GeoLite2-Country-Locations-en.csv"
IPV4_FILE_NAME = "GeoLite2-Country-Blocks-IPv4.csv"
IPV6_FILE_NAME = "GeoLite2-Country-Blocks-IPv6.csv"


def get_data_from_api():
  res = requests.get(API_URL, stream=True)
  return res


def unzip(file):
  with zipfile.ZipFile(file, 'r') as zip:
    return {name.split("/")[-1]: zip.read(name) for name in zip.namelist()}


def save_file(file_path, content):
  with open(file_path, "w+") as file:
    file.write(content)


if __name__ == '__main__':
  zip_content = unzip(io.BytesIO(get_data_from_api().content))
  save_file("db/ipv4.csv", zip_content[IPV4_FILE_NAME].decode('utf-8'))
