Installing Hyperspy
===================

Most users will like to :ref:`install-binary`. At the moment we provide binary installers for Debian/Ubuntu and Windows. If we do not distribute a binary for your platform or installing from binary is not for you it is also very easy to :ref:`install-source` or to    :ref:`install-dev`.


.. _install-binary:
 
Install from a binary
---------------------
.. Note::
    To date there is not any stable release of Hyperspy and therefore no binaries are provided. Currently the only way to get Hyperspy is to :ref:`install-dev`

..
    There are binary distributions for Linux and Windows. In Debian and Ubuntu the dependencies are installed automatically. In Windows there is an experimental bundle installer that includes all the dependencies both for Windows 32 bits and 64 bits.

.. _install-source:

Install from source
-------------------
.. Note::
    To date there is not any stable release of Hyperspy and therefore no tar.gz files are provided. Currently the only way to get Hyperspy is to :ref:`install-dev`



To install from source grab a tar.gz release and in Linux/Mac:

.. code-block:: bash

    $ tar -xzf Hyperspy.tar.gz
    $ cd Hyperspy
    $ python setup.py install

.. _install-dev:

Install the development version
-------------------------------


To get the development version from our mercurial repository you need to install `mercurial <http://mercurial.selenic.com/>`_. Then just do:

.. code-block:: bash

    $ hg clone https://bitbucket.org/Hyperspy

To install Hyperspy you could proceed like in :ref:`install-source`. However, if you are installing from the development version most likely you will prefer to install Hyperspy using  `pip <http://www.pip-installer.org>`_ development mode: 


.. code-block:: bash

    $ cd Hyperspy
    $ pip install -e ./
    
In any case, like when installing from source you must be sure to have all the dependencies installed, see :ref:`install-dependencies`
    
Creating Debian/Ubuntu binaries
-------------------------------

You can create binaries for Debian/Ubuntu running the `release_debian` script

.. code-block:: bash

    ./release_debian
    
.. Warning::

    For this to work, the following packages must be installed in your system python-stdeb, debhelper, dpkg-dev and python-argparser are required.
    
Creating windows binaries
-------------------------
    
To create a Windows binary run the `release_windows.bat` script in a windows machine.

.. _install-dependencies:

Installing the dependencies
---------------------------

If you use a Debian/Ubuntu binary to install Hyperspy all the dependencies should install automatically. Otherwise you must install the following packages: scipy, ipython, matplotlib, numpy, mdp, netcdf4-python, nose and h5py.

The easiest way to install these packages is by installing the `enthough python distribution <http://www.enthought.com/products/epd.php>`_ (EPD) that comes with most Hyperspy dependencies installed by default. When using EPD the only extra package that you will need to install is MDP. If you have an internet connection you can install as follows:

.. code-block:: bash

    easy_install http://sourceforge.net/projects/mdp-toolkit/files/mdp-toolkit/3.1/MDP-3.1.tar.gz/download


.. Warning::
    Hyperspy does not yet support the last version of Ipython 0.11 that is istalled by default in the last EPD release. Therefore, use EPD <= 7.0 to run Hyperspy.

Another option in Windows is to install `pythonxy <http://www.pythonxy.com/>`_.












