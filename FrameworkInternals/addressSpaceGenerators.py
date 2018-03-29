#!/usr/bin/env python
# encoding: utf-8
'''
addressSpaceGenerators.py

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
from transformDesign import transformDesignVerbose
asPath = "AddressSpace" + os.path.sep
def generateSourceVariables(projectBinaryDir):
	"""Generates the files SourceVariables.h and SourceVariables.cpp. This method is called automatically by cmake, it does not need to be called by the user."""
	output = os.path.join(projectBinaryDir, "AddressSpace", "include", "SourceVariables.h")
	transformDesignVerbose(asPath + "designToSourceVariablesHeader.xslt", output, 0, astyleRun=True)
	output = os.path.join(projectBinaryDir, "AddressSpace", "src", "SourceVariables.cpp")
	transformDesignVerbose(asPath + "designToSourceVariablesBody.xslt", output,0, astyleRun=True)

def generateASClass(projectBinaryDir, classname):
	"""Generates the files AS<classname>.h and AS<classname>.cpp. This method is called automatically by cmake, it does not need to be called by the user.
	
	Keyword arguments:
	classname -- the name of the device, which this class will be associated to.
	"""
	output = os.path.join(projectBinaryDir, "AddressSpace", "include", "AS{0}.h".format(classname))
	transformDesignVerbose(asPath + "designToClassHeader.xslt", output, 0, astyleRun=True, additionalParam="className=" + classname)
		
	output = os.path.join(projectBinaryDir, "AddressSpace", "src", "AS{0}.cpp".format(classname))	
	transformDesignVerbose(asPath + "designToClassBody.xslt", output, 0, astyleRun=True, additionalParam="className=" + classname)
	
def generateInformationModel(projectBinaryDir):
	"""Generates the files ASInformationModel.h and ASInformationModel.cpp. This method is called automatically by cmake, it does not need to be called by the user."""
	output = os.path.join(projectBinaryDir,"AddressSpace","include","ASInformationModel.h")
	transformDesignVerbose(asPath + "designToInformationModelHeader.xslt", output, 0, astyleRun=True)
	output = os.path.join(projectBinaryDir,"AddressSpace","src","ASInformationModel.cpp")
	transformDesignVerbose(asPath + "designToInformationModelBody.xslt", output, 0, astyleRun=True)
			