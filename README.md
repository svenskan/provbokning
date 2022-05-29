# Provbokning

## Installation

1. Install [Homebrew]:

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python 3:

```shell
brew install python3
```

3. Install [Google Chrome]. If the browser is already installed, update to the
   latest version (open `chrome://settings/help` in Chrome).

4. Clone this repository in some folder, such as `Downloads`:

```shell
cd ~/Downloads
git clone https://github.com/svenskan/provbokning.git
```

5. Install Python packages:

```shell
cd ~/Downloads/provbokning
pip3 install -r requirements.txt
```

6. Download and unpack the latest version of [ChromeDriver] in `provbokning`,
   which was created after cloning. The version of ChromeDriver should match the
   one of Chrome (open `chrome://settings/help` in Chrome). After unpacking,
   there should be a file called `chromedriver` directly in `provbokning`, not
   in a subfolder called `chromedriver`.

## Usage

1. Open and fill out `config.py`.

2. Run `bot.py` for reserving a time slot for 15 minutes so you have time to
   complete the process manually; a sound will be played. During the first
   execution, macOS might prevent ChromeDriver from running due to security
   reasons. If this is the case, shut down the script, go to System Preferences,
   open Security & Privacy, click General, and allow it to run.

```shell
cd ~/Downloads/provbokning
PATH="${PATH}:${PWD}" python3 bot.py
```

3. Alternatively, run `bot2.py` for doing everything automatically except for
   the payment, which will be postponed until later. It will also require a
   manual authentication via BankID upon start.

```shell
cd ~/Downloads/provbokning
PATH="${PATH}:${PWD}" python3 bot2.py
```

[ChromeDriver]: https://sites.google.com/chromium.org/driver/
[Google Chrome]: https://www.google.com/chrome/
[Homebrew]: https://brew.sh/
