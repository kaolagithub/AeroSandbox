# [AeroSandbox](https://peterdsharpe.github.io/AeroSandbox/) 
by [Peter Sharpe](https://peterdsharpe.github.io) (<pds [at] mit [dot] edu>)

## VERSION 0 DEPRECATION NOTICE
Dear User,

If you're reading this, you're looking at the repository for the final release of AeroSandbox v0. Development of version 0 was concluded on 2/15/2020, and AeroSandbox v0 has since been replaced by AeroSandbox v1. Please consider updating to AeroSandbox v1. In v1, analyses can be up to 2 orders of magnitude faster, solutions can be fully nonlinear, viscous & shock effects can be modeled, the code now plays well with a simultaneous-analysis-and-design (SAND) architecture, and there are huge graphics updates thanks to Plotly. Version 1 is a MASSIVE upgrade.

If you do not want to upgrade, you may continue using AeroSandbox v0 from within AeroSandbox v1 by replacing your 
```python
import aerosandbox as asb
```
statement with
```python
import aerosandbox_legacy_v0 as asb
```

Thank you for your continued support!

## About
AeroSandbox is a Python package for aircraft design optimization, fully-coupled viscous/inviscid 3D aerodynamics, and reverse-mode automatic differentiation for computing gradients of design variables.

The 10-second elevator pitch: **In half a second, you can calculate not only the aerodynamic performance of an airplane, but also the sensitivity of aerodynamic performance with respect to an effectively-infinite number of design variables.** This can be used to perform gradient-based aircraft design optimization extremely quickly.

Work in progress!


![VLM3 Image](media/images/vlm3_with_control_surfaces.png)
*VLM3 simulation of a glider, aileron deflections of +-30°. Runtime of 0.35 sec on a typical laptop (i7-8750H).*

![PANEL1 Image](media/images/panel1_naca4412.png)
*PANEL1 simulation of a wing (extruded NACA2412, α=15°, AR=4). Note the strong three-dimensionality of the flow near the tip.*

## Getting Started

### Installation

There are several easy ways to get started with AeroSandbox! (Assuming you already have Python >=3.7 installed, preferably via the [Anaconda distribution](https://www.anaconda.com/distribution/#download-section) - if not, do this first.)

1. (Recommended) Download the latest release here: [https://github.com/peterdsharpe/AeroSandbox/releases](https://github.com/peterdsharpe/AeroSandbox/releases). Then, run "pip install AeroSandbox" in your command prompt to ensure that all dependencies are satisfied.

2. If you just want the raw package (and no test cases or examples), install by simply entering "pip install AeroSandbox" into your terminal. 

3. Both of the above options will download the latest official release of AeroSandbox. If you'd rather get a nightly/dev version (which has more features but may be buggy), clone or download directly from [the AeroSandbox GitHub page](https://github.com/peterdsharpe/AeroSandbox).

There are many example cases you can try out in the /examples/ directory! Specifically, try running "/examples/vlm3_conventional.py".

### Usage
AeroSandbox is designed to have extremely intuitive, high-level, and human-readable code. You (yes, you!) can probably learn to analyze a simple airplane and visualize airflow around it within 5 minutes of downloading AeroSandbox. For example, here is all the code that is needed to design a glider, analyze its aerodynamics in flight, and visualize it (found in "/examples/vlm3_conventional.py"):

```python
from aerosandbox import *

glider = Airplane(
    name="Peter's Glider",
    xyz_ref=[0, 0, 0], # CG location
    wings=[
        Wing(
            name="Main Wing",
            xyz_le=[0, 0, 0], # Coordinates of the wing's leading edge
            symmetric=True,
            xsecs=[ # The wing's cross ("X") sections
                WingXSec(  # Root
                    xyz_le=[0, 0, 0], # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
                    chord=0.18,
                    twist=2, # degrees
                    airfoil=Airfoil(name="naca4412"),
                    control_surface_type='symmetric',  # Flap # Control surfaces are applied between a given XSec and the next one.
                    control_surface_deflection=0, # degrees
                    control_surface_hinge_point=0.75 # as chord fraction
                ),
                WingXSec(  # Mid
                    xyz_le=[0.01, 0.5, 0],
                    chord=0.16,
                    twist=0,
                    airfoil=Airfoil(name="naca4412"),
                    control_surface_type='asymmetric',  # Aileron
                    control_surface_deflection=0,
                    control_surface_hinge_point=0.75
                ),
                WingXSec(  # Tip
                    xyz_le=[0.08, 1, 0.1],
                    chord=0.08,
                    twist=-2,
                    airfoil=Airfoil(name="naca4412"),
                )
            ]
        ),
        Wing(
            name="Horizontal Stabilizer",
            xyz_le=[0.6, 0, 0.1],
            symmetric=True,
            xsecs=[
                WingXSec(  # root
                    xyz_le=[0, 0, 0],
                    chord=0.1,
                    twist=-10,
                    airfoil=Airfoil(name="naca0012"),
                    control_surface_type='symmetric',  # Elevator
                    control_surface_deflection=0,
                    control_surface_hinge_point=0.75
                ),
                WingXSec(  # tip
                    xyz_le=[0.02, 0.17, 0],
                    chord=0.08,
                    twist=-10,
                    airfoil=Airfoil(name="naca0012")
                )
            ]
        ),
        Wing(
            name="Vertical Stabilizer",
            xyz_le=[0.6, 0, 0.15],
            symmetric=False,
            xsecs=[
                WingXSec(
                    xyz_le=[0, 0, 0],
                    chord=0.1,
                    twist=0,
                    airfoil=Airfoil(name="naca0012"),
                    control_surface_type='symmetric',  # Rudder
                    control_surface_deflection=0,
                    control_surface_hinge_point=0.75
                ),
                WingXSec(
                    xyz_le=[0.04, 0, 0.15],
                    chord=0.06,
                    twist=0,
                    airfoil=Airfoil(name="naca0012")
                )
            ]
        )
    ]
)

aero_problem = vlm3( # Analysis type: Vortex Lattice Method, version 3
    airplane=glider,
    op_point=OperatingPoint(
        velocity=10,
        alpha=5,
        beta=0,
        p=0,
        q=0,
        r=0,
    ),
)

aero_problem.run() # Runs and prints results to console
aero_problem.draw() # Creates an interactive display of the surface pressures and streamlines
```

The best part is that by adding just a few more lines of code, you can not only get the performance at a specified design point, but also the derivatives of any performance variable with respect to any design variable. Thanks to reverse-mode automatic differentiation, this process only requires the time of one additional flow solution, regardless of the number of design variables. For an example of this, see "/examples/gradient_test_vlm2.py".

One final point to note: as we're all sensible and civilized human beings here, all inputs and outputs to AeroSandbox are expressed in base metric units, or derived units thereof (meters, Newtons, meters per second, kilograms, etc.).

### Dependencies

The fastest way to ensure that all dependencies are satisfied is by simply running "pip install AeroSandbox" in your command prompt. However, you can also install dependencies on your own if you'd like. You'll need the following libraries:
* numpy
* scipy
* matplotlib
* numba
* autograd
* pyvista

If you installed Python via the [Anaconda distribution](https://www.anaconda.com/distribution/#download-section), you likely have all of these except autograd. (Install this with "pip install autograd" in the command prompt.)

OpenGL is also required for visualization, though this should already be installed on nearly every computer. (No promises if you try to run AeroSandbox on a Raspberry Pi or something!)

## Current Features
* User-friendly, concise, high-level, object-oriented structure for airplane geometry definition and analysis.
* Fully reverse-mode AD compatible vortex-lattice method flow solver ("VLM3")! Very fast (~0.35s for typical problems) and fully compatible with arbitrary combinations of lifting surfaces. With this, you can get the gradient of a design space with arbitrary dimensionality almost instantly.

## Purpose
The primary purpose for this repository is to explore existing methods for aerodynamic analysis and develop new methods within a unified code base.

This package eventually seeks to develop the following:
An aerodynamics tool that models flow around any general triangulated 3D shape (with non-separated flow) using strongly-coupled viscous/inviscid methods. If successful, this could be orders of magnitude faster than volume-mesh-based CFD while retaining high accuracy (XFoil is a 2D example of this).

This code is made open-source in hopes that the aerospace community can benefit from this work. I've benefitted so much from open-source aerospace tools that came before me (XFoil, AVL, QProp, GPKit, XFLR5, OpenVSP, SU2, and SUAVE, just to name a few), so I hope to pay it forward, at least in small part!

## Future Goals
In descending order of priority/feasibility:
* (DONE) Finish implementing a traditional VLM for simulating multiple thin lifting surfaces.
* (DONE) Implement proper stability derivative calculation (i.e. not using finite-differencing).
* (SKIPPING) Perhaps implement a viscous drag buildup on wings from interpolated 2D XFOIL data (a la XFLR5's method for approximation of viscous drag).
* (SKIPPING) Perhaps implement a hybrid ring/horseshoe vortex VLM (a la XFLR5's VLM2) for simulating multiple thin lifting surfaces (hopefully with improved speed and robustness over the VLM1 approach).
* (SKIPPING) Perhaps consider implementing a free-wake compatible VLM model?
* (DONE) Implement an inviscid 3D panel method for simulating multiple objects of arbitrary thickness.
* (IN PROGRESS) Make the aforementioned 3D panel method able to use triangular panels for use with generalized geometries, given prescribed trailing edge stagnation points.
* (IN PROGRESS) Implement a 2.5D coupled viscous/inviscid method directly using the viscous methods described in Drela's paper "Viscous-Inviscid Analysis of Transonic and Low Reynolds Number Airfoils". Inviscid flow would be fully 3D, while viscous flow would make the assumption of negligible spanwise flow (strip theory).
* Implement a fully 3D coupled viscous/inviscid method, compatible with triangular panels. Ideally, the trailing edge stagnation points will be automatically identified, and nothing more than a surface triangulation along with freestream conditions will be required to compute forces and moments.


## Usefulness
AeroSandbox attempts to improve over existing conceptual-level aerodynamics tools. The following strengths and weaknesses are identified with existing tools, based purely off the author's experience:

Strengths:
* XFLR5: Reliability, speed, accuracy, visualization
* AVL: Reliability, speed, accuracy, scriptability
* Tornado: Implementation in a high-level, widely-used language (reduces dev. time and increases flexibility for users)
* VSPAero: Rapid CAD/geometry integration, geometric flexibility

Weaknesses:
* XFLR5: Lack of scriptability, limited geometric flexibility, one-way-coupled viscous analysis
* AVL: Single-precision calculation (low gradient accuracy), bottlenecking due to file I/O, no viscous analysis
* Tornado: Speed, user-friendliness, no viscous analysis
* VSPAero: Robustness, speed, accuracy, and reliability, decoupled viscous analysis
* All tools: None of these tools are capable of reverse-mode automatic differentiation for gradient computations.

With any luck, the list of strengths and weaknesses here will help to drive AeroSandbox development to retain positive qualities and eliminate negative ones. 

Specifically, the following desirable qualities (and associated quantitative metrics) have been identified:
* Fast (for point analysis, VLM calculations should yield a solution (CL, CDi) within 5% of the Richardson-extrapolated solution in less than 1 second for the ExampleAirplanes.conventional() airplane on a typical desktop computer)
* Accurate (in the limit of high panel density, the solution (CL, CDi) given by VLM1 must match AVL or XFLR5 to within 1%)
* Reliable/Robust (gradients of the outputs w.r.t. inputs are always finite and physical)
* User-friendly (eventually, a GUI will be created, and AeroSandbox will optionally ship as a packaged executable)
* Scriptable (the code will be object-oriented; the GUI will contain a CLI)
* Readable (every class and function will be documented; code will be PEP-8-compatible where reasonable)
* Optimizer-friendly (design gradients and stability derivatives will be efficiently computed through automatic differentiation)
* Visualization (visualization will be provided through Plotly's Dash interface)

## Donating
If you like this software, please consider donating to support development via PayPal at [paypal.me/peterdsharpe](https://paypal.me/peterdsharpe)! I'm a poor grad student, so every dollar you donate helps wean me off my diet of instant coffee and microwaved ramen noodles.

## Bugs
Please, please report all bugs by creating a new issue at [https://github.com/peterdsharpe/AeroSandbox/issues](https://github.com/peterdsharpe/AeroSandbox/issues)!

Please note that, while the entirety of the codebase should be cross-platform compatible, AeroSandbox has only been tested on Windows 10 in Python 3.7 via the [Anaconda distribution](https://www.anaconda.com/distribution/#download-section).

## Contributing

Thanks for your interest in helping with the development of AeroSandbox - contributions are always so, so welcome! If you have a change you'd like to make, the easiest way to do that is by submitting a pull request. 

If you've made several additions and would like to be involved in a more long-term capacity, please message me at (pds at mit dot edu) and we can add you as a collaborator here on Github!

Right now, branching is basically nonexistent. This is because there's currently only one contributor - me. As soon as this changes, we'll need to implement [proper branching](https://nvie.com/posts/a-successful-git-branching-model/). 

## License

MIT License

Copyright (c) 2019 Peter Sharpe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

