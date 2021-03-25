# PRJ_Aging_Brain

## Installation
### For Mac OS / Mac OS X
* Install the latest version of Python 3 - below is a quick summary taken from the website: https://docs.python-guide.org/starting/install3/osx/
    * Open terminal and install Homebrew. Copy the command below in your terminal and press Enter to do so.
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
    ```
    * Add Homebrew directory to PATH environment variable. You can do this by adding the following line at the bottom of your ~/.profile file.
    ```bash    
    export PATH="/usr/local/opt/python/libexec/bin:$PATH"
    ```
    If you have OS X 10.12 (Sierra) or older use this line instead.
    ```bash
    export PATH=/usr/local/bin:/usr/local/sbin:$PATH
    ```
    * Install Python 3 by running the following command in your terminal:
    ```bash
    $ brew install python
    ```
    Note: Homebrew installs pip pointing to the Homebrew’d Python 3 for you.
* Now install the following modules using pip:
    * numpy
    * pandas
    * matplotlib
    * nuitka

    These can be installed by using the command:
    ```bash
    $ python3 -m pip install *InsertPackageNameHere*
    ```
  Example: To install pandas you would type
    ```bash
    $ python3 -m pip install pandas
    ```
Now you're ready to run the app! Please go to the Running section to see how to proceed.

### For Linux
* Install the latest version of Python 3 - below is a quick summary taken from the 
  website: https://docs.python-guide.org/starting/install3/linux/
    * If you are using Ubuntu 16.10 or newer, then you can easily install Python 3.6 with the 
      following commands:
    ```bash
    $ sudo apt-get update
    $ sudo apt-get install python3
    ```
    * If you’re using another version of Ubuntu (e.g. the latest LTS release) or you want to 
  use a more current Python, we recommend using the deadsnakes PPA to install Python 3.8:    
  ```bash    
    export PATH="/usr/local/opt/python/libexec/bin:$PATH"
    ```
    If you have OS X 10.12 (Sierra) or older use this line instead.
    ```bash
    $ sudo apt-get install software-properties-common
    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo apt-get update
    $ sudo apt-get install python3.8
    ```
    * If you are using other Linux distribution, chances are you already have Python 3
      pre-installed as well. If not, use your distribution’s package manager. For example on
      Fedora, you would use dnf:
    ```bash
    $ sudo dnf install python3
    ```
    Note: Make sure you have pip and setuptools installed. Please follow the website
  https://pip.pypa.io/en/latest/installing/ for more details. To check if pip was automatically
  installed, you can run the following command:
  ```bash
    $ python3 -m pip --version
    ```
  If yes, you can check if setuptools are installed by using the command:
  ```bash
    $ python3 -m pip list
    ```
  And look for the setuptools package.
  
  If you do not have either, you can easily install pip and setuptools on Ubuntu 20.04 using 
  the command:
    ```bash
    $ sudo apt-get update
    $ sudo apt-get install python3-pip
    $ sudo apt-get install python3-setuptools
    ```
  
* Now install the following modules using pip:
    * numpy
    * pandas
    * matplotlib
    * nuitka

    These can be installed by using the command:
    ```bash
    $ python3 -m pip install *InsertPackageNameHere*
    ```
  Example: To install pandas you would type
    ```bash
    $ python3 -m pip install pandas
    ```
Now you're ready to run the app! Please go to the Running section to see how to proceed.
### For Windows


https://pypi.org/project/Nuitka/ \
https://nuitka.net/doc/user-manual.html#id3