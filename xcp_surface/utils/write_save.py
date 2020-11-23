# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Utilities to read and write nifiti and cifti data."""
import nibabel as nb
import numpy as np

def read_ndata(datafile,maskfile=None):
    '''
    read nifti or cifti
    input: 
      datafile:
        nifti or cifti file
    output:
       data:
        numpy ndarry ( vertices or voxels by timepoints)
    '''
    # read cifti series
    if datafile.endswith('.dtseries.nii'):
        data = nb.load(datafile).get_fdata().T
    # or nifiti data, mask is required
    elif datafile.endswith('.nii.gz'):
        datax = nb.load(datafile).get_fdata()
        mask = nb.load(maskfile)
        data = datax[mask==1].T
    return data
    


def write_ndata(data_matrix,template,filename,mask=None):
    '''
    input:
      data matrix : veritices by timepoint 
      template: header and affine
      filename : name of the output
      mask : mask is not needed

    '''

    # write cifti series
    if template.endswith('.dtseries.nii'):
        from nibabel.cifti2 import Cifti2Image
        template_file = nb.load(template)
        dataimg = Cifti2Image(dataobj=data_matrix.T,header=template_file.header,
                    file_map=template_file.file_map,nifti_header=template_file.nifti_header)
    # write nifti series
    elif template.endswith('.nii.gz'):
        mask_data = nb.load(mask).get_fdata()
        template_file = nb.load(template)
        dataz = np.zeros_like([mask_data.shape,data_matrix[1]])
        # this need rewriteen in short format
        for i in range(data_matrix.shape[1]):
            tcbfx = np.zeros(mask_data.shape) 
            tcbfx[mask_data==1] = data_matrix[:,i]
            dataz[:,:,:,i] = tcbfx
        dataimg = nb.Nifti1Image(dataobj=dataz, affine=template_file.affine, 
                 header=template_file.header)
    
    dataimg.to_filename(filename)
    return filename