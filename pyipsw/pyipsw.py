from functools import lru_cache
import hashlib
import os

from tqdm import tqdm
import requests

IPSW_API_FIRMWARES_JSON = 'https://api.ipsw.me/v2.1/firmwares.json/condensed'
DEVICES_FIELDS = ['device', 'name', 'version', 'buildid', 'url', 'uploaddate', 'size', 'signed', 'sha1sum',
                  'releasedate', 'platform', 'md5sum', 'filename', 'cpid', 'bdid', 'BoardConfig']
ITUNES_FIELDS = ['os', 'version', 'url', 'releasedate', 'uploaddate', '64biturl']
DOWNLOAD_CHUNK_SIZE = 8192


@lru_cache()
def fetch_firmwares():
    """
    Fetch the firmwares json from ipsw.me server.
    :return: Dictionary contains the devices and itunes data.
    :rtype: dict
    """
    return requests.get(IPSW_API_FIRMWARES_JSON).json()


def _filter_locals(filter_: str, locals_) -> bool:
    """
    Evaluate a condition string.
    :param filter_: Python code to evaluate.
    :param locals_: Locals to supply to the code.
    :return: True if the condition is true, False otherwise.
    """
    return eval(filter_, {}, locals_)


def _flatten_devices(firmwares, filter_: str = ''):
    """
    Convert nested ipsw.me firmwares data to a flat representation of devices.
    :param dict firmwares: Firmwares data from ipsw.me.
    :param filter_: Python code to filter by.
    :return: Devices' firmwares data
    :rtype: list
    """
    all_firmwares = []
    for device_key, device in firmwares['devices'].items():
        for firmware in device['firmwares']:
            firmware.update({
                'device': device_key,
                'name': device['name'],
                'BoardConfig': device['BoardConfig'],
                'platform': device['platform'],
                'cpid': device['cpid'],
                'bdid': device['bdid'],
            })
            if filter_ and not _filter_locals(filter_, firmware):
                continue
            all_firmwares.append(firmware)
    return all_firmwares


def _flatten_itunes(firmwares, filter_: str = ''):
    """
    Convert nested ipsw.me firmwares data to a flat representation of itunes versions.
    :param dict firmwares: Firmwares data from ipsw.me.
    :param filter_: Python code to filter by.
    :return: Itunes' versions data
    :rtype: list
    """
    all_versions = []
    for os_, itunes in firmwares['iTunes'].items():
        for itune in itunes:
            itune.update({
                'os': os_,
            })
            if filter_ and not _filter_locals(filter_, itune):
                continue
            all_versions.append(itune)
    return all_versions


def get_devices(filter_: str = '', reload: bool = False):
    """
    Get devices firmwares data.
    :param filter_: Python code to filter data. All names in `DEVICES_FIELDS` will be available as locals.
    :param reload: If ipsw.me data is already cache, fetch it again.
    :return: dict
    """
    if reload:
        fetch_firmwares.cache_clear()
    return _flatten_devices(fetch_firmwares(), filter_)


def get_itunes(filter_='', reload=False):
    """
    Get itunes versions data.
    :param filter_: Python code to filter data. All names in `ITUNES_FIELDS` will be available as locals.
    :param reload: If ipsw.me data is already cache, fetch it again.
    :return: dict
    """
    if reload:
        fetch_firmwares.cache_clear()
    return _flatten_itunes(fetch_firmwares(), filter_)


def _download_device(out_directory: str, device) -> None:
    """
    Download a device firmware.
    :param out_directory: Directory to write the firmware to.
    :param dict device: Device's data.
    """
    final_path = os.path.join(out_directory, device['filename'])
    if os.path.exists(final_path):
        with open(final_path, 'rb') as fd:
            data = fd.read()
        if hashlib.sha1(data).hexdigest() == device['sha1sum']:
            # File was already downloaded.
            return
    resp = requests.get(device['url'], allow_redirects=True, stream=True)
    with open(final_path, 'wb') as fd:
        with tqdm(total=device['size'], unit_scale=True, unit='B') as download_bar:
            for chunk in resp.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                fd.write(chunk)
                download_bar.update(DOWNLOAD_CHUNK_SIZE)


def download_devices(out_directory: str, filter_: str = '', reload: bool = False) -> None:
    """
    Download devices firmwares.
    :param out_directory: Directory to write the firmware to.
    :param filter_: Python code to filter data. All names in `DEVICES_FIELDS` will be available as locals.
    :param reload: If ipsw.me data is already cache, fetch it again.
    """
    if reload:
        fetch_firmwares.cache_clear()
    devices = _flatten_devices(fetch_firmwares(), filter_)
    with tqdm(devices) as files_bar:
        for device in files_bar:
            files_bar.set_description(f'Downloading {device["filename"]}')
            _download_device(out_directory, device)
