# WI2012 Automation Scripts

Repository containing scripts used to automate schedule generator, group assignments, and various data cross-verifications.

## Requirements
* `Python` - `3.12` or closely compatible version
* `pip`
* `pipx` (for system installation)

## Running
### Development Mode
**You can edit the scripts on the fly, and the next time the command is run, the update will immediately take effect.** The module will only be installed on the `Python` environment you use to install the project

```bash
# create a python virtual enviroment (optional, but recommended to install the app in separate, isolated environment from system environment)
python -m venv .venv

# install the module
pip install --editable .
```
then run with
```bash
python -m otomasi [-h|--help] {command}
```

### Build
**If you only need to run the commands as is (system wide)**, install it with `pipx`, the command will automatically be loaded in your PATH - which means you can run the command in any directory, independent of which `Python` environment you're using (since it has been handled automatically by `pipx`'s virtual environments)

```bash
pipx install .
```

then run with
```bash
otomasi [-h|--help] {command}
```
