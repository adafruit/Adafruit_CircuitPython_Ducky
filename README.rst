Introduction
============


.. image:: https://readthedocs.org/projects/adafruit-circuitpython-ducky/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/ducky/en/latest/
    :alt: Documentation Status


.. image:: https://raw.githubusercontent.com/adafruit/Adafruit_CircuitPython_Bundle/main/badges/adafruit_discord.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/adafruit/Adafruit_CircuitPython_Ducky/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_Ducky/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython library for running DuckyScript

DuckyScript
============
You can find the DuckyScript Documentation `here <https://docs.hak5.org/hak5-usb-rubber-ducky/>`_

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.



Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ducky/>`_.
To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ducky

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ducky

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install adafruit-circuitpython-ducky



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install adafruit_ducky

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

Here is an example of using the Ducky library.
First you will need to import the libraries

.. code-block:: python

    import time
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
    import adafruit_ducky

Once this is done, define the keyboard layout and initialize the `Ducky` object.

.. code-block:: python

    time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems
    keyboard = Keyboard(usb_hid.devices)
    keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)

    duck = adafruit_ducky.Ducky('duckyscript.txt', keyboard, keyboard_layout)

Now, set up a loop which will run a line of the script every time `loop` is called.

.. code-block:: python

    result = True
    while result is not False:
        result = duck.loop()


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/ducky/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_Ducky/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
