from requests.models import HTTPError
from beautifultable import BeautifulTable
import math, sys, requests, htmllistparse

def conv(byte):
  if byte == 0:
      return "0B"
  suff = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
  i = int(math.floor(math.log(byte, 1024)))
  p = math.pow(1024, i)
  s = round(byte / p, 2)
  return "%s %s" % (s, suff[i])

def download(pkg):
  url = "https://archive.archlinux.org/packages/" + pkg[0] + "/" + pkg
  table = BeautifulTable()
  try:
    _, lst = htmllistparse.fetch_listing(url, timeout=30)
    filtered = list(filter(lambda q: not q.name.endswith(".sig"), lst))
    limit = 0
    for file in filtered:
      limit += 1
      table.rows.append([limit, file.name, conv(file.size)])
    table.columns.header = ["index", "file", "size"]
    print(table)
    index = 0
    while index == 0:
      temp = input("Select an index > ").strip()
      if not temp.isdigit():
        print("Invalid input.")
      elif int(temp) > limit or int(temp) <= 0:
        print("Index must not exceed the limit or below zero.")
      else:
        index = int(temp)
    target = filtered[index - 1]
    r = requests.get(url + "/" + target.name)
    with open(target.name, 'wb') as f:
      f.write(r.content)
      print("Downloaded " + target.name + " to current working dir.")
  except HTTPError as err:
    print(err)

if __name__ == "__main__" and len(sys.argv) == 2:
  download(sys.argv[1])
