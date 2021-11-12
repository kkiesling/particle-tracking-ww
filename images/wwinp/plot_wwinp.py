import visit as v
import meshio
import sys
import os
import numpy as np
from IsogeomGenerator import driver

global global_max
global global_min


def get_data_names(mf, ratio):
    """get energy group names"""

    # data name
    key_names = mf.cell_data['hexahedron'].keys()
    group_names = []
    mins = []
    maxs = []
    levels = []
    for name in key_names:
        if 'ww' in name:
            group_names.append(name)
            minval = min(mf.cell_data['hexahedron'][name])
            maxval = max(mf.cell_data['hexahedron'][name])
            maxs.append(maxval)
            mins.append(minval)
            lev = driver.generate_levels(ratio, minval, maxval, mode='ratio')
            levels.append(lev)

    return group_names, maxs, mins, levels


def plot_image(group, mins, maxs, levels, ratio):

    v.AddPlot('Pseudocolor', group)

    # Pseudocolor plot options
    att = v.PseudocolorAttributes()
    att.scaling = 1  # log
    att.minFlag = 1  # turn on
    att.min = global_min
    att.maxFlag = 1  # turn on
    att.max = global_max
    att.colorTableName = 'plasma'
    v.SetPlotOptions(att)

    # operator options
    v.AddOperator('Clip')
    att_op = v.ClipAttributes()
    att_op.plane1Status = 0
    att_op.plane2Status = 1
    att_op.plane3Status = 1
    att_op.plane1Origin = (0, 0, 0)
    att_op.plane2Origin = (0, 0, 0)
    att_op.plane3Origin = (0, 0, 0)
    att_op.plane1Normal = (1, 0, 0)
    att_op.plane2Normal = (0, 1, 0)
    att_op.plane3Normal = (0, 0, 1)
    v.SetOperatorOptions(att_op)

    # annotations
    ann = v.AnnotationAttributes()
    ann.userInfoFlag = 0
    ann.databaseInfoFlag = 0
    ann.legendInfoFlag = 1
    ann.axes3D.visible = 0
    ann.axes3D.bboxFlag = 0
    v.SetAnnotationAttributes(ann)

    # view angle and lighting
    vatts = v.View3DAttributes()
    vatts.viewNormal = (-0.3527388964056335, 0.5366103037429186, 0.7665667960976841)
    vatts.viewUp = (0.1151167015834829, 0.8378881066657335, -0.5335650529454227)
    vatts.parallelScale = 346.41
    vatts.nearPlane = -692.82
    vatts.farPlane = 692.82
    vatts.imagePan = (0.08, 0.03)
    vatts.imageZoom = 1.01
    vatts.perspective = 1
    vatts.eyeAngle = 2
    vatts.centerOfRotationSet = 0
    vatts.centerOfRotation = (0, 0, 0)
    vatts.axis3DScaleFlag = 0
    vatts.axis3DScales = (1, 1, 1)
    vatts.shear = (0, 0, 1)
    vatts.windowValid = 0
    v.SetView3D(vatts)

    # make labels
    num = int(group.split('_')[-1])
    annobj = v.CreateAnnotationObject('Text2D')
    annobj.visible = 1
    annobj.active = 1
    annobj.position = (0.055, 0.92)
    annobj.height = 0.02
    annobj.textColor = (0, 0, 0, 255)
    annobj.useForegroundForTextColor = 1
    annobj.text = "Energy Group {}".format(num)
    annobj.fontFamily = 0
    annobj.fontBold = 1
    annobj.fontItalic = 0
    annobj.fontShadow = 0

    # set legend attributes
    objnames = v.GetAnnotationObjectNames()
    for name in objnames:
        if 'Plot' in name:
            legname = name
            break
    legobj = v.GetAnnotationObject(legname)
    legobj.drawTitle = 0
    legobj.drawMinMax = 0
    legobj.numberFormat = "%# -1.3e"
    legobj.fontBold = 0
    legobj.fontHeight = 0.021
    legobj.yScale = 1.5
    legobj.controlTicks = 0
    legobj.minMaxInclusive = 0
    legobj.numTicks = 2
    legobj.suppliedValues = tuple([mins, maxs])
    #legobj.suppliedLabels = tuple(data_vals)

    v.DrawPlots()

    # save fig
    saveatts = v.SaveWindowAttributes()
    saveatts.outputToCurrentDirectory = 1
    saveatts.fileName = group
    saveatts.format = 4  # PNG
    saveatts.screenCapture = 0
    saveatts.resConstraint = 0
    saveatts.width = 3000
    saveatts.height = 3000
    v.SetSaveWindowAttributes(saveatts)
    sname = v.SaveWindow()

    # Add contours
    e = v.AddPlot('Contour', group, 0, 1)
    catt = v.ContourAttributes()
    catt.contourMethod = 1  # values
    catt.contourNLevels = len(levels)
    catt.contourValue = tuple(levels)
    catt.minFlag = 0
    catt.maxFlag = 0
    catt.colorType = 2  # ColorByColorTable
    catt.colorTableName = 'viridis_light'
    catt.invertColorTable = 1
    catt.wireframe = 1
    catt.lineWidth = 6
    catt.lineStyle = 0
    catt.legendFlag = 0
    e = v.SetPlotOptions(catt)

    robj = v.CreateAnnotationObject('Text2D')
    robj.visible = 1
    robj.active = 1
    robj.position = (0.055, 0.39)
    robj.height = 0.015
    robj.textColor = (0, 0, 0, 255)
    robj.useForegroundForTextColor = 1
    robj.text = "Surface Spacing\nRatio = {}".format(ratio)
    robj.fontFamily = 0
    robj.fontBold = 0
    robj.fontItalic = 0
    robj.fontShadow = 0

    e = v.DrawPlots()

    saveatts.fileName = group + '_r{}'.format(ratio)
    v.SetSaveWindowAttributes(saveatts)
    sname = v.SaveWindow()

    v.DeleteAllPlots()

    annobj.visible = 0  # delete annotation object
    robj.visible = 0  # delete annotation object


if __name__ == '__main__':

    f = sys.argv[1]  # expanded_tags.vtk file for wwinp
    ratio = sys.argv[2]  # ratio for plotting contours

    v.LaunchNowin()
    v.OpenDatabase(f)

    mf = meshio.read(f)
    group_names, maxs, mins, levels = get_data_names(mf, ratio)

    annobj = v.CreateAnnotationObject('Text2D')
    annobj.visible = 1
    annobj.active = 1
    annobj.position = (0.055, 0.45)
    annobj.height = 0.015
    annobj.textColor = (0, 0, 0, 255)
    annobj.useForegroundForTextColor = 1
    annobj.text = "Weight Window" + "\n" + "Lower Bound"
    annobj.fontFamily = 0
    annobj.fontBold = 0
    annobj.fontItalic = 0

    global_max = max(maxs)
    global_min = min(mins)

    for i, group in enumerate(group_names):
        plot_image(group, mins[i], maxs[i], levels[i], ratio)

    v.CloseDatabase(f)
