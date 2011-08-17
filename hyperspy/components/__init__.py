# -*- coding: utf-8 -*-
# Copyright © 2007 Francisco Javier de la Peña
#
# This file is part of Hyperspy.
#
# Hyperspy is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hyperspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hyperspy; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  
# USA
'''Components that can be used to define a model

There are some components that are only useful for one particular kind of signal
and therefore their name are preceded by the signal name: eg. eels_cl_edge.

Writing a new template is really easy, just edit _template.py and maybe take a 
look to the other components.
'''
from hyperspy.components.bleasdale import Bleasdale
from hyperspy.components.eels_double_offset import DoubleOffset
from hyperspy.components.eels_double_power_law import DoublePowerLaw
from hyperspy.components.eels_cl_edge import EELSCLEdge
from hyperspy.components.error_function import Erf
from hyperspy.components.exponential import Exponential
from hyperspy.components.fixed_pattern import FixedPattern
from hyperspy.components.gaussian import Gaussian
from hyperspy.components.line import Line
from hyperspy.components.logistic import Logistic
from hyperspy.components.lorentzian import Lorentzian
from hyperspy.components.offset import Offset
from hyperspy.components.parabole import Parabole
from hyperspy.components.power_law import PowerLaw
from hyperspy.components.pes_see import SEE
from hyperspy.components.rc import RC
from hyperspy.components.spline import Spline
from hyperspy.components.eels_vignetting import Vignetting
from hyperspy.components.voigt import Voigt
from hyperspy.components.resizeble_fixed_pattern import ResizebleFixedPattern


