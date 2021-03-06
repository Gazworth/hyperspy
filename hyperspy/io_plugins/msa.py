# -*- coding: utf-8 -*-
# Copyright 2007-2011 The Hyperspy developers
#
# This file is part of  Hyperspy.
#
#  Hyperspy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  Hyperspy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  Hyperspy.  If not, see <http://www.gnu.org/licenses/>.

import locale
import time
import datetime

import numpy as np

from hyperspy.misc.config_dir import os_name
from hyperspy.misc.utils import generate_axis
from hyperspy import messages
from hyperspy.misc.utils_varia import overwrite
from hyperspy import Release

# Plugin characteristics
# ----------------------
format_name = 'MSA'
description = ''
full_suport = False
file_extensions = ('msa', 'ems', 'mas', 'emsa', 'EMS', 'MAS', 'EMSA', 'MSA')
default_extension = 0

# Reading features
reads_2d = False
reads_1d = True
reads_3d = False
reads_xd = False
# Writing features
writes_2d = False
writes_1d = True
writes_3d = False
writes_xd = False
# ----------------------

# For a description of the EMSA/MSA format, incluiding the meaning of the 
# following keywords: 
# http://www.amc.anl.gov/ANLSoftwareLibrary/02-MMSLib/XEDS/EMMFF/EMMFF.IBM/Emmff.Total
keywords = {    
                # Required parameters
                'FORMAT' : {'dtype' : str, 'mapped_to': None},
                'VERSION' : {'dtype' : str, 'mapped_to': None},
                'TITLE' : {'dtype' : str, 'mapped_to': None},
                'DATE' : {'dtype' : str, 'mapped_to': None},     
                'TIME' : {'dtype' : str, 'mapped_to': None},
                'OWNER' : {'dtype' : str, 'mapped_to': None},
                'NPOINTS' : {'dtype' : float, 'mapped_to': None},
                'NCOLUMNS' : {'dtype' : float, 'mapped_to': None},
                'DATATYPE' : {'dtype' : str, 'mapped_to': None},
                'XPERCHAN' : {'dtype' : float, 'mapped_to': None},
                'OFFSET' : {'dtype' : float, 'mapped_to': None},
                # Optional parameters
                ## Spectrum characteristics
                'SIGNALTYPE' : {'dtype' : str, 'mapped_to': 'signal'},
                'XLABEL' : {'dtype' : str, 'mapped_to': None},
                'YLABEL' : {'dtype' : str, 'mapped_to': None},
                'XUNITS' : {'dtype' : str, 'mapped_to': None},
                'YUNITS' : {'dtype' : str, 'mapped_to': None},
                'CHOFFSET' : {'dtype' : float, 'mapped_to': None},
                'COMMENT' : {'dtype' : str, 'mapped_to': None},
                ## Microscope
                'BEAMKV' : {'dtype' : float, 'mapped_to': 'beam_energy'},
                'EMISSION' : {'dtype' : float, 'mapped_to': None},
                'PROBECUR' : {'dtype' : float, 'mapped_to': None},
                'BEAMDIAM' : {'dtype' : float, 'mapped_to': None},
                'MAGCAM' : {'dtype' : float, 'mapped_to': None},
                'OPERMODE' : {'dtype' : str, 'mapped_to': None},
                'CONVANGLE' : {'dtype' : float, 'mapped_to': None},
                
                ## Specimen
                'THICKNESS' : {'dtype' : float, 'mapped_to': None},
                'XTILTSTGE' : {'dtype' : float, 'mapped_to': None},
                'YTILTSTGE' : {'dtype' : float, 'mapped_to': None},
                'XPOSITION' : {'dtype' : float, 'mapped_to': None},
                'YPOSITION' : {'dtype' : float, 'mapped_to': None},
                'ZPOSITION' : {'dtype' : float, 'mapped_to': None},
                
                ## EELS
                'INTEGTIME' : {'dtype' : float, 'mapped_to': None}, # in ms
                'DWELLTIME' : {'dtype' : float, 'mapped_to': None}, # in ms
                'COLLANGLE' : {'dtype' : float, 'mapped_to': None},
                'ELSDET' :  {'dtype' : str, 'mapped_to': None},

                ## EDS
                'ELEVANGLE' : {'dtype' : float, 'mapped_to': None},
                'AZIMANGLE' : {'dtype' : float, 'mapped_to': None},
                'SOLIDANGLE' : {'dtype' : float, 'mapped_to': None},
                'LIVETIME' : {'dtype' : float, 'mapped_to': None},
                'REALTIME' : {'dtype' : float, 'mapped_to': None},
                'TBEWIND' : {'dtype' : float, 'mapped_to': None},
                'TAUWIND' : {'dtype' : float, 'mapped_to': None},
                'TDEADLYR' : {'dtype' : float, 'mapped_to': None},
                'TACTLYR' : {'dtype' : float, 'mapped_to': None},
                'TALWIND' : {'dtype' : float, 'mapped_to': None},
                'TPYWIND' : {'dtype' : float, 'mapped_to': None},
                'TBNWIND' : {'dtype' : float, 'mapped_to': None},
                'TDIWIND' : {'dtype' : float, 'mapped_to': None},
                'THCWIND' : {'dtype' : float, 'mapped_to': None},
                'EDSDET'  : {'dtype' : str, 'mapped_to': None},	
            }
def file_reader(filename, **kwds):
    parameters = {}
    mapped = {}
    spectrum_file = open(filename)


    y = []
    # Read the keywords
    data_section = False
    for line in spectrum_file.readlines():
        if data_section is False:
            if line[0] == "#":
                key,value = line.split(': ')
                key = key.strip('#').strip()
                value = value.strip()
                
                if key != 'SPECTRUM':
                    parameters[key] = value
                else:
                    data_section = True
        else:
            # Read the data
            if line[0] != "#" and line.strip(): 
                if parameters['DATATYPE'] == 'XY':
                    xy = line.replace(',', ' ').strip().split()
                    y.append(float(xy[1]))
                elif parameters['DATATYPE'] == 'Y':
                    data = [
                    float(i) for i in line.replace(',', ' ').strip().split()]
                    y.extend(data)
    # We rewrite the format value to be sure that it complies with the 
    # standard, because it will be used by the writer routine
    parameters['FORMAT'] = "EMSA/MAS Spectral Data File"
    
    # Convert the parameters to the right type and map some
    # TODO: the msa format seems to support specifying the units of some 
    # parametes. We should add this feature here
    for parameter, value in parameters.iteritems():
        # Some parameters names can contain the units information
        # e.g. #AZIMANGLE-dg: 90.
        if '-' in parameter:
            clean_par, units = parameter.split('-')
            clean_par, units = clean_par.strip(), units.strip()
        else:
            clean_par, units = parameter, None
        if clean_par in keywords:
            try:
                parameters[parameter] = keywords[clean_par]['dtype'](value)
            except:
                # Normally the offending mispelling is a space in the scientic
                # notation, e.g. 2.0 E-06, so we try to correct for it
                try:
                    parameters[parameter] = keywords[clean_par]['dtype'](
                    value.replace(' ', ''))
                except:
                    print("The %s keyword value, %s " % (parameter, value) +
                    "could not be converted to the right type" )
                
            if keywords[clean_par]['mapped_to'] is not None:
                mapped[keywords[clean_par]['mapped_to']] = parameters[parameter]
                if units is not None:
                    mapped[keywords[clean_par]['mapped_to']+'_units'] = units
                
    # The data parameter needs some extra care
    # It is necessary to change the locale to US english to read the date
    # keyword            
    loc = locale.getlocale(locale.LC_TIME)
    
    if os_name == 'posix':
        locale.setlocale(locale.LC_TIME, ('en_US', 'UTF8'))
    elif os_name == 'windows':
        locale.setlocale(locale.LC_TIME, 'english')
    try:
        H, M = time.strptime(parameters['TIME'], "%H:%M")[3:5]
        mapped['time'] = datetime.time(H, M)
    except:
        print('The time information could not be retrieved')
    try:    
        Y, M, D = time.strptime(parameters['DATE'], "%d-%b-%Y")[0:3]
        mapped['date'] = datetime.date(Y, M, D)
    except:
        print('The date information could not be retrieved')

    locale.setlocale(locale.LC_TIME, loc) # restore saved locale

    axes = []

    axes.append({
            'size' : len(y), 
            'index_in_array' : 0,
            'name' : parameters['XLABEL'] if 'XLABEL' in parameters else '', 
            'scale': parameters['XPERCHAN'] if 'XPERCHAN' in parameters else 1,
            'offset' : parameters['OFFSET'] if 'OFFSET' in parameters else 0,
            'units' : parameters['XUNITS'] if 'XUNITS' in parameters else '',
                })

    mapped['original_filename'] = filename
    mapped['record_by']='spectrum'
    if 'signal_type' in mapped:
        if mapped['signal_type'] == 'ELS':
            mapped['signal_type'] = 'EELS'
    else:
        # Defaulting to EELS looks reasonable
        mapped['signal_type'] = 'EELS'

    dictionary = {
                    'data' : np.array(y),
                    'axes' : axes,
                    'mapped_parameters': mapped,
                    'original_parameters' : parameters
                }
    return [dictionary,]

def file_writer(filename, signal, format = None, separator = ', '):
    keywords = {}
    FORMAT = "EMSA/MAS Spectral Data File"
    if hasattr(signal.original_parameters, 'FORMAT') and \
    signal.original_parameters.FORMAT == FORMAT:
        keywords = signal.original_parameters.as_dictionary()
        if format is not None:
            keywords['DATATYPE'] = format
        else:
            if 'DATATYPE' in keywords:
                format = keywords['DATATYPE']
    else:
        if format is None:
            format = 'Y'
        if hasattr(signal.mapped_parameters, "date"):
            loc = locale.getlocale(locale.LC_TIME)
            if os_name == 'posix':
                locale.setlocale(locale.LC_TIME, ('en_US', 'UTF8'))
            elif os_name == 'windows':
                locale.setlocale(locale.LC_TIME, 'english')
            keywords['DATE'] = signal.mapped_parameters.data.strftime("%d-%b-%Y")
            locale.setlocale(locale.LC_TIME, loc) # restore saved locale
            
    keys_from_signal = {
        # Required parameters
        'FORMAT' : FORMAT,
        'VERSION' : '1.0',
        'TITLE' : signal.title[:64] if hasattr(signal, "title") else '',
        'DATA' : '',
        'TIME' : '',
        'OWNER' : '',
        'NPOINTS' : signal.axes_manager.axes[0].size,
        'NCOLUMNS' : 1,
        'DATATYPE' : format,
        'XPERCHAN' : signal.axes_manager.axes[0].scale,
        'OFFSET' : signal.axes_manager.axes[0].offset,
        ## Spectrum characteristics

        'XLABEL' : signal.axes_manager.axes[0].name,
#        'YLABEL' : '',
        'XUNITS' : signal.axes_manager.axes[0].units,
#        'YUNITS' : '',
        'COMMENT' : 'File created by Hyperspy version %s' % Release.version,
#        ## Microscope
#        'BEAMKV' : ,
#        'EMISSION' : ,
#        'PROBECUR' : ,
#        'BEAMDIAM' : ,
#        'MAGCAM' : ,
#        'OPERMODE' : ,
#        'CONVANGLE' : ,
#        ## Specimen
#        'THICKNESS' : ,
#        'XTILTSTGE' : ,
#        'YTILTSTGE' : ,
#        'XPOSITION' : ,
#        'YPOSITION' : ,
#        'ZPOSITION' : ,
#        
#        ## EELS
#        'INTEGTIME' : , # in ms
#        'DWELLTIME' : , # in ms
#        'COLLANGLE' : ,
#        'ELSDET' :  ,                     
    }
    
    # Update the keywords with the information retrieved from the signal class
    for key, value in keys_from_signal.iteritems():
        if key not in keywords or value != '':
            keywords[key] = value

    f = open(filename, 'w')   
    # Remove the following keys from keywords if they are in 
    # (although they shouldn't)
    for key in ['SPECTRUM', 'ENDOFDATA']:
        if key in keywords: del(keywords[key])
    
    f.write(u'#%-12s: %s\u000D\u000A' % ('FORMAT', keywords.pop('FORMAT')))
    f.write(u'#%-12s: %s\u000D\u000A' % ('VERSION', keywords.pop('VERSION')))
    for keyword, value in keywords.items():
        f.write(u'#%-12s: %s\u000D\u000A' % (keyword, value))
    
    f.write(u'#%-12s: Spectral Data Starts Here\u000D\u000A' % 'SPECTRUM')

    if format == 'XY':        
        for x,y in zip(signal.axes_manager.axes[0].axis, signal.data):
            f.write("%g%s%g" % (x, separator, y))
            f.write(u'\u000D\u000A')
    elif format == 'Y':
        for y in signal.data:
            f.write('%f%s' % (y, separator))
            f.write(u'\u000D\u000A')
    else:
        raise ValueError('format must be one of: None, \'XY\' or \'Y\'')

    f.write(u'#%-12s: End Of Data and File' % 'ENDOFDATA')
    f.close()   

