## Change Log

## Unreleased

-

### Version 2.0.4 (20221203)

Improve dependencies installation instructions.

### Version 2.0.3 (20220706)

Update to latest upstream tag for pyalsa.

### Version 2.0.2 (20210203)

Fix version in `setup.cfg` & `README.md`.

### Version 2.0.1 (20211221)

- Fix crash when starting when J-Station can't be found.
- Fix 0 being interpreted as None for CC events value.

### Version 2.0.0 (20210310)

Migrate to python 3.

### Version 1.0.1 (20170702)

#### User

- Fixed setup script version and categories.

#### Development

- Moved MIDI configuration to MIDI dialog, where it belonged.

### Version 1.0.0 (20170612)

#### User

- Programs bank import and export.
- Program copy / paste.
- Fixed sysex device id not being used.
- Fixed moving a program from the J-Station not being reflected in the UI.

#### Development

- Allow parsing multiple messages from a single sysex buffer.

### Version 0.7.0 (20170610)

#### User

- Persist settings: MIDI in/out ports and import/export folder.
- Fixed digital out level throwing an exception when changing value.
- Minor changes to the UI.

#### Development

- Automatically fill seq_event when building a message from data (this is the
parallel behaviour to how messages are parsed from seq_events or sysex buffers)


### Version 0.6.0 (20170608)

#### User

- Program can be **renamed** from the bank list
- **Import and export** a single program in the same format as J-Edit.
- Human readable value for scales instead of the raw value
- Effect scales adapt their range depending on the selected effect
- Fixed scales not going to their full range
- Fixed incorrect ranges for some parameters

#### Development

- Messages can be built from a sysex buffer, not just seq events.
- Enhanced buffer parsing and building.
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
