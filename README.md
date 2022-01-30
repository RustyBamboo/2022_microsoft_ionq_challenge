# Leap through the Channel - Microsoft + IONQ challenge @ MIT iQuHack 2022

<p align="left">
  <a href="https://azure.microsoft.com/en-us/solutions/quantum-computing/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488491-609828a4-cd1f-4076-b5b2-a8d9fc2d0fa4.png" width="30%"/> </a>
  <a href="https://ionq.com/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488159-da95eb05-9277-4abe-b1ba-b49871d563ed.svg" width="20%" style="padding: 1%;padding-left: 5%"/></a>
  <a href="https://iquhack.mit.edu/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151647370-d161d5b5-119c-4db9-898e-cfb1745a8310.png" width="8%" style="padding-left: 5%"/> </a>
</p>


A simplistic arcade-like shooter game powered by Qiskit, Azure, and IONQ computers.

Try to defeat incoming invaders by selecting the correct weapon (left and right arrow keys) and firing (space). You may encounter some unexpected behavior with your weapon (quantum noise). But do not fear, once you beat enough enemies you will be awarded upgrades that fix your weapon (quantum error correction!)

Your weapons include: `hadafire`, `x-bringer`, `z-bringer` which correspond to quantum gates!

## Demo
![Demo](media/demo.gif)

## Running
- Ensure you have `python3` and `pip3` installed
- Download this repo and enter directory
- `pip install -r requirements.txt`
- `./main.py`

### Behind the scenes

If you want to learn about how it works, as well as the error correction, look [here](tutorial/tutorial.ipynb)

## MIT iQuHack 2022 Experience

IQuHack made a virtual hackathon fun! Everything was very organized and enabled people to meet and talk to other people. In the case of our group, we all meet through slack and gather.town -- and we all were undergraduate or graduate students working on quantum computing.

On the flip side, we did not enjoy the challenges -- sure, making a game is a fun creative process that would work for all scopes of experience and has a lot of oppurtunity to establish a platform for outreach. But given that we have been studying/working in the field, what we expected walking into this was something along the lines of "perform _quantum error correction_, or maximizing quantum capability through _pulse-level control of trapped ions_." Despite that, we made the most out of that and included quantum error correction as part of our game.



## Files and Structure
```
.
├── entities
│   ├── bullet.py
│   ├── dashboard.py
│   ├── enemy.py
│   ├── __init__.py
│   ├── player.py
│├── levels
│   ├── __init__.py
│   ├── level0.py
│   ├── level_controller.py
│   └── level.py
├── main.py
├── media
│   └── demo.gif
├── README.md
└── requirements.txt
```

## References
```
[1]R. Chao and B. W. Reichardt, “Fault-tolerant quantum computation with few qubits,” npj Quantum Inf, vol. 4, no. 1, p. 42, Dec. 2018.
[2]M. Urbanek, B. Nachman, and W. A. de Jong, “Quantum error detection improves accuracy of chemical calculations on a quantum computer,” arXiv:1910.00129 [physics, physics:quant-ph], Sep. 2019.
```
