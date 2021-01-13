# Visit 2.13.0 log file
ScriptVersion = "2.13.0"
if ScriptVersion != Version():
    print "This script is for VisIt %s. It may not work with version %s" % (ScriptVersion, Version())
visit.ShowAllWindows()
visit.OpenDatabase("test_mesh.vtk", 0)
# The UpdateDBPluginInfo RPC is not supported in the VisIt module so it will not be logged.
visit.AddPlot("Pseudocolor", "ww_n", 1, 1)
visit.DrawPlots()
visit.AddOperator("Isovolume", 1)
IsovolumeAtts = visit.IsovolumeAttributes()
IsovolumeAtts.lbound = -9.9
IsovolumeAtts.ubound = 0.15
IsovolumeAtts.variable = "default"
visit.SetOperatorOptions(IsovolumeAtts, 1)
visit.AddOperator("ExternalSurface", 1)
visit.DrawPlots()
visit.ExportDBAtts = visit.ExportDBAttributes()
ExportDBAtts.allTimes = 0
ExportDBAtts.dirname = "/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/wwig-geoms//tmp-1//vols/"
ExportDBAtts.filename = "0"
ExportDBAtts.timeStateFormat = "_%04d"
ExportDBAtts.db_type = "STL"
ExportDBAtts.db_type_fullname = "STL_1.0"
ExportDBAtts.variables = ("ww_n")
ExportDBAtts.writeUsingGroups = 0
ExportDBAtts.groupSize = 48
ExportDBAtts.opts.types = (0)
ExportDBAtts.opts.help = ""
ExportDatabase(ExportDBAtts)
visit.RemoveAllOperators(1)
visit.AddOperator("Isovolume", 0)
IsovolumeAtts = visit.IsovolumeAttributes()
IsovolumeAtts.lbound = 0.15
IsovolumeAtts.ubound = 0.25
IsovolumeAtts.variable = "default"
visit.SetOperatorOptions(IsovolumeAtts, 0)
visit.AddOperator("ExternalSurface", 0)
visit.DrawPlots()
visit.ExportDBAtts = visit.ExportDBAttributes()
ExportDBAtts.allTimes = 0
ExportDBAtts.dirname = "/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/wwig-geoms//tmp-1//vols/"
ExportDBAtts.filename = "1"
ExportDBAtts.timeStateFormat = "_%04d"
ExportDBAtts.db_type = "STL"
ExportDBAtts.db_type_fullname = "STL_1.0"
ExportDBAtts.variables = ("ww_n")
ExportDBAtts.writeUsingGroups = 0
ExportDBAtts.groupSize = 48
ExportDBAtts.opts.types = (0)
ExportDBAtts.opts.help = ""
ExportDatabase(ExportDBAtts)
visit.RemoveAllOperators(0)
visit.AddOperator("Isovolume", 0)
IsovolumeAtts = visit.IsovolumeAttributes()
IsovolumeAtts.lbound = 0.25
IsovolumeAtts.ubound = 0.35
IsovolumeAtts.variable = "default"
visit.SetOperatorOptions(IsovolumeAtts, 0)
visit.AddOperator("ExternalSurface", 0)
visit.DrawPlots()
visit.ExportDBAtts = visit.ExportDBAttributes()
ExportDBAtts.allTimes = 0
ExportDBAtts.dirname = "/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/wwig-geoms//tmp-1//vols/"
ExportDBAtts.filename = "2"
ExportDBAtts.timeStateFormat = "_%04d"
ExportDBAtts.db_type = "STL"
ExportDBAtts.db_type_fullname = "STL_1.0"
ExportDBAtts.variables = ("ww_n")
ExportDBAtts.writeUsingGroups = 0
ExportDBAtts.groupSize = 48
ExportDBAtts.opts.types = (0)
ExportDBAtts.opts.help = ""
ExportDatabase(ExportDBAtts)
visit.RemoveAllOperators(0)
visit.AddOperator("Isovolume", 0)
IsovolumeAtts = visit.IsovolumeAttributes()
IsovolumeAtts.lbound = 0.35
IsovolumeAtts.ubound = 0.45
IsovolumeAtts.variable = "default"
visit.SetOperatorOptions(IsovolumeAtts, 0)
visit.AddOperator("ExternalSurface", 0)
visit.DrawPlots()
visit.ExportDBAtts = visit.ExportDBAttributes()
ExportDBAtts.allTimes = 0
ExportDBAtts.dirname = "/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/wwig-geoms//tmp-1//vols/"
ExportDBAtts.filename = "3"
ExportDBAtts.timeStateFormat = "_%04d"
ExportDBAtts.db_type = "STL"
ExportDBAtts.db_type_fullname = "STL_1.0"
ExportDBAtts.variables = ("ww_n")
ExportDBAtts.writeUsingGroups = 0
ExportDBAtts.groupSize = 48
ExportDBAtts.opts.types = (0)
ExportDBAtts.opts.help = ""
ExportDatabase(ExportDBAtts)
visit.RemoveAllOperators(0)
visit.AddOperator("Isovolume", 0)
IsovolumeAtts = visit.IsovolumeAttributes()
IsovolumeAtts.lbound = 0.45
IsovolumeAtts.ubound = 10.5
IsovolumeAtts.variable = "default"
visit.SetOperatorOptions(IsovolumeAtts, 0)
visit.AddOperator("ExternalSurface", 0)
visit.DrawPlots()
visit.ExportDBAtts = visit.ExportDBAttributes()
ExportDBAtts.allTimes = 0
ExportDBAtts.dirname = "/home/kkiesling/Pokeball/Documents/CNERG/ww-files/particle-tracking-ww/wwig-geoms//tmp-1//vols/"
ExportDBAtts.filename = "4"
ExportDBAtts.timeStateFormat = "_%04d"
ExportDBAtts.db_type = "STL"
ExportDBAtts.db_type_fullname = "STL_1.0"
ExportDBAtts.variables = ("ww_n")
ExportDBAtts.writeUsingGroups = 0
ExportDBAtts.groupSize = 48
ExportDBAtts.opts.types = (0)
ExportDBAtts.opts.help = ""
ExportDatabase(ExportDBAtts)
visit.RemoveAllOperators(0)
visit.SetActivePlots(0)
visit.DeleteActivePlots()
visit.CloseComputeEngine("Rapidash", "")
