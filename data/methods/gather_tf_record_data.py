from bs4 import BeautifulSoup
import requests
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from urllib.request import urlopen
import os

data_type = "test"  # train, test, validate
part = "video"  # video, frame, segment

r = requests.get(
    f"http://storage.googleapis.com/us.data.yt8m.org/2/{part}/{data_type}/index.html")
data = r.text
soup = BeautifulSoup(data)
for link in soup.find_all('a'):
    tf_record_full_name = link.get('href')
    tf_record_name = tf_record_full_name.split(".")[0]
    if not os.path.exists(f"./tfrecords/{part}/{data_type}/{tf_record_name}.tfrecord"):
        print(f"Grabbing {tf_record_name}.tfrecord")
        curr_response = requests.get(
            f"http://storage.googleapis.com/us.data.yt8m.org/2/{part}/{data_type}/{tf_record_name}.tfrecord")
        with open(f"./tfrecords/{part}/{data_type}/{tf_record_name}.tfrecord", "wb") as f:
            f.write(curr_response.content)


# session = FuturesSession()
# reqs = []
# for link in soup.find_all('a'):
#     i += 1
#     tf_record_full_name = link.get('href')
#     tf_record_name = tf_record_full_name.split(".")[0]
#     if not os.path.exists(f"./COMPS/data/{data_type}/{tf_record_name}.tfrecord"):
#         print("Grabbing: ", tf_record_name)
#         print(f"http://storage.googleapis.com/us.data.yt8m.org/2/{part}/{data_type}/{tf_record_name}.tfrecord")
#         reqs.append(session.get(f"http://storage.googleapis.com/us.data.yt8m.org/2/{part}/{data_type}/{tf_record_name}.tfrecord"))

# with session as sess:
#     for future in as_completed(reqs):
#         print(f"Completed request for {tf_record_name}")
#         curr_response = future.result()
#         with open(f"./data/{part}/{data_type}/{tf_record_name}.tfrecord", "wb") as f:
#             f.write(curr_response.content)
#             print("Content downloaded.")