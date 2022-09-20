# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Functions for resampling CIFTI files."""

from nipype import logging
from nipype.interfaces.base import CommandLineInputSpec, File, TraitedSpec, traits
from nipype.interfaces.workbench.base import WBCommand

iflogger = logging.getLogger("nipype.interface")


class _CiftiSurfaceResampleInputSpec(CommandLineInputSpec):
    """Input specification for the CiftiSurfaceResample command."""

    in_file = File(
        exists=True,
        mandatory=True,
        argstr="%s ",
        position=0,
        desc="the gifti file",
    )

    current_sphere = File(
        exists=True,
        position=1,
        argstr=" %s",
        desc=" the current sphere surface in gifti for in_file",
    )

    new_sphere = File(
        exists=True,
        position=2,
        argstr=" %s",
        desc=" the new sphere surface to be resample the in_file to, eg fsaverag5 or fsl32k",
    )

    metric = traits.Str(
        argstr=" %s ",
        position=3,
        desc=" fixed for anatomic",
        default="  BARYCENTRIC  ",
    )

    out_file = File(
        name_source=["in_file"],
        name_template="resampled_%s.surf.gii",
        keep_extension=True,
        argstr=" %s",
        position=4,
        desc="The gifti output, either left and right",
    )


class _CiftiSurfaceResampleOutputSpec(TraitedSpec):
    """Input specification for the CiftiSurfaceResample command."""

    out_file = File(exists=True, desc="output gifti file")


class CiftiSurfaceResample(WBCommand):
    """Resample a surface from one sphere to another.

    TODO: Improve documentation.
    """

    input_spec = _CiftiSurfaceResampleInputSpec
    output_spec = _CiftiSurfaceResampleOutputSpec
    _cmd = "wb_command  -surface-resample"
