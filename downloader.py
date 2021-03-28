import logging
import os
import sys
import time
import requests
from urllib import parse


log = logging.getLogger(__name__)


class Downloader:
    def __init__(self):
        log.info("Initializing downloader.")
        access_key = os.getenv("UNSPLASH_ACCESS_KEY", sys.argv[1])
        self.time_to_sleep = os.getenv(
            "SLEEP_FOR", sys.argv[2]
        )  # Sleep for x seconds between each request.
        image_count = os.getenv("IMAGE_COUNT", sys.argv[3])
        self.destination_dir = os.getenv("DESTINATION_DIR", sys.argv[4])

        self.unsplash_api_url = (
            "https://api.unsplash.com/"
            f"photos/random/?count={image_count})"
            f"&client_id={access_key}"
        )

        if not os.path.isdir(self.destination_dir):
            log.info(f"Creating non-existant {self.destination_dir}.")
            os.makedirs(self.destination_dir, exist_ok=True)

        log.info(
            (
                f"Amount of images to download: {image_count}.\n"
                f"Sleep for seconds: {self.time_to_sleep}.\n"
                f"Destination directory: {self.destination_dir}."
            )
        )

    def get_image_list(self):
        res = requests.get(self.unsplash_api_url)

        data = res.json()

        if res.status_code == 200:
            return data

        raise ConnectionError(f"Status code: {res.status_code}.")

    def download_images(self):

        data = self.get_image_list()
        log.info(f"Got array of length {len(data)}.")

        urls = [image_data["urls"]["full"] for image_data in data]

        for url in urls:
            res = requests.get(url, stream=True)
            parsed = parse.urlparse(url)
            file_name = parsed.path[1:]
            file_ext = parse.parse_qs(parsed.query)["fm"][0]
            file_name_with_ext = f"{file_name}.{file_ext}"

            log.info(f"Downloading {file_name_with_ext}.")
            with open(
                os.path.join(self.destination_dir, file_name_with_ext), "wb"
            ) as image_file:
                for block in res.iter_content(1024 * 8):

                    if not block:
                        break

                    image_file.write(block)
            log.info("Success. Will now sleep.")
            time.sleep(int(self.time_to_sleep))


if __name__ == "__main__":
    downloader = Downloader()
    downloader.download_images()
