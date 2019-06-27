from AeroSandbox import *

# Slightly modified from original geometry by moving both the horizontal tail and vertical stabilizer up 0.1m. This was to ensure that there was no wake interference from the main wing. This has been reflected in the associated .xfl file.

a = Airplane(
        name="XFLR Default",
        xyz_ref=[0, 0, 0],
        wings=[
            Wing(
                name="Main Wing",
                xyz_le=[0, 0, 0],
                symmetric=True,
                vlm_chordwise_panels=13,
                sections=[
                    WingSection(  # Root
                        xyz_le=[0, 0, 0],
                        chord=0.18,
                        twist=0,
                        airfoil=Airfoil(name="naca0012"),
                        vlm_spanwise_panels=19,
                    ),
                    WingSection(  # Tip
                        xyz_le=[0.07, 1, 0],
                        chord=0.11,
                        twist=0,
                        airfoil=Airfoil(name="naca0012")
                    )
                ]
            ),
            Wing(
                name="Horizontal Stabilizer",
                xyz_le=[0.6, 0, 0.1],
                symmetric=True,
                vlm_chordwise_panels=7,
                sections=[
                    WingSection(  # root
                        xyz_le=[0, 0, 0],
                        chord=0.1,
                        twist=0,
                        airfoil=Airfoil(name="naca0012"),
                        vlm_spanwise_panels=7,
                    ),
                    WingSection(  # tip
                        xyz_le=[0.02, 0.17, 0],
                        chord=0.08,
                        twist=0,
                        airfoil=Airfoil(name="naca0012")
                    )
                ]
            ),
            Wing(
                name="Vertical Stabilizer",
                xyz_le=[0.65, 0, 0.1],
                symmetric=False,
                vlm_chordwise_panels=7,
                sections=[
                    WingSection(
                        xyz_le=[0, 0, 0],
                        chord=0.1,
                        twist=0,
                        airfoil=Airfoil(name="naca0012"),
                        vlm_spanwise_panels=7,
                    ),
                    WingSection(
                        xyz_le=[0.04, 0, 0.12],
                        chord=0.06,
                        twist=0,
                        airfoil=Airfoil(name="naca0012")
                    )
                ]
            )
        ]
    )
a.set_ref_dims_from_wing()

ap = vlm1(
    airplane=a,
    op_point=OperatingPoint(velocity=10,
                            alpha=5,
                            beta=0),
)
ap.run()
ap.draw()

# Answer you should get: (XFLR5)
# CL = 0.490
# CDi = 0.006
# CL/CDi = 83.250
# Cm = -0.322