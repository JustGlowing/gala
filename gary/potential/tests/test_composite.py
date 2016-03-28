# coding: utf-8

from __future__ import absolute_import, unicode_literals, division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Third party
import pytest
import numpy as np

# This project
from ...integrate import LeapfrogIntegrator, DOPRI853Integrator
from ..core import *
from ..builtin import *
from ...units import solarsystem

class CompositeHelper(object):

    def setup(self):
        self.units = solarsystem
        self.p1 = KeplerPotential(m=1.*u.Msun, units=self.units)
        self.p2 = HernquistPotential(m=0.5*u.Msun, c=0.1*u.au,
                                     units=self.units)

    def test_shit(self):
        potential = self.Cls(one=self.p1, two=self.p2)

        q = np.ascontiguousarray(np.array([[1.1,0,0]]).T)
        print("val", potential.value(q))

        q = np.ascontiguousarray(np.array([[1.1,0,0]]).T)
        print("grad", potential.gradient(q))

    def test_composite_create(self):
        potential = self.Cls()

        # Add a point mass with same unit system
        potential["one"] = KeplerPotential(units=self.units, m=1.)

        with pytest.raises(TypeError):
            potential["two"] = "derp"

        assert "one" in potential.parameters
        assert "m" in potential.parameters["one"]
        with pytest.raises(TypeError):
            potential.parameters["m"] = "derp"

    def test_plot_composite(self):
        potential = self.Cls()

        # Add a kepler potential and a harmonic oscillator
        potential["one"] = self.p1
        potential["two"] = self.p2

        grid = np.linspace(-5.,5)
        fig = potential.plot_contours(grid=(grid,0.,0.))
        # fig.savefig(os.path.join(plot_path, "composite_kepler_sho_1d.png"))

        fig = potential.plot_contours(grid=(grid,grid,0.))
        # fig.savefig(os.path.join(plot_path, "composite_kepler_sho_2d.png"))

    def test_integrate(self):
        potential = self.Cls()
        potential["one"] = self.p1
        potential["two"] = self.p2

        w = potential.integrate_orbit([1.,0,0, 0,2*np.pi,0], dt=0.01, nsteps=1000,
                                      Integrator=DOPRI853Integrator, cython_if_possible=True)
        print(w.pos[0])
        fig = w.plot()
        fig.suptitle(self.__class__.__name__)

# ------------------------------------------------------------------------

class TestComposite(CompositeHelper):
    Cls = CompositePotential

class TestCComposite(CompositeHelper):
    Cls = CCompositePotential


def test_uh():
    import matplotlib.pyplot as pl
    pl.show()
