# AI Foundations Playbook

Want to learn the basics of AI? This project provides all you need for a simulation of cars and creating levels for the cars to try. 
Implement your own way of letting the cars learn by themselves how to pass the level

![Screenshot](Screenshot.jpg)

## Table of Contents

- Project Description
- Installation
- Usage
- Options
- Contact

## Project Description

The Car Navigation Simulation Project is a Python-based GUI application that allows users to design, simulate, and visualize car navigation through custom levels. The application is built using the Tkinter library for the graphical user interface and provides a set of classes that allow advanced users to customize the simulation behavior. Beginners should only edit the files in the "options" folder. The project aims to provide a user-friendly interface for designing levels, running simulations, and analyzing the performance of different car navigation strategies.

The LevelEditor allows users to create custom levels by defining a series of connected points on a canvas, where each point represents a street. Users can use the "Level Designer" tool to draw these levels and save them in JSON format. The application provides a "Level Viewer" tool to display the saved levels and a "Level Remover" tool to remove unwanted levels.

## Installation

Ensure you have Python installed on your system (Python 3.6 or later is recommended).  
Install further modules for advanced learning mechanisms.

## Usage

The LevelEditor allows users to create custom levels by defining a series of connected points on a canvas, where each point represents a street. Users can use the "Level Designer" tool to draw these levels and save them in JSON format. The application provides a "Level Viewer" tool to display the saved levels and a "Level Remover" tool to remove unwanted levels.

The core simulation engine of the project is located in the "Simulation.py" file. It simulates the navigation of multiple cars through the specified level. Users can select a level to simulate, and the application will display the simulation in a Tkinter window. Cars navigate through the level based on the brain logic defined in the "Brain.py" file. Edit Brain.py and Iteration.py to change the programs behaviour (Implement advanced learning mechanisms etc.)

## Options

YourBrain.py: Edit this file to define custom logic for car navigation. The YourBrain class contains methods to calculate turn angles and car movements.  
 -> For the simulation to use your brain also edit Brain.py and initialize YourBrain  
YourIteration.py: Edit this file to customize the car iteration process during the simulation. The YourIteration class allows advanced users to define their iteration logic.  
 -> For the simulation to use your iteration process also edit Iteration.py and initialize YourIteration  

## Contact
[LinkedIn](https://www.linkedin.com/in/joris-plettscher/)  
[GitHub](https://github.com/Joris-Plettscher)  
Feel free to customize this project to fit specific needs. Happy coding!
