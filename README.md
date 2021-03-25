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
* Install the latest version of Python 3 - below is a quick summary taken from the 
  website: https://phoenixnap.com/kb/how-to-install-python-3-windows
  * Download the appropriate latest installer from https://www.python.org/downloads/windows/
  * Run the executable installer \
  Note: Make sure you select  Install launcher for all users and Add Python 3.7 to PATH checkboxes. The latter 
    places the interpreter in the execution path. For all recent versions of Python, the recommended installation
    options include Pip and IDLE.

* Now install the following modules using pip:
    * numpy
    * pandas
    * matplotlib
    * nuitka

    These can be installed by opening Command Prompt and using the following command:
    ```bash
    C:\Users\Username> python -m pip install *InsertPackageNameHere*
    ```
  Example: To install pandas you would type
    ```bash
    C:\Users\Username> python -m pip install pandas
    ```
Now you're ready to run the app!

## Running

### For Mac OS / Mac OS X / Linux
* First navigate to this project folder where this README file is located using the terminal.
* Run the following command:
```bash
$ python3 -m nuitka main.py
```
This will generate optimised source code for a C backend complier.
* Finally run the last command:
```bash
$ ./main.bin
```
To run the application or run
```bash
$ ./main.bin -analysis
```
To run the BrainAnalysis.py file located in the analysis folder which provides only the analysis.

Note: You can also run the command:
```bash
$ python3 main.py
```
To run the application but using the nuitka code generator is heavily recommended especially if you are on
Mac OS / Mac OS X as the simulation will run quite slowly otherwise.

### For Windows
* First navigate to this project folder where this README file is located using the Windows PowerShell.
* Run the following command:
```bash
$ python -m nuitka --mingw64 main.py
```
This will generate optimised source code for a MinGW64 based C compiler.
* Finally run the last command:
```bash
$ main.exe
```
To run the application or run
```bash
$ main.exe -analysis
```
To run the BrainAnalysis.py file located in the analysis folder which provides only the analysis.

Note: You can also run the command:
```bash
$ python main.py
```
To run the application but using the nuitka code generator is heavily recommended as the simulation will run 
quite slowly otherwise.

#### For more details on Nuitka, follow the following links:
* https://pypi.org/project/Nuitka/
* https://nuitka.net/doc/user-manual.html#id3