# Description
**GStation-Edit** is a linux replacement for the J-Edit software from Johnson
Amplification. J-Edit is an interface for the J-Station guitar / bass amp
modeling and effect processing system.

The J-Station features a dozen of knobs to access the most common parameters.
To get the full potential of the device, it is more convenient to use a computer
based application. The application also allows saving / restoring parameters
to / from files. The manufaturer ships the device with J-Edit, a Windows based
application for that purpose.

Until recently, J-Edit couldn't be used properly on
[Wine](https://www.winehq.org/). In 2009, I started implementing the basic
functions in a Linux application. As of today, all parameters can be accessed
from GStation-Edit and the most important features are available (see the
[feature list below](#features)).

The application communicates with the J-Station over a MIDI connection,
exchanging sysex and CC events. By design, sysex events are proprietary. As a
consequence, most of the development effort was focused on understanding the
exchanges, designing a communication framework and implementing the messages
necessary for the application.

For latest versions, make sure to check the project at
[github](https://github.com/fengalin/gstation-edit). For archeology, you can
check the initial project's page at sourceforge.


# Screenshots
## With default GNOME theme
![Default theme](assets/gstation-edit_default-theme.png)
<br/>
## With dark GNOME theme
![Dark theme](assets/gstation-edit_dark-theme.png)


# <a name='features'></a>Features
- Search the J-Station on the available MIDI ports.
- Load user's bank programs.
- Modify parameters/program from the UI and update the J-Station.
- Modify parameters/program from the J-Station and update the UI.
- Rename a program.
- Undo or Store changes from the UI.
- Import and export a program in the same format as J-Edit.
- Import and export a programs bank in the same format as J-Edit.
- Update utility settings (digital output level, cabinet emulation, ...).
- Track changes with a * in the bank list.


# Not supported yet
- Program copy / paste.
- Factory banks are selectable from the J-Station, but will not be reflected
in the UI.
- Only firmware 2.0 is supported. If someone uses firmware 1.0, please contact
me and we could have GStation-Edit compatible with both firmwares.


# <a name='how_to_run'></a>How to run GStation-Edit
## Dependencies
Make sure your system includes the following dependencies:
- python-2.7 (Python 3 can't be used due to the dependency on PyAlsa which
is stucked to Python 2)
- GTK 3.16 or higher
- gobject-introspection
- pygobject or python-gobject
- pyalsa or python-alsa

## <a name='running_from_source'></a>Running from source
You can launch GStation-Edit from the download root directory (do this if you
face problems as you will get log messages):

    $ ./gstation-edit


## Install
You can install gstation-edit in order to integrate with your DE.
After the installation, there should be a "GStation-Edit" entry in
the Audio and Video menu.
### User install
From the dowload root directory:

    $ ./setup.py install --user

### System wide install
From the dowload root directory:

    $ sudo ./setup.py install


# Troubleshooting
## Could not connect to J-Station
There are many reasons for not being able to connect to J-Station. 
This could range from a simple physical connection to conflicts
with other MIDI devices.

### Check the connection
1. Make sure the MIDI OUT link from the computer is connected to
the MIDI IN port on the J-Station and vice versa.
2. Make sure the MIDI/J8 switch of the J-Station is switched to
the right when looking at the back of the J-Station. The switch must
be vertically aligned with the top mark next to the MIDI IN label.

### Check that the MIDI interface is detected

#### The main window and MIDI select dialog doesn't show up
If nothing happens when you launch GStation-Edit (see [how to run
GStation-Edit](how_to_run) above), you probably forgot to install a dependency.
This should be explicit on the command line if you [run GStation-Edit
from source](#running_from_source).
If you get something not that obvious, drop me a message with the output from
the command line.

#### The main window shows up
The MIDI ports detected by pyALSA should display In the comboboxes.
If the comboboxes are empty, you probably have an issue with your MIDI interface.
Drop me a message with any relevant information if you think your MIDI interface
is properly installed and recognized by the OS.

If you can see the MIDI ports in the comboboxes but the connection fails when
you try to auto-connect:
- Disconnect any other MIDI device
- Try different combinaisons with the MIDI and Sysex channels.
Since I never met this situation, it is possible that GStaton-Edit is not robust
to all cases. Send me a message with the details.
