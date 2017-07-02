# this file is part of gstation-edit
# Copyright (C) F LAIGNEL 2009-2017 <fengalin@free.fr>
#
# gstation-edit is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gstation-edit is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

VERSION='1.0.1'

from distutils.core import setup, Extension

setup(  name='gstation-edit',
        version=VERSION,
        description='GTK replacement for Johnson J-Station J-Edit.',
        author='F Laignel',
        author_email='fengalin@free.fr',
        url='http://sourceforge.net/projects/gstation-edit/',
        license='GNU General Public License version 3.0 (GPLv3)',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: X11 Applications :: GTK',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Operating System :: Unix',
            'Programming Language :: Python :: 2',
            'Topic :: Multimedia :: Sound/Audio',
            'Natural Language :: English',
            ],
        packages=["gstation_edit", "gstation_edit.messages",
                  "gstation_edit.midi", "gstation_edit.rack",
                  "gstation_edit.ui_core"],
        package_dir={"gstation_edit": "gstation_edit"},
        scripts = ['gstation-edit'],
        data_files=[('share/gstation-edit', ['README.md', 'CHANGELOG.md',
                     'LICENSE',
                     "gstation_edit/resources/gstation-edit-one-window.ui"]),
                    ('share/applications', ['gstation-edit.desktop'])]
  )
