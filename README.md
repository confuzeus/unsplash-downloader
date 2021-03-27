# Unsplash random image downloader

Download random images from unsplash.

## Usage

1. Install packages with `pip install -r requirements.txt`
2. Run with `python3 downloader.py [OPTIONS]`

### Options

You can set options using either environment variables or command line arguments.

The following environment variables are available:

`UNSPLASH_ACCESS_KEY` - The access key used to download image metadata from Unsplash.
    
`SLEEP_FOR` - The number of seconds to sleep between each request. This is used to prevent triggering rate limiting.

`IMAGE_COUNT` - The number of images to download.

`DESTINATION_DIR` - The destination where to save the images. If this doesn't exist, it will be created.

To configure using command like arguments, use the same order. Example:

`python3 downloader.py mY-$ecret-@cce$s-keY 60 1000 /home/user/downloads/unsplash`

This will download 1000 images to /home/user/downloads/unsplash and sleep 60 seconds between each request.