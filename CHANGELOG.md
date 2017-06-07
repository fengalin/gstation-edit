## Change Log

### Version 0.6.0 (in progress)
#### User
- Editable program names in bank list
- Human readable value for scales instead of the raw value
- Effect scales adapt their range depending on the selected effect
- Fixed scales not going to their full range
- Fixed incorrect ranges for some parameters

#### Development
- Simplified UI signals connection
- Factorized MIDI select dialog for main application and sniffer


### Version 0.5.0 (20170603)
#### User
- Added a **Utility Settings** dialog
- Added Undo and Store buttons
- Added a button to open the MIDI Selection dialog
- Fixed install

#### J-Station interface
- Properly sign off when closing GStation-Edit

#### Development
- Built a new and better **MIDI sniffer** which allows tracing exchanges
between J-Edit (runing in Wine) and the J-Sstation and added it to the project
so I will not loose it again
- Ported to **GTK-3** using GObject
- Reworked project structure and coding style
- Reworked **Messages** framework
- Isolated test suites


### [Previous versions hosted at sourceforge](https://sourceforge.net/projects/gstation-edit/)
#### Version 0.4 - 20120115
- Replaced home made ALSA binding with PYALSA (no longer need to generate
anything, application can be launch directly from the source directory)
- Preparation for Python 3 conformity

#### Version 0.3 - 20091225 (nothing much exciting for those who already run v 0.2)
- Better use of distutils
- Various cleanups

#### Version 0.2 - 20091027
- Added a MIDI port auto-selection feature
- Auto selection of current program upon startup
- Flag to indicate that the program has changed
- Rename from the contextual menu (though nothing applies it to the J-Station
by now)

#### Version 0.1 - 20091021
- Added a MIDI port selection dialogue
- Better includes for py_alsa_seq
- Improved dependencies identification

#### Version 0.0 - 20091017
- First public dump
