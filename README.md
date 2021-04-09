# Learning Simulation of the Brain
This is a Python implementation simulating the learning process in the ageing brain and also
offers a graphical user interface (GUI) for easier user interactions. The simulation 
parameters can be modified by changing the source code or through the GUI before each model 
generation for a more personalised user experience.

The application is split into three distinct sections, each in their own folders: the model, 
the view or GUI, and the analysis. There is a main.py file in the parent folder that the user 
interacts with to run code either from the view section or the analysis section.

## Attributions
The Neuron class in the Neuron.py file has been inspired and adapted from the article Neural Modeling with Python (Part 1) written by Byron Galbraith in
Jan 19, 2011: http://neurdon.wpengine.com/2011/01/19/neural-modeling-with-python-part-1/.

The code used in the generateSynapticWeights(...) method in the NeuralNetwork.py file was taken and adapted from the answers of
RishiG and Sam Manson in the Dec 2019 stack overflow post 'How to get N random integer numbers whose sum is equal to M':
https://stackoverflow.com/questions/59148994/how-to-get-n-random-integer-numbers-whose-sum-is-equal-to-m.

The label and checkbutton creation methods (makeLabelAndEntry(...) & makeLabelAndCheckbutton(...)) in the MainWindow.py file were learnt and
adpated from the 'How To Create TextBox In Python TKinter' tutorial on codeloop:
https://codeloop.org/how-to-create-textbox-in-python-tkinter/.

The canvas drawings in the NeuralNetworkFrame.py file were partially inspired from the Bryan Oakley answer in the Jan 24, 2011 stack overflow post
'tkinter: displaying a square grid': https://stackoverflow.com/questions/4781184/tkinter-displaying-a-square-grid.

The code that displays the generated matplotlib figure in the ViewPropertiesWindows.py file has been learnt and adpated from the Eric Levieil answer in
the July 15, 2015 stack overflow post 'Placing plot on Tkinter main window in Python':
https://stackoverflow.com/questions/31440167/placing-plot-on-tkinter-main-window-in-python.

## Installation
### For Mac OS / Mac OS X
* First install a GCC. This can be obtained by downloading and installing Xcode using the following link:
  https://developer.apple.com/xcode/
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
  
If you already have Python 3 installed, please update or upgrade it to the latest version.

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
    * If you are using Ubuntu 18.04 or newer, then you can easily install Python 3 with the 
      following commands:
    ```bash
    $ sudo apt-get update
    $ sudo apt-get install python3
    ```
    * If that does not work or face other issues, you can also use deadsnakes PPA to install new versions of 
      Python 3. Below are the steps to install Python 3.8:
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
  
  If you already have Python 3 installed, please update or upgrade it to the latest version.

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
  * Download the appropriate latest Windows installer from https://www.python.org/downloads/windows/
  * Run the executable installer \
  Note: Make sure you select  Install launcher for all users and Add Python 3.7+ to PATH checkboxes. The latter 
    places the interpreter in the execution path. For all recent versions of Python, the recommended installation
    options include Pip and IDLE so no need for specifying a custom installation in the setup application.

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
  
If you already have Python 3 installed, please update or upgrade it to the latest version.

Now you're ready to run the app!

## Running

### For Mac OS / Mac OS X / Linux
* First navigate to this project folder where this README file is located using the terminal.
* Run the following command and respond yes to any prompts that come up:
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
* First navigate to this project folder where this README file is located using the Windows Command Prompt.
* Run the following command and respond yes to any prompts that come up:
```bash
$ python -m nuitka main.py
```
This will generate optimised source code for a MinGW64 based C compiler by default.
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

### If Nuitka fails to run, please follow the following links to make sure you have the correct requirements:
* https://nuitka.net/doc/user-manual.html#id3
* https://pypi.org/project/Nuitka/

## System Requirements
### Minimum Requirements
There are not any specific minimum requirements as long as the latest version of Python 3 can be installed on your
computer. Any modern day computer should be able to install and run Python 3 so unless you have a very out-dated 
system, there should not be any issues. In the case there are, please refer to 'The Hitchhiker’s Guide to Python'
by using the following url: https://docs.python-guide.org/.

### Recommended Requirements
To ensure a smooth installation and running process, these are the recommended hardware and software requirements:
* Any modern day operating system
  * Windows 7 or 10
  * Mac OS X 10.11 or higher, 64-bit
  * Linux: RHEL 6/7 or Ubuntu 18.04+ LTS, 64-bit
* A x86 64-bit CPU (Intel / AMD architecture)
* 2 GB RAM
* 1 GB free disk space

### Details on Operating Systems
Out of the three types of operating systems that were listed in the recommended requirements sections,
the most preferred choice would be the most up to date long-term-support (LTS) Linux distributions, such as RHEL 7 or 
Ubuntu 20.04 LTS, as they natively uses the GCC compiler when running python scripts which seems to optimize and 
run this simulation much better than other compilers such as Clang/LLVM on OS X.
Nuitka is not strictly necessary on these Linux distributions but is still helpful
in reducing possible overhead and make certain checks. It also displays the simulation in the best format as Linux
distributions do not have as much GUI restrictions such as the button height being unchangable on Mac operating
systems. The Windows 7/10 are the least preferred choice of operating systems as the Windows systems themselves are not as programming
friendly as what Mac or Linux offers.

A detail to note is that the Ubuntu Linux 16.04 LTS will no longer be supported by April 30, 2021. This means
that the Ubuntu 16.04 LTS will stop receiving security patches or other software updates by April 30, 2021. This is
why Ubuntu 18.04+ LTS was recommended even though Ubuntu Linux 16.04 LTS would run this application perfectly fine.

## Bugs & Errors
All the known bugs and errors in this application arise from the passing of inappropriate parameters to the Learning Simulator class. This can be done through both the GUI and the analysis generator that the user can interact with. The following list contains the inappropriate parameters for the Learning Simulator class:

* When the input or output neuron amount is less than 1.
* When the synaptic strength is less than 0.
* When the memory capacity is more than 100\% (105\% in specific because of integer casting and float-rounding functions).
* When the output neuron amount multiplied by the memory capacity is less than or equal to 1 (0.5 in specific because of integer casting and float-rounding functions).
* When the values for any of the simulation factors contain a non-number, i.e. string or character.
