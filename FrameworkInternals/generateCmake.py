#!/usr/bin/env python
# encoding: utf-8
'''
generateCmake.py

@author:     Damian Abalo Miron <damian.abalo@cern.ch>
@author:     Piotr Nikiel <piotr@nikiel.info>

@copyright:  2015 CERN

@license:
Copyright (c) 2015, CERN, Universidad de Oviedo.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@contact:    quasar-developers@cern.ch
'''

import os
import sys
import platform
from transformDesign import TransformKeys, transformByKey
from externalToolCheck import subprocessWithImprovedErrors
from commandMap import getCommand
from quasarExceptions import Mistake

def generateCmake(context, buildType="Release"):
	"""Generates CMake header lists in various directories, and then calls cmake.
	
	Keyword arguments:
	buildType -- Optional parameter to specify Debug or Release build. If it is not specified it will default to Release.
	"""	
	if not context['projectSourceDir'] == context['projectBinaryDir']: # out-of-source build
		if os.path.isfile(os.path.join(context['projectSourceDir'], 'CMakeCache.txt')):
			raise Mistake('User mistake? CMakeCache.txt exists in source directory; '+
						  'that will prevent CMake to make a successful out-of-source build. '+
						  'Remove CMakeCache.txt (or attempt "quasar.py clean" and retry') 
		
		
	transformByKey(TransformKeys.AS_CMAKE, {'context':context})
	transformByKey(TransformKeys.D_CMAKE, {'context':context})
	print("Build type ["+buildType+"]")
	projectSourceDir = context['projectSourceDir']
	projectBinaryDir = context['projectBinaryDir']
	if not os.path.isdir(projectBinaryDir):
		print("PROJECT_BINARY_DIR {0} doesn't exist -- creating it.".format(projectBinaryDir))
		os.mkdir(projectBinaryDir)
	os.chdir(projectBinaryDir)

	print("Calling CMake")
	if platform.system() == "Windows":
		subprocessWithImprovedErrors([getCommand("cmake"), "-DCMAKE_BUILD_TYPE=" + buildType,
					      "-G", "Visual Studio 15 2017 Win64", projectSourceDir],
					     getCommand("cmake"))
	elif platform.system() == "Linux":
		subprocessWithImprovedErrors([getCommand("cmake"), "-DCMAKE_BUILD_TYPE=" + buildType,
                                              projectSourceDir],
					     getCommand("cmake"))
