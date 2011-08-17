# -*- coding: utf-8 -*-
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

import h5py

import numpy as np

from hyperspy import messages

# Plugin characteristics
# ----------------------
format_name = 'HDF5'
description = 'The default file format for Hyperspy based on the HDF5 standard' 

full_suport = False
# Recognised file extension
file_extensions = ['hdf', 'h4', 'hdf4', 'h5', 'hdf5', 'he4', 'he5']
default_extension = 4
# Reading capabilities
reads_images = True
reads_spectrum = True
reads_spectrum_image = True
# Writing capabilities
writes_images = True
writes_spectrum = True
writes_spectrum_image = True

# -----------------------
# File format description
# -----------------------
# The root must contain a group called Experiments
# The experiments group can contain any number of subgroups
# Each subgroup it is an experiment or signal
# Each subgroup must contain at least one dataset called data
# The data is an array of arbitrary dimension
# In addition a number equal to the number of dimensions of the data dataset
# + 1 of empty groups called coordinates followed by a number must exists 
# with the following attributes:
#    'name' 
#    'offset' 
#    'scale' 
#    'units' 
#    'size'
#    'index_in_array' : 1
# The experiment group contains a number of attributes that will be directly 
# assigned as class attributes of the Signal instance. In addition the 
# experiment groups may contain an 'extra_parameters' subgroup that will be 
# assigned to the 'extra_parameters' attribute of the Signal instance as a 
# dictionary
# The Experiments group can contain attributes that may be common to all the 
# experiments and that will be accessible as attribures of the Experiments
# instance

not_valid_format = 'The file is not a valid Hyperspy hdf5 file'

def file_reader(filename, record_by, mode = 'r', driver = 'core', 
                backing_store = False, **kwds):
            
    f = h5py.File(filename, mode = mode, driver = driver)
    # If the file has been created with Hyperspy it should cointain a folder 
    # Experiments.
    experiments = []
    exp_dict_list = []
    if 'Experiments' in f:
        for ds in f['Experiments']:
            if isinstance(f['Experiments'][ds], h5py.Group):
                if 'data' in f['Experiments'][ds]:
                    experiments.append(ds)
        if not experiments:
            f.close()
            raise IOError(not_valid_format)
        # Parse the file
        for experiment in experiments:
            exg = f['Experiments'][experiment]
            exp = {}
            exp['data'] = exg['data'][:]
            axes = []
            for i in xrange(len(exp['data'].shape)):
                try:
                    print('axis-%i' % i)
                    axes.append(dict(exg['axis-%i' % i].attrs))
                except KeyError:
                    f.close()
                    raise IOError(not_valid_format)
            exp['mapped_parameters'] = hdfgroup2dict(
            exg['mapped_parameters'], {})
            exp['original_parameters'] = hdfgroup2dict(
            exg['original_parameters'], {})
            exp['axes'] = axes
            exp_dict_list.append(exp)
    else:
        # Eventually there will be the possibility of loading the datasets of 
        # any hdf5 file
        pass
    f.close()
    return exp_dict_list

def dict2hdfgroup(dictionary, group):
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            dict2hdfgroup(value, group.create_group(key))
        else:
            if value is None:
                value = '_None_'
            try:
                group.attrs[key] = value
            except:
                if type(value) is unicode:
                    try:
                        group.attrs[key] = str(value)
                    except:
                        print("The hdf5 writer could not write the following "
                        "information in the file")
                        print('%s : %s' % (key, value))
                else:
                    print("The hdf5 writer could not write the following "
                    "information in the file")
                    print('%s : %s' % (key, value))
            
def hdfgroup2dict(group, dictionary = {}):
    for key, value in group.attrs.iteritems():
        dictionary[key] = value if value != '_None_' else None
    for _group in group:
        dictionary[_group] = {}
        hdfgroup2dict(group[_group], dictionary[_group])
    return dictionary
                                    
def file_writer(filename, signal, *args, **kwds):
    f = h5py.File(filename, mode = 'w')
    exps = f.create_group('Experiments')
    expg = exps.create_group(signal.mapped_parameters.name)
    expg.create_dataset('data', data = signal.data)
    for axis in signal.axes_manager.axes:
        axis_dict = axis.get_axis_dictionary()
        # For the moment we don't store the slice_bool
        del(axis_dict['slice_bool'])
        coord_group = expg.create_group('axis-%s' % axis.index_in_array)
        dict2hdfgroup(axis_dict, coord_group)
    mapped_par = expg.create_group('mapped_parameters')
    dict2hdfgroup(signal.mapped_parameters._get_parameters_dictionary(), 
                  mapped_par)
    original_par = expg.create_group('original_parameters')
    dict2hdfgroup(signal.original_parameters._get_parameters_dictionary(), 
                  original_par)
    f.close()