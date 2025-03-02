# -*- coding: utf-8 -*-
"""oscillator-pinn-final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/111fG-ZdSOMIVJ9AjvFpehh9B46nLVKUt
"""

from PIL import Image

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

def save_gif_PIL(outfile, files, fps=5, loop=0):
    "Helper function for saving GIFs"
    imgs = [Image.open(file) for file in files]
    imgs[0].save(fp=outfile, format='GIF', append_images=imgs[1:], save_all=True, duration=int(1000/fps), loop=loop)

def oscillator(d, w0, x):
    assert d < w0
    w = np.sqrt(w0**2-d**2)
    phi = np.arctan(-d/w)
    A = 1/(2*np.cos(phi))
    cos = torch.cos(phi+w*x)
    sin = torch.sin(phi+w*x)
    exp = torch.exp(-d*x)
    y  = exp*2*A*cos
    return y

class FCN(nn.Module):
    def __init__(self, n_input, n_output, n_hidden, n_layers):
        super().__init__()
        activation = nn.Tanh
        self.fcs = nn.Sequential(*[
                        nn.Linear(n_input, n_hidden),
                        activation()])
        self.fch = nn.Sequential(*[
                        nn.Sequential(*[
                            nn.Linear(n_hidden, n_hidden),
                            activation()]) for _ in range(n_layers-1)])
        self.fce = nn.Linear(n_hidden, n_output)

    def forward(self, x):
        x = self.fcs(x)
        x = self.fch(x)
        x = self.fce(x)
        return x

d, w0 = 1, 20

x = torch.linspace(0,1,500).view(-1,1)
y = oscillator(d, w0, x).view(-1,1)
print(x.shape, y.shape)

x_data = x[0:200:10]
y_data = y[0:200:10]
print(x_data.shape, y_data.shape)

plt.figure()
plt.plot(x, y, label="Exact solution")
plt.scatter(x_data, y_data, color="orange", label="Training data")
plt.legend()
plt.show()

def plot_result(x,y,x_data,y_data,yh,xp=None):
    plt.figure(figsize=(8,4))
    plt.plot(x,y, color="grey", alpha=0.8, label="Exact solution")
    plt.plot(x,yh, color="blue", alpha=0.8, label="NN prediction")
    plt.scatter(x_data, y_data, s=60, color="red", label='Training datapoints')
    if xp is not None:
        plt.scatter(xp, -0*torch.ones_like(xp), color="green",
                    label='Physics loss training locations')
    l = plt.legend(loc=(1.01,0.34), frameon=True, fontsize="large")
    plt.setp(l.get_texts(), color="k")
    plt.xlim(-0.05, 1.05)
    plt.ylim(-1.1, 1.1)
    plt.text(1.065,0.7,"Epoch no.: %i"%(i+1),fontsize="x-large",color="k")
    plt.axis("off")


# standard neural network
torch.manual_seed(123)
model = FCN(1,1,32,3)
optimizer = torch.optim.Adam(model.parameters(),lr=1e-3)
for i in range(1000):
    optimizer.zero_grad()
    yh = model(x_data)
    loss = torch.mean((yh-y_data)**2) # mean squared error
    loss.backward()
    optimizer.step()

    if (i+1) % 10 == 0:

        yh = model(x).detach()

        plot_result(x,y,x_data,y_data,yh)

        if (i+1) % 500 == 0: plt.show()
        else: plt.close("all")

x_physics = torch.linspace(0,1,30).view(-1,1).requires_grad_(True)
mu, k = 2*d, w0**2

torch.manual_seed(123)
model = FCN(1,1,32,3)
optimizer = torch.optim.Adam(model.parameters(),lr=1e-4)
for i in range(20000):
    optimizer.zero_grad()

    # compute the "data loss"
    yh = model(x_data)
    loss1 = torch.mean((yh-y_data)**2)# use mean squared error

    # compute the "physics loss"
    yhp = model(x_physics)
    dx  = torch.autograd.grad(yhp, x_physics, torch.ones_like(yhp), create_graph=True)[0]
    dx2 = torch.autograd.grad(dx,  x_physics, torch.ones_like(dx),  create_graph=True)[0]
    physics = dx2 + mu*dx + k*yhp
    loss2 = (1e-4)*torch.mean(physics**2)

    loss = loss1 + loss2 # add two loss terms together
    loss.backward()
    optimizer.step()

    if (i+1) % 150 == 0:

        yh = model(x).detach()
        xp = x_physics.detach()

        plot_result(x,y,x_data,y_data,yh,xp)


        if (i+1) % 6000 == 0: plt.show()
        else: plt.close("all")

