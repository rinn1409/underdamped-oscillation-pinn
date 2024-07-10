A physics-informed neural network (PINN) to approximate the waveform of a 1D underdamped harmonic oscillator. The code contains both a normal fully-connected network as well as a network which incorporates a 'physics loss' term in order to accurately predict the harmonic oscillator waveform.
![image](https://github.com/rinn1409/underdamped-oscillation-pinn/assets/91346597/ee59fd3c-e8dd-4546-8062-203a19c8e4ea)
![image](https://github.com/rinn1409/underdamped-oscillation-pinn/assets/91346597/4e0712a6-4be2-49ec-925b-1cea2b4b4dce)
First image shows the network struggling to predict the waveform apart from the training point locations.
The second image shows the graphs of PINN predictions, using a physics loss term in the loss function.
