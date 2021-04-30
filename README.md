# The Visualization Toolkit rendering the Boston Teapot
This project render [the boston teapot](https://www.sjbaker.org/wiki/index.php?title=The_History_of_The_Teapot) using [The Visualization Toolkit](https://vtk.org/) in different ways to visualize the attributes of the dataset. 
* [Technologies](#technologies)
* [Setup](#setup)
* [Examples](#examples)

## Technologies
Project is created with:
* Python: 3.7.4
* Vtk: 9.0.1

## Setup
Clone the repository: `git clone git@github.com:Adilius/Python_VTK_BostonTeapot.git`

Change directory to repoitory: `cd Python_VTK_BostonTeapot`

Install the dependencies using pip: `pip install -r requirements.txt`

Incase you get a Python version mismatch when installing dependencies:

```
ERROR: Could not find a version that satisfies the requirement vtk

ERROR: No matching distribution found for vtk
```
Create a virtual enviroment inside the repository with python 3.7.4 using Powershell: `virtualenv -p /path/to/Python/Python37/python.exe venv`

Activate the virtual enviroment: `venv\Scripts\activate.ps1`

Then install dependencies again: `pip install -r requirements.txt`

When done running examples code, exit the virtual enviroment using: `deactivate`

## Examples

<details>
<summary>Volume visualization</summary>
Run it using command: 
  
```python
python volume.py
```
https://user-images.githubusercontent.com/43440295/115959178-41143a00-a50b-11eb-93aa-c0f0220c6dec.mp4
</details>

<details>
<summary>Contour visualization</summary>
Run it using command: 
  
```python
python contour.py
```
https://user-images.githubusercontent.com/43440295/115965096-cad20080-a527-11eb-95c7-79206c488b98.mp4
</details>

<details>
<summary>Slice visualization</summary>
Run it using command: 
  
```python
python slice.py
```
https://user-images.githubusercontent.com/43440295/115959180-42ddfd80-a50b-11eb-8e5a-b6d9d25c2f08.mp4
</details>

<details>
<summary>Clip visualization</summary>
Run it using command: 
  
```python
python contour_clip.py
```
https://user-images.githubusercontent.com/43440295/115971134-06c88e00-a547-11eb-9555-295ba2a7dfe9.mp4
</details>
