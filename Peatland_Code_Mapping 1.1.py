#Peatland Code 1.1
#Date: 20200507
#Author: Chris Osborne

import arcpy
import os
import sys
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
arcpy.env.outputZFlag = "Disabled"
#Inputs
Bare_Peat_Input = arcpy.GetParameterAsText(0)
Hags_Input = arcpy.GetParameterAsText(1)
Gullies_Input = arcpy.GetParameterAsText(2)
Grips_Input = arcpy.GetParameterAsText(3)
Non_Peatland = arcpy.GetParameterAsText(4)
Site_Boundary_Input = arcpy.GetParameterAsText(5)
#Output
Output_Peatland_Code = arcpy.GetParameterAsText(6)

#set spatial reference to OSGB
sr = "27700"

#version - will be added to the attributes
version = "1.1"

#Check for bare peat
if Bare_Peat_Input == "":
		arcpy.AddError('ERROR: No bare peat data.')
	
else:	
	#check geometry of bare peat
	arcpy.RepairGeometry_management(Bare_Peat_Input, "DELETE_NULL")

	#create copies before deleting IDs
	Bare_Peat = Output_Peatland_Code [:-4] +"_bp_copy.shp"
	arcpy.CopyFeatures_management(Bare_Peat_Input, Bare_Peat)
	#check for ID field and delete if present
	fields = arcpy.ListFields(Bare_Peat)
	for field in fields:
		if field.name == "ID":
			arcpy.DeleteField_management(Bare_Peat, "ID")
	

#Check for site_bounadary
if Site_Boundary_Input == "":
		arcpy.AddError('ERROR: No site boundary data.')
	
else:	
	#create copies before deleting IDs
	Site_Boundary = Output_Peatland_Code [:-4] +"_sb_copy.shp"
	arcpy.CopyFeatures_management(Site_Boundary_Input, Site_Boundary)
	#check for ID field and delete if present
	fields = arcpy.ListFields(Site_Boundary)
	for field in fields:
		if field.name == "ID":
			arcpy.DeleteField_management(Site_Boundary, "ID")
	

try:
	#define initial outputs - to be merged later
	Output_AEF = Output_Peatland_Code [:-4] + "_AEF.shp"
	Output_AEH = Output_Peatland_Code [:-4] + "_AEH.shp"
	Output_AEG = Output_Peatland_Code [:-4] + "_AEG.shp"
	Output_Drained = Output_Peatland_Code [:-4] + "_Drained.shp"
	Output_Modified = Output_Peatland_Code [:-4] + "_Mod.shp"
	Output_Non_Peatland = Output_Peatland_Code [:-4] + "_NP.shp"

	if Non_Peatland == "":
		arcpy.AddMessage("No non-peatland input.")

	else:
		arcpy.CopyFeatures_management(Non_Peatland, Output_Non_Peatland)
		#check for grid code and area in Non-Peatland
		fields = arcpy.ListFields(Output_Non_Peatland)
		for field in fields:
			if field.name == "ID":
				arcpy.DeleteField_management(Output_Non_Peatland, "ID")
			if field.name == "gridcode":
				arcpy.DeleteField_management(Output_Non_Peatland, "gridcode")
			if field.name == "Area":
				arcpy.DeleteField_management(Output_Non_Peatland, "Area")
			if field.name == "Area_ha":
				arcpy.DeleteField_management(Output_Non_Peatland, "Area_ha")
		arcpy.AddField_management(Output_Non_Peatland, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_Non_Peatland, "gridcode", "6", "PYTHON")
		
		
	#create list for erosion feature (will be used for drained output)
	ef_list = []
	#Check for hags	
	if Hags_Input == "":
		arcpy.AddError('ERROR: No hag data.')
	
	else:	
		Hags = Output_Peatland_Code [:-4] +"_ph_copy.shp"
		arcpy.CopyFeatures_management(Hags_Input, Hags)
		#delete ID column if exists
		fields = arcpy.ListFields(Hags)
		for field in fields:
			if field.name == "ID":
				arcpy.DeleteField_management(Hags, "ID")
		arcpy.AddMessage("Hags shapefile found: " + str(Hags) + "")
		Hags_buffer = Output_Peatland_Code [:-4] + "_hags_buffer.shp"
		arcpy.Buffer_analysis(Hags, Hags_buffer, "30", "FULL", "ROUND", "ALL", "")
		arcpy.DefineProjection_management(Hags_buffer, sr)
		arcpy.RepairGeometry_management(Hags_buffer)
		#check for grid code and area in Hags_buffer
		fields = arcpy.ListFields(Hags_buffer)
		for field in fields:
			if field.name == "gridcode":
				arcpy.DeleteField_management(Hags_buffer, "gridcode")
			if field.name == "Area":
				arcpy.DeleteField_management(Hags_buffer, "Area")
			if field.name == "Area_ha":
				arcpy.DeleteField_management(Hags_buffer, "Area_ha")
		ef_list.append(Hags_buffer)
		
		

	#Check for gullies
	if Gullies_Input == "":
		arcpy.AddError('ERROR: No gully data.')
	
	else:		
		Gullies = Output_Peatland_Code [:-4] +"_gu_copy.shp"
		arcpy.CopyFeatures_management(Gullies_Input, Gullies)
		#delete ID column if exists
		fields = arcpy.ListFields(Gullies)
		for field in fields:
			if field.name == "ID":
				arcpy.DeleteField_management(Gullies, "ID")
		arcpy.AddMessage("Gully shapefile found: " + str(Gullies) + "")
		Gullies_buffer = Output_Peatland_Code [:-4] + "_gullies_buffer.shp"
		arcpy.Buffer_analysis(Gullies, Gullies_buffer, "30", "FULL", "ROUND", "ALL", "")
		arcpy.DefineProjection_management(Gullies_buffer, sr)
		arcpy.RepairGeometry_management(Gullies_buffer)
		#check for grid code and area in Gullies_buffer
		fields = arcpy.ListFields(Gullies_buffer)
		for field in fields:
			if field.name == "gridcode":
				arcpy.DeleteField_management(Gullies_buffer, "gridcode")
			if field.name == "Area":
				arcpy.DeleteField_management(Gullies_buffer, "Area")
			if field.name == "Area_ha":
				arcpy.DeleteField_management(Gullies_buffer, "Area_ha")
		ef_list.append(Gullies_buffer)
		
		
	#Check for grips	
	if Grips_Input == "":
		arcpy.AddMessage("No grip input.")
	
	else:			
		Grips = Output_Peatland_Code [:-4] +"_gr_copy.shp"
		arcpy.CopyFeatures_management(Grips_Input, Grips)
		#delete ID column if exists
		fields = arcpy.ListFields(Grips)
		for field in fields:
			if field.name == "ID":
				arcpy.DeleteField_management(Grips, "ID")
		arcpy.AddMessage("Grips shapefile found: " + str(Grips) + "")
		Grips_buffer = Output_Peatland_Code [:-4] + "_grips_buffer.shp"
		arcpy.Buffer_analysis(Grips, Grips_buffer, "30", "FULL", "ROUND", "ALL", "")
		arcpy.DefineProjection_management(Grips_buffer, sr)
		arcpy.RepairGeometry_management(Grips_buffer)
		#check for grid code and area in Grips_buffer
		fields = arcpy.ListFields(Grips_buffer)
		for field in fields:
			if field.name == "gridcode":
				arcpy.DeleteField_management(Grips_buffer, "gridcode")
			if field.name == "Area":
				arcpy.DeleteField_management(Grips_buffer, "Area")
			if field.name == "Area_ha":
				arcpy.DeleteField_management(Grips_buffer, "Area_ha")
		ef_list.append(Grips_buffer)
		



	#Create Actively Eroding Hag BP shapefile		
	Hags_BP_Buffer = Output_AEH [:-4] + "_HBP_Buffer.shp"
	arcpy.Buffer_analysis(Hags, Hags_BP_Buffer, "1", "FULL", "ROUND", "ALL", "")
	Output_AEH_Clip = Output_AEH [:-4] + "_Clip.shp"
	arcpy.Clip_analysis(Bare_Peat, Hags_BP_Buffer, Output_AEH_Clip)
	Output_AEH_SinglePart = Output_AEH [:-4] + "_Single_Part.shp"
	arcpy.MultipartToSinglepart_management(Output_AEH_Clip, Output_AEH_SinglePart)

	if Non_Peatland == "":
		arcpy.Clip_analysis(Output_AEH_SinglePart, Site_Boundary, Output_AEH)
		arcpy.AddField_management(Output_AEH, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_AEH, "gridcode", "2", "PYTHON")

	else:
		Output_AEH_Clip2 = Output_AEH [:-4] + "_Clip2.shp"
		arcpy.Clip_analysis(Output_AEH_SinglePart, Site_Boundary, Output_AEH_Clip2)
		arcpy.Erase_analysis(Output_AEH_Clip2, Output_Non_Peatland, Output_AEH)
		arcpy.AddField_management(Output_AEH, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_AEH, "gridcode", "2", "PYTHON")
		arcpy.Delete_management(Output_AEH_Clip2)

	#Create Actively Eroding Gully BP shapefile
	Gully_BP_Buffer = Output_AEG [:-4] + "_GBP_Buffer.shp"
	arcpy.Buffer_analysis(Gullies, Gully_BP_Buffer, "2.5", "FULL", "ROUND", "ALL", "")
	Output_AEG_Clip = Output_AEG [:-4] + "_Clip.shp"
	arcpy.Clip_analysis(Bare_Peat, Gully_BP_Buffer, Output_AEG_Clip)
	Output_AEG_SinglePart = Output_AEG [:-4] + "_Single_Part.shp"
	arcpy.MultipartToSinglepart_management(Output_AEG_Clip, Output_AEG_SinglePart)

	if Non_Peatland == "":
		arcpy.Clip_analysis(Output_AEG_SinglePart, Site_Boundary, Output_AEG)
		arcpy.AddField_management(Output_AEG, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_AEG, "gridcode", "3", "PYTHON")
		
	else:	
		Output_AEG_Clip2 = Output_AEG [:-4] + "_Clip2.shp"
		arcpy.Clip_analysis(Output_AEG_SinglePart, Site_Boundary, Output_AEG_Clip2)
		arcpy.Erase_analysis(Output_AEG_Clip2, Output_Non_Peatland, Output_AEG)
		arcpy.AddField_management(Output_AEG, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_AEG, "gridcode", "3", "PYTHON")
		arcpy.Delete_management(Output_AEG_Clip2)

	#Create Actively Eroding Flat BP shapefile
	Actively_Eroding_Merge = Output_AEF [:-4] + "_Merge.shp"
	arcpy.Merge_management([Output_AEH, Output_AEG], Actively_Eroding_Merge)
	Output_AEF_Erase = Output_AEF [:-4] + "_Erase.shp"
	arcpy.Erase_analysis(Bare_Peat, Actively_Eroding_Merge, Output_AEF_Erase)
	#check for grid code and area in Output_AEF_Erase
	fields = arcpy.ListFields(Output_AEF_Erase)
	for field in fields:
		if field.name == "gridcode":
			arcpy.DeleteField_management(Output_AEF_Erase, "gridcode")
		if field.name == "Area":
			arcpy.DeleteField_management(Output_AEF_Erase, "Area")
		if field.name == "Area_ha":
			arcpy.DeleteField_management(Output_AEF_Erase, "Area_ha")

	if Non_Peatland == "":
		arcpy.Clip_analysis(Output_AEF_Erase, Site_Boundary, Output_AEF)
		
	else:	
		Output_AEF_Clip2 = Output_AEF [:-4] + "_Clip2.shp"
		arcpy.Clip_analysis(Output_AEF_Erase, Site_Boundary, Output_AEF_Clip2)
		arcpy.Erase_analysis(Output_AEF_Clip2, Output_Non_Peatland, Output_AEF)
		arcpy.Delete_management(Output_AEF_Clip2)

	#Create Drained shapefile
	Drained_Erase = Output_Drained [:-4] + "_Erase.shp" 
	Erosion_Features_Merge = Output_Peatland_Code [:-4] + "_erosion_f_merge.shp"
	Erosion_Features_Buffer = Output_Peatland_Code [:-4] + "_erosion_f_buffer.shp"
	arcpy.Merge_management(ef_list, Erosion_Features_Merge)
	arcpy.Dissolve_management(Erosion_Features_Merge, Erosion_Features_Buffer, "", "", "MULTI_PART", "")
	arcpy.Erase_analysis(Erosion_Features_Buffer, Bare_Peat, Drained_Erase)
	#check for grid code and area in Drained_Erase
	fields = arcpy.ListFields(Drained_Erase)
	for field in fields:
		if field.name == "gridcode":
			arcpy.DeleteField_management(Drained_Erase, "gridcode")
		if field.name == "Area":
			arcpy.DeleteField_management(Drained_Erase, "Area")
		if field.name == "Area_ha":
			arcpy.DeleteField_management(Drained_Erase, "Area_ha")
	

	if Non_Peatland == "":
		arcpy.Clip_analysis(Drained_Erase, Site_Boundary, Output_Drained)
		arcpy.AddField_management(Output_Drained, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_Drained, "gridcode", "4", "PYTHON")

	else:
		Drained_Clip2 = Output_Drained [:-4] + "_Clip2.shp"
		arcpy.Clip_analysis(Drained_Erase, Site_Boundary, Drained_Clip2)
		arcpy.Erase_analysis(Drained_Clip2, Output_Non_Peatland, Output_Drained)
		arcpy.AddField_management(Output_Drained, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_Drained, "gridcode", "4", "PYTHON")
		arcpy.Delete_management(Drained_Clip2)

	#Create Modified shapefile
	if Non_Peatland == "":	
		Modified1 = Output_Modified [:-4] + "_Erase_Temp.shp"
		arcpy.Erase_analysis(Site_Boundary, Output_Drained, Modified1)
		#check for grid code and area in Modified1
		fields = arcpy.ListFields(Modified1)
		for field in fields:
			if field.name == "ID":
				arcpy.DeleteField_management(Modified1, "ID")
			if field.name == "gridcode":
				arcpy.DeleteField_management(Modified1, "gridcode")
			if field.name == "Area":
				arcpy.DeleteField_management(Modified1, "Area")
			if field.name == "Area_ha":
				arcpy.DeleteField_management(Modified1, "Area_ha")
		arcpy.Erase_analysis(Modified1, Bare_Peat, Output_Modified)
		#check for Id field and add it if does not exist. Required for merge.mod_f_list = arcpy.ListFields(Output_Modified)
		mod_f_list = arcpy.ListFields(Output_Modified)
		for field in mod_f_list:
			if field.name == "ID":
				arcpy.CalculateField_management(Output_Modified, "ID", "1", "PYTHON")
			else:
				arcpy.AddField_management(Output_Modified, "ID", "SHORT", "1", "", "", "", "NON_NULLABLE","REQUIRED","")
				arcpy.CalculateField_management(Output_Modified, "ID", "1", "PYTHON")
			
		arcpy.AddField_management(Output_Modified, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_Modified, "gridcode", "5", "PYTHON")

	else:
		Modified1 = Output_Modified [:-4] + "_Erase_Temp.shp"
		Modified2 = Output_Modified [:-4] + "_Erase_Temp2.shp"
		arcpy.Erase_analysis(Site_Boundary, Output_Drained, Modified1)
		#check for grid code and area in Modified1
		fields = arcpy.ListFields(Modified1)
		for field in fields:
			if field.name == "ID":
				arcpy.DeleteField_management(Modified1, "ID")
			if field.name == "gridcode":
				arcpy.DeleteField_management(Modified1, "gridcode")
			if field.name == "Area":
				arcpy.DeleteField_management(Modified1, "Area")
			if field.name == "Area_ha":
				arcpy.DeleteField_management(Modified1, "Area_ha")
		arcpy.Erase_analysis(Modified1, Output_Non_Peatland, Modified2)
		arcpy.Erase_analysis(Modified2, Bare_Peat, Output_Modified)
		#check for Id field and add it if does not exist. Required for merge.
		mod_f_list = arcpy.ListFields(Output_Modified)
		for field in mod_f_list:
			if field.name == "ID":
				arcpy.CalculateField_management(Output_Modified, "ID", "1", "PYTHON")
			else:
				arcpy.AddField_management(Output_Modified, "ID", "SHORT", "1", "", "", "", "NON_NULLABLE","REQUIRED","")
				arcpy.CalculateField_management(Output_Modified, "ID", "1", "PYTHON")
					
		arcpy.AddField_management(Output_Modified, "gridcode", "LONG", "10", "", "", "gridcode", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_Modified, "gridcode", "5", "PYTHON")
		arcpy.Delete_management(Modified1)
		arcpy.Delete_management(Modified2)

	if Non_Peatland == "":
		arcpy.AddMessage("Merging outputs...")
		Outputs_Merge = Output_Non_Peatland [:-4] + "_Merge.shp"
		Output_Peatland_Code_temp = Output_Peatland_Code [:-4] + "_temp.shp"
		arcpy.Merge_management([Output_AEF, Output_AEH, Output_AEG, Output_Drained, Output_Modified], Outputs_Merge)
		arcpy.Dissolve_management(Outputs_Merge, Output_Peatland_Code_temp, "gridcode", "", "MULTI_PART", "")
		arcpy.AddField_management(Output_Peatland_Code_temp, "Category", "TEXT", "", "", "50", "Category", "NON_NULLABLE", "REQUIRED", "")
		
		arcpy.AddMessage("Reclassifying...")
		expression_gridcode = "Reclass(!gridcode!)"
		codeblock_gc = """def Reclass (gridcode):
		  if gridcode == 0:
			return 'Actively Eroding: Flat bare'
		  elif gridcode == 1:
			return 'Actively Eroding: Flat bare'
		  elif gridcode == 2:
			return 'Actively Eroding: Hagg/Gully'
		  elif gridcode == 3: 
			return 'Actively Eroding: Hagg/Gully'
		  elif gridcode == 4:
			return 'Drained'
		  elif gridcode == 5:
			return 'Modified'"""

		arcpy.CalculateField_management(Output_Peatland_Code_temp, "Category", expression_gridcode, "PYTHON_9.3", codeblock_gc) 
		arcpy.Dissolve_management(Output_Peatland_Code_temp, Output_Peatland_Code, "Category", "", "MULTI_PART", "")
		arcpy.AddField_management(Output_Peatland_Code, "Area_ha", "FLOAT", "", "", "", "Area_ha", "NON_NULLABLE", "REQUIRED", "")
		area_expression = "round(!SHAPE.AREA@HECTARES!,2)"
		arcpy.CalculateField_management(Output_Peatland_Code, "Area_ha", area_expression, "PYTHON")
		arcpy.AddField_management(Output_Peatland_Code, "Version", "FLOAT", "","","","Version", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_Peatland_Code, "Version", version, "PYTHON")
		arcpy.AddMessage("			OUTPUT COMPLETE: Peatland Code = " + str(Output_Peatland_Code) + ".") 
		arcpy.Delete_management(Output_Peatland_Code_temp)

	else:
		arcpy.AddMessage("Merging outputs...")
		Outputs_Merge = Output_Non_Peatland [:-4] + "_Merge.shp"
		Output_Peatland_Code_temp = Output_Peatland_Code [:-4] + "_temp.shp"
		arcpy.Merge_management([Output_AEF, Output_AEH, Output_AEG, Output_Drained, Output_Modified, Output_Non_Peatland], Outputs_Merge)
		arcpy.Dissolve_management(Outputs_Merge, Output_Peatland_Code_temp, "gridcode", "", "MULTI_PART", "") 
		arcpy.AddField_management(Output_Peatland_Code_temp, "Category", "TEXT", "", "", "50", "Category", "NON_NULLABLE", "REQUIRED", "")
		
		expression_gridcode = "Reclass(!gridcode!)"
		codeblock_gc = """def Reclass (gridcode):
		  if gridcode == 0:
			return 'Actively Eroding: Flat bare'
		  elif gridcode == 1:
			return 'Actively Eroding: Flat bare'
		  elif gridcode == 2:
			return 'Actively Eroding: Hagg/Gully'
		  elif gridcode == 3: 
			return 'Actively Eroding: Hagg/Gully'
		  elif gridcode == 4:
			return 'Drained'
		  elif gridcode == 5:
			return 'Modified'
		  elif gridcode == 6:
			return 'Non Peatland'"""

		arcpy.CalculateField_management(Output_Peatland_Code_temp, "Category", expression_gridcode, "PYTHON_9.3", codeblock_gc) 
		arcpy.Dissolve_management(Output_Peatland_Code_temp, Output_Peatland_Code, "Category")
		arcpy.AddField_management(Output_Peatland_Code, "Area_ha", "FLOAT", "", "", "", "Area_ha", "NON_NULLABLE", "REQUIRED", "")
		area_expression_ha = "round(!SHAPE.AREA@HECTARES!,2)"
		arcpy.CalculateField_management(Output_Peatland_Code, "Area_ha", area_expression_ha, "PYTHON")
		arcpy.AddField_management(Output_Peatland_Code, "Version", "FLOAT", "","","","Version", "NON_NULLABLE", "REQUIRED", "")
		arcpy.CalculateField_management(Output_Peatland_Code, "Version", version, "PYTHON")
		arcpy.AddMessage("			OUTPUT COMPLETE: Peatland Code = " + str(Output_Peatland_Code) + ".") 
		arcpy.Delete_management(Output_Peatland_Code_temp)
		 
	
except Exception:
	e = sys.exc_info()[1]
	print(e.args[0])
	arcpy.AddError(e.args[0])
	arcpy.AddWarning("Error occurred.")

finally:
	#check if the data exists, if it does, delete it. 
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_hags_buffer.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_hags_buffer.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_gullies_buffer.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_gullies_buffer.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_grips_buffer.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_grips_buffer.shp")
	if arcpy.Exists(Output_AEH [:-4] + "_HBP_Buffer.shp"):
		arcpy.Delete_management(Output_AEH [:-4] + "_HBP_Buffer.shp")
	if arcpy.Exists(Output_AEG [:-4] + "_GBP_Buffer.shp"):
		arcpy.Delete_management(Output_AEG [:-4] + "_GBP_Buffer.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_Drained.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_Drained.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_Mod.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_Mod.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_AEF.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_AEF.shp")
	if arcpy.Exists(Output_AEF [:-4] + "_Erase.shp"):
		arcpy.Delete_management(Output_AEF [:-4] + "_Erase.shp")
	if arcpy.Exists(Output_Peatland_Code[:-4] + "_Erosion_Features_Buffer.shp"):
		arcpy.Delete_management(Output_Peatland_Code[:-4] + "_Erosion_Features_Buffer.shp")
	if arcpy.Exists(Output_Peatland_Code[:-4] + "_Erosion_Features_Merge.shp"):
		arcpy.Delete_management(Output_Peatland_Code[:-4] + "_Erosion_Features_Merge.shp")
	if arcpy.Exists(Output_AEF [:-4] + "_Merge.shp"):
		arcpy.Delete_management(Output_AEF [:-4] + "_Merge.shp")
	if arcpy.Exists(Output_Non_Peatland [:-4] + "_Merge.shp"):
		arcpy.Delete_management(Output_Non_Peatland [:-4] + "_Merge.shp")
	if arcpy.Exists(Output_Drained [:-4] + "_Erase.shp"):
		arcpy.Delete_management(Output_Drained [:-4] + "_Erase.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_NP.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_NP.shp")
	if arcpy.Exists(Output_AEH [:-4] + "_copy.shp"):
		arcpy.Delete_management(Output_AEH [:-4] + "_copy.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_AEH.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_AEH.shp")
	if arcpy.Exists(Output_AEH [:-4] + "_Buffer.shp"):
		arcpy.Delete_management(Output_AEH [:-4] + "_Buffer.shp")
	if arcpy.Exists(Output_AEH [:-4] + "_Clip.shp"):
		arcpy.Delete_management(Output_AEH [:-4] + "_Clip.shp")
	if arcpy.Exists(Output_AEH [:-4] + "_Single_Part.shp"):
		arcpy.Delete_management(Output_AEH [:-4] + "_Single_Part.shp")
	if arcpy.Exists(Output_AEG [:-4] + "_copy.shp"):
		arcpy.Delete_management(Output_AEG [:-4] + "_copy.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_AEG.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_AEG.shp")
	if arcpy.Exists(Output_AEG [:-4] + "_Buffer.shp"):
		arcpy.Delete_management(Output_AEG [:-4] + "_Buffer.shp")
	if arcpy.Exists(Output_AEG [:-4] + "_Clip.shp"):
		arcpy.Delete_management(Output_AEG [:-4] + "_Clip.shp")
	if arcpy.Exists(Output_AEG [:-4] + "_Single_Part.shp"):
		arcpy.Delete_management(Output_AEG [:-4] + "_Single_Part.shp")
	if arcpy.Exists(Output_AEG [:-4] + "_grips_copy.shp"):
		arcpy.Delete_management(Output_AEG [:-4] + "_grips_copy.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_erosion_f_merge.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_erosion_f_merge.shp")	
	if arcpy.Exists(Output_Peatland_Code [:-4] + "_erosion_f_buffer.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] + "_erosion_f_buffer.shp")	
	if arcpy.Exists(Output_Modified [:-4] + "_Erase_Temp.shp"):
		arcpy.Delete_management(Output_Modified [:-4] + "_Erase_Temp.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] +"_bp_copy.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] +"_bp_copy.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] +"_gu_copy.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] +"_gu_copy.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] +"_ph_copy.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] +"_ph_copy.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] +"_gr_copy.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] +"_gr_copy.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] +"_Mod_Erase_Temp2.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] +"_Mod_Erase_Temp2.shp")
	if arcpy.Exists(Output_Peatland_Code [:-4] +"_sb_copy.shp"):
		arcpy.Delete_management(Output_Peatland_Code [:-4] +"_sb_copy.shp")