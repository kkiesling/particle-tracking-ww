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
    data = {}
    mins = []
    maxs = []
    for name in key_names:
        if ('ww' in name):
            # and (('003' in name) or ('014' in name) or ('024' in name)):
            data[name] = {}
            minval = min(mf.cell_data['hexahedron'][name])
            maxval = max(mf.cell_data['hexahedron'][name])
            maxs.append(maxval)
            mins.append(minval)
            data[name]['min'] = minval
            data[name]['max'] = maxval
            lev = driver.generate_levels(ratio, minval, maxval, mode='ratio')
            data[name]['levels'] = lev

    return data, maxs, mins


def plot_image(group, mins, maxs, levels, ratio):

    v.AddPlot('Pseudocolor', group, 0, 1)
    v.AddPlot('Pseudocolor', group, 0, 1)
    # second plot is just to have another legend to work with tick marks

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
    v.AddOperator('Clip', 1)
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

    # make labels
    num = int(group.split('_')[-1])
    annobj = v.CreateAnnotationObject('Text2D')
    annobj.visible = 1
    annobj.active = 1
    annobj.position = (0.03, 0.92)
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
    legnames = []
    for name in objnames:
        if 'Plot' in name:
            legnames.append(name)

    # right side ticks - do only min and max if no contours
    tickvals = [mins, maxs]
    legobj = v.GetAnnotationObject(legnames[0])
    legobj.managePosition = 0
    legobj.position = (0.10, 0.9)
    legobj.drawTitle = 0
    legobj.drawMinMax = 0
    legobj.numberFormat = "%# -1.2e"
    legobj.fontBold = 0
    legobj.fontHeight = 0.021
    legobj.yScale = 1.5
    legobj.controlTicks = 0
    legobj.minMaxInclusive = 0
    legobj.numTicks = len(tickvals)
    legobj.suppliedValues = tuple(tickvals)

    # left tick marks
    tickmin = np.around(np.log10(global_min))
    tickmax = np.around(np.log10(global_max))
    numticks = tickmax - tickmin + 1
    tickvals = [
        10**x for x in np.linspace(tickmin, tickmax, numticks, endpoint=True)]
    if tickvals[0] < global_min:
        tickvals = tickvals[1:]
    legobj2 = v.GetAnnotationObject(legnames[1])
    legobj2.managePosition = 0
    legobj2.position = (0.056, 0.9)
    legobj2.orientation = 1
    legobj2.drawTitle = 0
    legobj2.drawMinMax = 0
    legobj2.numberFormat = "%# -.0e"
    legobj2.fontBold = 0
    legobj2.fontHeight = 0.021
    legobj2.yScale = 1.5
    legobj2.controlTicks = 0
    legobj2.minMaxInclusive = 0
    legobj2.numTicks = len(tickvals)
    legobj2.suppliedValues = tuple(tickvals)

    # view angle and lighting
    vatts = v.View3DAttributes()
    vatts.viewNormal = (-0.5, 0.2, 0.6)
    vatts.viewUp = (0, 1, 0)
    vatts.parallelScale = 346.41
    vatts.nearPlane = -692.82
    vatts.farPlane = 692.82
    vatts.imagePan = (0.02, 0)
    vatts.perspective = 1
    vatts.eyeAngle = 2
    vatts.centerOfRotationSet = 0
    vatts.centerOfRotation = (0, 0, 0)
    vatts.axis3DScaleFlag = 0
    vatts.axis3DScales = (1, 1, 1)
    vatts.shear = (0, 0, 1)
    vatts.windowValid = 0
    vatts.imageZoom = 4.5
    v.SetView3D(vatts)

    v.DrawPlots()

    # save fig
    saveatts = v.SaveWindowAttributes()
    saveatts.outputToCurrentDirectory = 1
    saveatts.fileName = 'cwwm/cwwm_' + group
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

    # update the right side with contour tick marks
    legobj = v.GetAnnotationObject(legnames[0])
    legobj.managePosition = 0
    legobj.position = (0.10, 0.9)
    legobj.drawTitle = 0
    legobj.drawMinMax = 0
    legobj.numberFormat = "%# -1.2e"
    legobj.fontBold = 0
    legobj.fontHeight = 0.021
    legobj.yScale = 1.5
    legobj.controlTicks = 0
    legobj.minMaxInclusive = 0
    legobj.numTicks = len(levels)
    legobj.suppliedValues = tuple(levels)

    robj = v.CreateAnnotationObject('Text2D')
    robj.visible = 1
    robj.active = 1
    robj.position = (0.03, 0.39)
    robj.height = 0.015
    robj.textColor = (0, 0, 0, 255)
    robj.useForegroundForTextColor = 1
    robj.text = "Surface Spacing\nRatio = {}".format(ratio)
    robj.fontFamily = 0
    robj.fontBold = 0
    robj.fontItalic = 0
    robj.fontShadow = 0

    e = v.DrawPlots()

    saveatts.fileName = 'cwwm/cwwm_' + group + '_r{}'.format(ratio)
    v.SetSaveWindowAttributes(saveatts)
    sname = v.SaveWindow()

    v.DeleteAllPlots()

    annobj.visible = 0  # delete annotation object
    robj.visible = 0  # delete annotation object


if __name__ == '__main__':

    f = sys.argv[1]  # expanded_tags.vtk file for wwinp

    v.LaunchNowin()
    v.OpenDatabase(f)
    redo = False
    for ratio in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25]:
        mf = meshio.read(f)
        data, maxs, mins = get_data_names(mf, ratio)

        annobj = v.CreateAnnotationObject('Text2D')
        annobj.visible = 1
        annobj.active = 1
        annobj.position = (0.03, 0.45)
        annobj.height = 0.015
        annobj.textColor = (0, 0, 0, 255)
        annobj.useForegroundForTextColor = 1
        annobj.text = "Weight Window" + "\n" + "Lower Bound"
        annobj.fontFamily = 0
        annobj.fontBold = 0
        annobj.fontItalic = 0

        global_max = max(maxs)
        global_min = min(mins)

        for name, info in data.items():
            plot_image(name, info['min'], info['max'], info['levels'], ratio)
            if name == 'ww_n_008' and not redo:
                # redo # 8 because it is weird
                plot_image(name, info['min'], info['max'], info['levels'], ratio)
                redo = True

    v.CloseDatabase(f)
