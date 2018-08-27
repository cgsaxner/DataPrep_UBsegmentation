# ------------------------------------------------------------

# 
#  \file    DataPreperation.py
#  \author  Christina
#  \date    2017-05-09
#
#  Prepares PET and CT Data for Deep Learning

# ------------------------------------------------------------

from mevis import *
import os
import numpy as np


def setThreshold():
  maxSUV = ctx.field("InfoPET.maxValue").value
  ctx.field("Threshold.threshold").value = maxSUV * ctx.field("ThresholdRatio").value
  pass

def setWindow():
  minval = ctx.field("InfoCT.minValue").value
  maxval = ctx.field("InfoCT.maxValue").value
  range = abs(minval) + maxval
  factor = 65535 / range
  ctx.field("Window.windowCenter").value = factor * 2800
  pass
    
def getSlices():
  if ctx.field("exportAllSlices").value == True:
    startSlice = 0
    endSlice = ctx.field("InfoCT.sizeZ").value
  else:
    startSlice = ctx.field("startSlice").value
    endSlice = ctx.field("endSlice").value
  return startSlice, endSlice
  
  
def getRotationAngles():
  if ctx.field("rotation").value == True:
    angles = np.linspace(-ctx.field("maxAngle").value, ctx.field("maxAngle").value, ctx.field("numAngles").value, endpoint = True)
  else:
    angles = np.linspace(0, 1, 1, endpoint = False)
  return angles

def getScales():
  if ctx.field("scaling").value == True:
    scalesX = np.linspace((1 - ctx.field("scaleRange").value), (1 + ctx.field("scaleRange").value), ctx.field("numScalesX").value, endpoint = True)
    scalesY = np.linspace((1 - ctx.field("scaleRange").value), (1 + ctx.field("scaleRange").value), ctx.field("numScalesY").value, endpoint = True)
  else:
    scalesX = np.linspace(1, 1, 1, endpoint = False)
    scalesY = np.linspace(1, 1, 1, endpoint = False)
  return scalesX, scalesY

def getNoiseLevels():
  if ctx.field("addNoise").value == True:
    noiseType = ctx.field("noiseType").value
    if noiseType == "Uniform":
      noise = np.linspace(0, ctx.field("maxAmplitude").value, ctx.field("noiseSlices").value)
    elif noiseType == "Gaussian":
      noise = np.linspace(0, ctx.field("maxSigma").value, ctx.field("noiseSlices").value)
    elif noiseType == "SaltPepper":
      noise = np.linspace(0, ctx.field("maxDensity").value, ctx.field("noiseSlices").value)
  else:
    noise = np.linspace(0, 1, 1, endpoint = False)
    noiseType = "none"
  return noise, noiseType

def setProgress(p):
  ctx.field("progress").value = p

def getExportPathImage():
  return ctx.field("exportPathImage").value

def getExportPathLabel():
  return ctx.field("exportPathLabel").value

def getExportFileName():
  return ctx.field("exportFileName").value

def switchNoiseType():
  noiseType = ctx.field("noiseType").value
  selectTabAt = 0
  if noiseType == "Uniform":    
    selectTabAt = 0
  elif noiseType == "Gaussian":
    selectTabAt = 1
  elif noiseType == "SaltPepper":
    selectTabAt = 2
  ctx.control("paraTabView").selectTabAtIndex(selectTabAt)
  return

def calcSliceNumber():
  startSlice, endSlice = getSlices()
  inputSlices = endSlice - startSlice
  if ctx.field("rotation").value == True:
    rotations = ctx.field("numAngles").value
  else:
    rotations = 1
  if ctx.field("scaling").value == True:
    scalesX = ctx.field("numScalesX").value
    scalesY = ctx.field("numScalesY").value
  else:
    scalesX = 1
    scalesY = 1
  if ctx.field("addNoise").value == True:
    noiseSlices = ctx.field("noiseSlices").value
  else:
    noiseSlices = 1
  SliceNumber = inputSlices * rotations * scalesX * scalesY * noiseSlices
  ctx.field("totalSlices").value = SliceNumber
  
def augmentAndSafe(name, exportPath, exportFileName, i):
  angles = getRotationAngles()
  scalesX, scalesY = getScales()
  noise, noiseType = getNoiseLevels()
  for r in angles:
    for x in scalesX:
      for y in scalesY:
        for n in noise:
          ctx.field("AffineTransformation2D" + name + ".rotation").value = r * 3.14159265359 / 180
          ctx.field("AffineTransformation2D" + name + ".scalingX").value = x
          ctx.field("AffineTransformation2D" + name + ".scalingY").value = y
          if noiseType == "Uniform":
            ctx.field("AddNoise.amplitude").value = n
          elif noiseType == "Gaussian":
            ctx.field("AddNoise.sigma").value = n
          elif noiseType == "SaltPepper": 
            ctx.field("AddNoise.density").value = n
          elif noiseType == "none":
            ctx.field("AddNoise.amplitude").value = 0
            ctx.field("AddNoise.sigma").value = 0
            ctx.field("AddNoise.density").value = 0
          completeFileName = os.path.join(exportPath, exportFileName + str(i) + "_" + "angle" + str(round(r, 2)) + "_scale" + str(round(x, 2)) + "_" + str(round(y, 2)) + "_noise_" + noiseType + str(round(n, 2)) + name + ".tiff")
          ctx.field("ImageSave" + name + ".filename").value = completeFileName
          ctx.field("SubImage" + name + ".z").value = i
          ctx.field("ImageSave" + name + ".startTaskSynchronous").touch()
  
def exportCT(field):
  exportPath = getExportPathImage()
  startSlice, endSlice = getSlices()
  numSlices = endSlice - startSlice
  setProgress(0)
  if os.path.exists(exportPath) and os.path.isdir(exportPath):
    exportFileName = getExportFileName()    
    for i in range(startSlice, endSlice):  
      augmentAndSafe("CT", exportPath, exportFileName, i) 
      setProgress(float(i)/float(ctx.field("totalSlices").value))
    setProgress(1)
  else:
    print "Directory does not exists", exportPath  
    
def exportPET(field):
  exportPath = getExportPathLabel()
  startSlice, endSlice = getSlices()
  numSlices = endSlice - startSlice
  setProgress(0)
  if os.path.exists(exportPath) and os.path.isdir(exportPath):
    exportFileName = getExportFileName()
    for i in range(startSlice, endSlice):
      augmentAndSafe("PET", exportPath, exportFileName, i) 
      setProgress(float(i)/float(ctx.field("totalSlices").value))
    setProgress(1)
  else:
    print "Directory does not exists", exportPath  



  

  