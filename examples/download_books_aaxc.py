import pathlib
import shutil

import audible
import requests


# files downloaded via this script can't be converted at this moment
# audible uses a new format (aaxc instead of aax)
# more informations and workaround here:
# https://github.com/mkb79/Audible/issues/3


# get download link(s) for book
def _get_download_link(asin, quality):
    try:
        response, _ = client.post(
            f"content/{asin}/licenserequest",
            body={
                "drm_type": "Adrm",
                "consumption_type": "Download",
                "quality": quality
            }
        )
        return response['content_license']['content_metadata']['content_url']['offline_url']
    except Exception as e:
        print(f"Error: {e}")
        return


def download_file(url, filename):
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return filename


if __name__ == "__main__":
    password = input("Password for file: ")

    auth = audible.FileAuthenticator(
        filename="FILENAME",
        encryption="json",
        password=password
    )
    client = audible.AudibleAPI(auth)

    books, _ = client.get(
        path="library/books",
        api_version="0.0",
        params={
            "purchaseAfterDate": "01/01/1970"
        }
    )["books"]["book"]

    for book in books:
        asin = book['asin']
        title = book['title'] + f" ({asin})" + ".aaxc"
        dl_link = _get_download_link(asin, quality="Extreme")
        if dl_link:
            filename = pathlib.Path.cwd() / "audiobooks" / title
            print(f"download link now: {dl_link}")
            status = download_file(dl_link, filename)
            print(f"downloaded file: {status}")
