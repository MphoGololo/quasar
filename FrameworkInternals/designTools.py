#!/usr/bin/env python
# encoding: utf-8
'''
designTools.py

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
import platform
import shutil
from transformDesign import transformByKey, TransformKeys, getTransformOutput
from externalToolCheck import subprocessWithImprovedErrors
from externalToolCheck import subprocessWithImprovedErrorsPipeOutputToFile
from commandMap import getCommand

designPath = "Design" + os.path.sep
designXML = "Design.xml"
designXSD = "Design.xsd"

def validateDesign(context):
	"""Checks design.xml against Design.xsd, and after that performs some additional checks (defined in designValidation.xslt)"""
	# 1st line of validation -- does it matches its schema?
	# This allows some basic checks
	print("1st line of check -- XSD conformance")
	print("Validating the file " + designXML + " with the schema " + designXSD)
	subprocessWithImprovedErrors([getCommand("xmllint"), "--noout", "--schema", designPath + designXSD, designPath + designXML], getCommand("xmllint"))
	# 2nd line of validation -- including XSLT
	print("2nd line of check -- more advanced checks using XSLT processor")
	transformByKey(TransformKeys.DESIGN_VALIDATION, {'context':context} )

def formatXml(inFileName, outFileName):
	if platform.system() == "Windows":
		subprocessWithImprovedErrorsPipeOutputToFile([getCommand("xmllint"), inFileName], outFileName, getCommand("xmllint"))
	elif platform.system() == "Linux":
		subprocessWithImprovedErrorsPipeOutputToFile([getCommand("xmllint"), "--format", inFileName], outFileName, getCommand("xmllint"))

def formatDesign():
	"""Formats design.xml. This is done to have always the same indentation format. The formatting is done in a separate file, in case something goes wrong, and then copied over."""
	backupName = designXML + ".backup"
	tempName = designXML + ".new"

	print("Creating a backup of " + designXML + " under the name of " + backupName)
	shutil.copyfile(designPath + designXML, designPath + backupName)

	print("Formatting the file " + designXML + "using the tool XMLlint. The result will be saved in " + tempName)
	formatXml(designPath + designXML, designPath + tempName)
		
	print("Copying the formated file  " + tempName + " into the name of " + designXML)
	shutil.copyfile(designPath + tempName, designPath + designXML)
	
def upgradeDesign(additionalParam):
	"""Method for adjusting Design.xml for a new Design.xsd when updating to a new version of the Framework"""
	print("Formatting your design file ...")
	formatDesign()

	transformByKey(TransformKeys.UPGRADE_DESIGN, {'whatToDo':additionalParam})
	
	print("Formatting the upgraded file ")
	upgradedNonFormatted = getTransformOutput(TransformKeys.UPGRADE_DESIGN)
	upgradedFormatted = upgradedNonFormatted + ".formatted"
	
	formatXml(upgradedNonFormatted, upgradedFormatted)
	
	print("Now running merge-tool. Please merge the upgraded changed")
	subprocessWithImprovedErrors([getCommand("diff"), "-o", designPath + designXML, designPath + designXML, upgradedFormatted], getCommand("diff"))
	
def createDiagram(context, detailLevel=0):
	"""Creates an UML diagram based on the classes of the server.
	
	Keyword arguments:
	detailLevel -- Detail level of the diagram. If it is not present, 0 will be assumed
	"""
	if detailLevel == "":
		detailLevel = 0
	transformByKey(TransformKeys.CREATE_DIAGRAM_DOT, {'context': context, 'detailLevel':detailLevel})
	print("Generating pdf diagram with dot.")
	subprocessWithImprovedErrors([getCommand("graphviz"), "-Tpdf", "-o", designPath + "diagram.pdf", getTransformOutput(TransformKeys.CREATE_DIAGRAM_DOT, {'context': context})], "GraphViz (dot)")
			
