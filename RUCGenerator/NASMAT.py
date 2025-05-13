#-----------------------------------------------------------------------------------------
#
#   NASMAT.py
#
#   PURPOSE: Write a *RUC File for NASMAT
#
#   INPUTS:
#       self    structure containing all GUI information
#-----------------------------------------------------------------------------------------
def NASMAT(self):
    # Import Modules
    import os
    import numpy as np
    import shutil
    from tkinter import filedialog

    # Set file
    filename = os.path.join(os.getcwd(),'temp.RUC')

    # Get the Pixel Information
    pixels = self.ruc_image.load()

    # Get the subcell dimensions
    NB = self.ruc_image.width
    NG = self.ruc_image.height
    NB_D = float(self.entry_convx.get())
    NG_D = float(self.entry_convy.get())

    # Set Colors List
    clrs = []
    keys = []
    for key in self.ColorManager.keys():
        clrs.append(self.ColorManager[key])
        keys.append(key)

    # Assign Materials
    mats = np.zeros(shape=(NB,NG))
    for i in range(NB):
        for j in range(NG):
            color = pixels[i,j]
            if color in clrs:
                mats[i,j] = keys[clrs.index(color)]
            else:
                mats[i,j] = keys[clrs.index('Other')]

    # Write the RUC
    fid = open(filename, "w")
    # Write RUC Options
    fid.write('*RUC\n')
    fid.write(f' MOD=202 ARCHID=99\n')

    # Define number of subcells
    fid.write(f' NB={NB} NG={NG}\n')

    # Write Dimensions
    dimX = ' H='
    for i in range(NB):
        dimX = dimX + str(NB_D) + ','
    dimX = dimX[:-1] + "\n"
    fid.write(dimX)

    dimY = ' D='
    for i in range(NG):
        dimY = dimY + str(NG_D) + ','
    dimY = dimY[:-1] + "\n"
    fid.write(dimY)

    # Write materials
    for j in range(NG):
        line = ' SM='
        for i in range(NB):
            line = line + str(mats[i,j]) + ','
        line = line[:-1] + "\n"
        fid.write(line)
    fid.close()

    # Ask User to save
    file_path = None
    while file_path is None:
        file_path = filedialog.asksaveasfilename(
            title="Create a new project file",
            filetypes=(("RUC", "*.ruc"),)
        )

    # Move file
    shutil.move(os.path.join(os.getcwd(),'temp.RUC'),file_path + '.RUC')

    return