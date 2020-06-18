#!/usr/bin/env python3

from datetime import datetime
from json import loads
from typing import NamedTuple, Tuple

from requests import Session


class Picture(NamedTuple):
    url: str
    height: int
    width: int


class ImageSet(NamedTuple):
    horizontal: Picture
    vertical: Picture


def get_images() -> Tuple[ImageSet, str]:
    endpoint = (
        # Just becase we can concatenate the string :)
        "https://arc" + ".msn" + ".com/v3/Delivery/Cache?"
        + "pid=209567&fmt=json&rafb=0&ua=" + "WindowsShellClient%2F0&disphorzres=9999"
        + "&dispvertres=9999&lo=80217&pl=en-US&lc=en-US&ctry=us&time="
        + datetime.now().isoformat()
    )

    images: ImageSet = None
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    with Session() as s:
        print(f"Endpoint URL {endpoint}")
        resp = s.get(endpoint, headers=headers)
        if resp.status_code != 200:
            print("E: " + resp.text)
            return images, ""
        resp_data = loads(resp.text)
        if "batchrsp" not in resp_data or "items" not in resp_data["batchrsp"]:
            return images, ""
        item = resp_data["batchrsp"]["items"][0]
        item = loads(item["item"])
        if "ad" not in item:
            return images, ""
        ad = item["ad"]
        copyrights_text = ad["copyright_text"]["tx"]
        image = ad["image_fullscreen_001_landscape"]
        landscape = Picture(url=image["u"], height=int(image["h"]), width=int(image["w"]),)

        image = ad["image_fullscreen_001_portrait"]
        portrait = Picture(url=image["u"], height=int(image["h"]), width=int(image["w"]),)
        images = ImageSet(horizontal=landscape, vertical=portrait)
    return images, copyrights_text


def _get_image_data(url: str):
    if not url:
        return b""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    data = bytes()
    with Session() as s:
        resp = s.get(url, headers=headers, stream=True)
        if not resp.ok:
            return data
        for chunk in resp.iter_content(1024):
            data += chunk
    return data


if __name__ == "__main__":
    image_set, copyright_text = get_images()
    time_str = datetime.now().strftime("%Y%m%d.%H%M")
    with open(f"{time_str}-copyright.txt", "w") as f:
        f.write(f"Wallpaper: {copyright_text}")
    # Make veritical image
    portrait_data = _get_image_data(image_set.vertical.url)
    if portrait_data:
        with open(
            f"{time_str}-portrait-{image_set.vertical.height}x{image_set.vertical.width}.jpg", "wb"
        ) as f:
            f.write(portrait_data)
    del portrait_data
    # Make Landscape image
    landscape_data = _get_image_data(image_set.horizontal.url)
    if landscape_data:
        with open(
            f"{time_str}-landscape-{image_set.horizontal.height}x{image_set.horizontal.width}.jpg",
            "wb",
        ) as f:
            f.write(landscape_data)
    del landscape_data
