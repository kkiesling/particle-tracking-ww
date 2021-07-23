import visit as v
import meshio
import sys
import os
import numpy as np


# global min and max
global_min = 1.e300
global_max = 0.


def get_data_info(f):
    """get data name and min/max vals from wwig geom file f

    get minimum non-zero"""
    global global_min
    global global_max

    mf = meshio.read(f)

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

    data_vals = sorted(set(mf.cell_data['triangle'][data_name]))[1:]

    # update global min and max
    if min_data < global_min:
        global_min = min_data
    if max_data > global_max:
        global_max = max_data

    return data_name, max_data, min_data, data_vals


def plot_image(data_name, info):

    # unpack info
    f = info['file']
    data_vals = info['data']

    v.OpenDatabase(f)
    v.AddPlot('Pseudocolor', data_name)

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
    num = int(data_name.split('_')[-1])
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
    legobj.numTicks = len(data_vals)
    legobj.suppliedValues = tuple(data_vals)
    #legobj.suppliedLabels = tuple(data_vals)

    v.DrawPlots()

    # save fig
    saveatts = v.SaveWindowAttributes()
    saveatts.outputToCurrentDirectory = 1
    saveatts.fileName = data_name
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
    fdir = sys.argv[1]
    flist = os.listdir(fdir)

    v.LaunchNowin()

    fdata_list = {}

    for fname in flist:
        f = fdir + '/' + fname
        data_name, max_data, min_data, data_vals = get_data_info(f)
        fdata_list[data_name] = {'file': f, 'min': min_data, 'max': max_data, 'data': data_vals}

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

    for data_name, info in fdata_list.items():
        plot_image(data_name, info)

