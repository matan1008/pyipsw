[![Python application](https://github.com/matan1008/pyipsw/workflows/Python%20application/badge.svg)](https://github.com/matan1008/pyipsw/actions/workflows/python-app.yml "Python application action")
[![Pypi version](https://img.shields.io/pypi/v/pyipsw.svg)](https://pypi.org/project/pyipsw/ "PyPi package")
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/matan1008/pyipsw.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/matan1008/pyipsw/context:python)

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
    * [CLI](#cli)

# Description

`pyipsw` is a utility created in order to access ipsw.me data easily using python / cli.

# Installation

Install the last released version using `pip`:

```shell
python3 -m pip install --user -U pyipsw
```

Or install the latest version from sources:

```shell
git clone git@github.com:matan1008/pyipsw.git
cd pyipsw
python3 -m pip install --user -U -e .
```

# Usage

## CLI

In order to show data about devices, just run the devices command:

```shell
pyipsw devices
```

If you require more or less data, add `-c` with column name:

```shell
pyipsw devices -c device -c version -c BoardConfig
```

Run `pyipsw devices --help` to see available columns:

```shell
Usage: pyipsw devices [OPTIONS]

  Show data about apple devices.

Options:
  -c, --columns [device|name|version|buildid|url|uploaddate|size|signed|sha1sum|releasedate|platform|md5sum|filename|cpid|bdid|BoardConfig]
                                  Data to show
  -f, --filters TEXT              Python code to act as filter to devices,
                                  e.g. "iPhone11" in device
  --help                          Show this message and exit.
```

You can also add python code to filter the printed data:

```shell
pyipsw devices -f "'iPhone10' in device and '14.4' in version"
```

Which will output:

```
------------------------------------------------------------------------------------
| device     | version | buildid | filename                                        |
------------------------------------------------------------------------------------
| iPhone10,1 | 14.4.2  | 18D70   | iPhone_4.7_P3_14.4.2_18D70_Restore.ipsw         |
| iPhone10,1 | 14.4.1  | 18D61   | iPhone_4.7_P3_14.4.1_18D61_Restore.ipsw         |
| iPhone10,1 | 14.4    | 18D52   | iPhone_4.7_P3_14.4_18D52_Restore.ipsw           |
| iPhone10,2 | 14.4.2  | 18D70   | iPhone_5.5_P3_14.4.2_18D70_Restore.ipsw         |
| iPhone10,2 | 14.4.1  | 18D61   | iPhone_5.5_P3_14.4.1_18D61_Restore.ipsw         |
| iPhone10,2 | 14.4    | 18D52   | iPhone_5.5_P3_14.4_18D52_Restore.ipsw           |
| iPhone10,3 | 14.4.2  | 18D70   | iPhone10,3,iPhone10,6_14.4.2_18D70_Restore.ipsw |
| iPhone10,3 | 14.4.1  | 18D61   | iPhone10,3,iPhone10,6_14.4.1_18D61_Restore.ipsw |
| iPhone10,3 | 14.4    | 18D52   | iPhone10,3,iPhone10,6_14.4_18D52_Restore.ipsw   |
| iPhone10,4 | 14.4.2  | 18D70   | iPhone_4.7_P3_14.4.2_18D70_Restore.ipsw         |
| iPhone10,4 | 14.4.1  | 18D61   | iPhone_4.7_P3_14.4.1_18D61_Restore.ipsw         |
| iPhone10,4 | 14.4    | 18D52   | iPhone_4.7_P3_14.4_18D52_Restore.ipsw           |
| iPhone10,5 | 14.4.2  | 18D70   | iPhone_5.5_P3_14.4.2_18D70_Restore.ipsw         |
| iPhone10,5 | 14.4.1  | 18D61   | iPhone_5.5_P3_14.4.1_18D61_Restore.ipsw         |
| iPhone10,5 | 14.4    | 18D52   | iPhone_5.5_P3_14.4_18D52_Restore.ipsw           |
| iPhone10,6 | 14.4.2  | 18D70   | iPhone10,3,iPhone10,6_14.4.2_18D70_Restore.ipsw |
| iPhone10,6 | 14.4.1  | 18D61   | iPhone10,3,iPhone10,6_14.4.1_18D61_Restore.ipsw |
| iPhone10,6 | 14.4    | 18D52   | iPhone10,3,iPhone10,6_14.4_18D52_Restore.ipsw   |
------------------------------------------------------------------------------------
```

You can also download the firmwares with:

```shell
pyipsw download-devices /tmp/firmwares -f "'iPhone10' in device and '14.4' in version"
```