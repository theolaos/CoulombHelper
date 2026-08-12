# CoulombHelper: Electronic Physics simulator

A small algorithm that helps visualize and calculate for you the Law of Coulomb in real time!

Work with multiple point charges, and how they affect each other in space.

Move the point charges around, give different data, inspect the results.

Particle Visualizer is WIP (with the help of my game engine [tleng](https://github.com/tl-ecosystem/tleng))

# Installation

## How to download:

Go to releases!
<details>
<summary><h3>Windows</h3></summary>
 
 - Install the `.zip` file
 - Extract the `.zip` file to a folder of your liking
 - Double click the `.exe` file. 
 
</details>

<details>
<summary><h3>Linux</h3></summary>
  - Using Wine:
    - Ensure that you have wine installed.
    - Follow Windows How-To.

 - Linux binaries:
    - Install the `coulomb_helper.tar.gz` 
    - Extract the contents of `coulomb_helper.tar.gz`
    - Double click on the `coulomb_helper` file
</details>

<details>
<summary><h3>From Source</h3></summary>
 
- Clone the games repository locally. And clone the Tleng Game engine Locally
    ``` bash
    $ git clone https://www.github.com/theolaos/CoulombHelper.git
    $ git clone https://www.github.com/tl-ecosystem/tleng.git
    ```    
- Create a symbolic link inside CoulombHelper `src` directory from the tleng repo:
    ```bash
    $ ln -r -s ./tleng/src/tleng2 ./CoulombHelper/src
    ```
- Change to the game directory
    ``` bash
    $ cd CoulombHelper
    ```
- Create a virtual python enviroment and then activate it:
    ```bash
    $ python -m venv venv
    ```
    - linux
    ```bash
    $ source ./venv/bin/activate
    ```
    - Windows
    ```bash
    $ .\venv\Scripts\Activate.ps1
    ```
- Download the requirements:

    Using pip:
    ```bash
    $ pip install -r requirements.txt
    ```
    Using your package manager manually (apt, dnf, pacman ...):
    ```bash
    $ sudo 'your-package-manager' install pygame3-'your-package'
    ```
- Run the game.
    ```bash
    $ python main.py
    ```
</details>


# Contribute

You are free to contribute in any way you want. Just create a `pull request` and I will review it.
