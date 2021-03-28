import logging
import os
import sys
import time
import requests
from urllib import parse


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))


class Downloader:
    def __init__(self):
        log.info("Initializing downloader.")
        access_key = os.getenv("UNSPLASH_ACCESS_KEY", sys.argv[1])
        self.headers = {"Authorization": "Client-ID " + access_key}
        self.time_to_sleep = int(
            os.getenv("SLEEP_FOR", sys.argv[2])
        )  # Sleep for x seconds between each request.
        image_count = int(os.getenv("IMAGE_COUNT", sys.argv[3]))
        self.destination_dir = os.getenv("DESTINATION_DIR", sys.argv[4])

        # Unsplash allows fetching up to 30 images in one bundle.
        # We have to iterate image_count / 30 times to get the desired amount.
        self.iteration_count = int(image_count / 30)
        self.unsplash_api_url = (
            "https://api.unsplash.com/" "photos/random/?count=30"
        )  # noqa
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

    def log_errors(self, error_list, status_code=None):
        if status_code:
            log.error(f"Status code: {status_code}")
        for error in error_list:
            log.error(f"Error: {error}")

    def get_image_list(self):

        image_list = []

        def request_images():
            return requests.get(self.unsplash_api_url, headers=self.headers)

        for idx, __ in enumerate(range(self.iteration_count)):

            log.info(f"Attempting to fetch batch {idx}")

            res = request_images()
            data = res.json()
            if res.status_code == 200:
                log.info("Success.")
                image_list += [image_data for image_data in data]
            else:
                self.log_errors(data["errors"], res.status_code)
                log.info("Will sleep before retrying")
                time.sleep(self.time_to_sleep)
                res = request_images()
            log.info("Will sleep before next request.")
            time.sleep(self.time_to_sleep)

        return image_list

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
            time.sleep(self.time_to_sleep)


if __name__ == "__main__":
    downloader = Downloader()
    downloader.download_images()
