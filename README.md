# Description
**GStation-Edit** is a linux replacement for the Windows based J-Edit software
from Johnson Amplification. J-Edit is an interface for the J-Station guitar /
bass amp modeling and effect processing system.

**GStation-Edit** development started in 2009
[at sourceforge](https://sourceforge.net/projects/gstation-edit/)

# Screenshots
## With default GNOME theme
![Default theme](assets/gstation-edit_default-theme.png)
<br/>
## With dark GNOME theme
![Dark theme](assets/gstation-edit_dark-theme.png)


# Features
- Search the J-Station on the available MIDI ports.
- Load user's bank programs.
- Modify parameters/program from the UI and update the J-Station.
- Modify parameters/program from the J-Station and update the UI.
- Undo or Store changes from the UI.
- Update utility settings (digital output level, cabinet emulation, ...).
- Track changes with a * in the bank list with the same meaning as the LED on
the Store button on the J-Station.


# Not supported yet
- The following items in the program list's context menu: export and import
a program, copy / paste, rename.
- Scale widgets display raw values. Actual units should be displayed instead
(such as dB, ms, etc.)
- Scale widgets will not get to their full range.
- Factory banks are selectable from the J-Station, but will not be reflected
in the UI.
- Only firmware 2.0 is supported. If someone uses firmware 1.0, please contact
me and we could have GStation-Edit compatible with both firmwares.


# How to run GStation-Edit
## Dependencies
Make sure your system includes the following dependencies:
- python-2.7 (Python 3 can't be used due to the dependency on PyAlsa which
is stucked to Python 2)
- GTK 3.16 or higher
- gobject-introspection
- pygobject or python-gobject
- pyalsa or python-alsa

## Runing from source
You can launch GStation-Edit from the download root directory:

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

    # sudo ./setup.py install


# Troubleshooting (WIP)
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
If nothing happens when you launch GStation-Edit (see **How to run
GStation-Edit** above), you probably forgot to install a dependency. 
This should be explicit on the command line if you run GStation-Edit
from source (see **Runing from source** above).
If you get something not that obvious, don't hesitate to drop me a message
with the output from the command line.

#### The main window shows up
The MIDI ports detected by Py-ALSA should display In the comboboxes. 
If the comboboxes are empty, you probably have an issue with your MIDI interface.
Drop me a message with any relevant information if you think your MIDI interface
is properly installed and recognized by the OS.

If you can see the MIDI ports in the comboboxes but the connection fails when
you try to auto-connect:
- Disconnect any other MIDI device
- Try different combinaisons with the MIDI and Sysex channels.
Since I never met this situation, it is possible that GStaton-Edit is not robust
to all cases. Send me a message with the details.
