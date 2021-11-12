import visit as v
import meshio
import sys
import os
import numpy as np


def get_data_info(mf, extrema):
    """get data name and min/max vals from wwig geom file f

    get minimum non-zero"""
    # data name
    key_names = mf.cell_data['triangle'].keys()
    for name in key_names:
        if 'ww' in name:
            data_name = name
            break

    # min/max data
    max_data = max(mf.cell_data['triangle'][data_name])
    min_data = min(mf.cell_data['triangle'][data_name][
                mf.cell_data['triangle'][data_name][:] > 0])

    if min_data < extrema[0]:
        extrema[0] = min_data
    if max_data > extrema[1]:
        extrema[1] = max_data

    data_vals = sorted(set(mf.cell_data['triangle'][data_name]))[1:]

    return data_name, data_vals, extrema


def plot_image(f, data_name, data_vals, extrema, ratio):

    print(data_name)
    v.OpenDatabase(f)
    v.AddPlot('Pseudocolor', data_name)

    # Pseudocolor plot options
    att = v.PseudocolorAttributes()
    att.scaling = 1  # log
    att.minFlag = 1  # turn on
    att.min = extrema[0]
    att.maxFlag = 1  # turn on
    att.max = extrema[1]
    att.colorTableName = 'viridis_light'
    att.invertColorTable = 1
    v.SetPlotOptions(att)

    # operator options
    v.AddOperator('Clip')
    att_op = v.ClipAttributes()
    att_op.plane1Status = 0
    att_op.plane2Status = 0
    att_op.plane3Status = 1
    att_op.plane1Origin = (0, 0, 0)
    att_op.plane2Origin = (0, 0, 0)
    att_op.plane3Origin = (0, 0, 0)
    att_op.plane1Normal = (1, 0, 0)
    att_op.plane2Normal = (0, 1, 0)
    att_op.plane3Normal = (0, 0, 1)
    v.SetOperatorOptions(att_op)

    v.AddPlot('Mesh', 'mesh')
    matt = v.MeshAttributes()
    matt.legendFlag = 0
    matt.lineWidth = 2
    v.SetPlotOptions(matt)

    # operator options
    v.AddOperator('Clip')
    att_op = v.ClipAttributes()
    att_op.plane1Status = 0
    att_op.plane2Status = 0
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

    # make labels
    num = int(data_name.split('_')[-1])
    annobj = v.CreateAnnotationObject('Text2D')
    annobj.visible = 1
    annobj.active = 1
    annobj.position = (0.055, 0.92)
    annobj.height = 0.02
    annobj.textColor = (0, 0, 0, 255)
    annobj.useForegroundForTextColor = 1
    annobj.text = "Energy Group {}, p = {} cm".format(num, ratio)
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
    legobj.numTicks = len(data_vals)
    legobj.suppliedValues = tuple(data_vals)
    #legobj.suppliedLabels = tuple(data_vals)

    v.DrawPlots()

    # save fig
    saveatts = v.SaveWindowAttributes()
    saveatts.outputToCurrentDirectory = 1
    saveatts.fileName = 'wwig_rough/wwig_s{}_'.format(ratio) + data_name
    saveatts.format = 4  # PNG
    saveatts.screenCapture = 0
    saveatts.resConstraint = 0
    saveatts.width = 3000
    saveatts.height = 3000
    v.SetSaveWindowAttributes(saveatts)
    sname = v.SaveWindow()

    v.DeleteAllPlots()

    annobj.visible = 0  # delete annotation object
    annobj.active = 0  # delete annotation object
    legobj.active = 0

    v.CloseDatabase(f)


if __name__ == '__main__':

    # get file list from directory
    fdir = sys.argv[1]  # decimated viz dir
    rlist = os.listdir(fdir)

    v.LaunchNowin()

    # add this text only one time
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
    annobj.fontShadow = 0

    # get data extrema per energy group
    for e in range(0, 27):
        i = '{:03d}'.format(e)
        print(i)
        min_start = 1e300
        max_start = 0
        extrema = [min_start, max_start]
        vals_dict = {}
        data_names = {}
        for r in rlist:
            factor = float(r)
            fname = r + '/wwn_{}.vtk'.format(i)
            f = fdir + '/' + fname
            mf = meshio.read(f)
            data_name, data_vals, extrema = get_data_info(mf, extrema)
            vals_dict[factor] = data_vals
            data_names[factor] = data_name

        for r in rlist:
            factor = float(r)
            fname = r + '/wwn_{}.vtk'.format(i)
            f = fdir + '/' + fname
            plot_image(f, data_names[factor], vals_dict[factor], extrema, factor)

            # redo #9 because it is weird
            if factor == 0.2:
                plot_image(f, data_names[factor], vals_dict[factor], extrema, factor)
