import argparse
import logging

import nibabel as nib
from dipy.viz import colormap
from dipy.tracking.streamline import Streamlines
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.streamline import save_trk

from dipy.viz import window, actor, has_fury
# import dipy.io.streamline.Streamlines
import dipy
from dipy.io.streamline import save_trk
from dipy.viz import window, actor
from fury.colormap import line_colors
from functions.ADCandFA import ADCandFAcalculator
from functions.data_processing.Tracktography import tracking
from functions.data_processing.tensor import tensor
from functions.utils.io import load_image
from functions.utils.manage_args import verify_file_exists, verify_file_is_nifti
from functions.data_processing.CreateMask import CreateB0Mask, CreateWMmask


#


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('filename_I',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")  # Always write a good explanation!
    p.add_argument('filename_J',
                   help="Image filename to be loaded. Image should be a test file "
                        "file.")  # Always write a good explanation!

    # Typical arg: add debugging prints or not
    p.add_argument('-v', action='store_true', dest='verbose',
                   help='If set, produces verbose output.')

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()
    print("****\n"
          "Args that were received in the main method: \n{}\n"
          "****".format(args))

    # 1. Verifications
    verify_file_exists(args.filename_I)
    from_nifti_i = verify_file_is_nifti(args.filename_I)
    verify_file_exists(args.filename_J)

    logging_level = 'DEBUG' if args.verbose else 'INFO'
    logging.basicConfig(level=logging_level)

    # 2. Load data
    logging.info("Loading data")

    dmri = load_image(args.filename_I, from_nifti_i)
    # print(args.filename_J)
    # print(dmri.shape)
    masked_dmri, B0Mask = CreateB0Mask(dmri)
    T = tensor(masked_dmri, args.filename_J, B0Mask)
    # Tnifti = nib.Nifti1Image(T, dmri.affine)
    # nib.save(Tnifti, 'Data/tensor.nii.gz')

    ADC, FA = ADCandFAcalculator(T, B0Mask)
    # FAnifti = nib.Nifti1Image(FA, dmri.affine)
    # nib.save(FAnifti, 'Data/FA.nii.gz')
    # ADCnifti = nib.Nifti1Image(ADC, dmri.affine)
    # nib.save(ADCnifti, 'Data/ADC.nii.gz')
    wm_mask, wmNonZeroList = CreateWMmask(B0Mask, FA, dmri)
    # Mask = nib.load('Data/cluster_toB.nii').get_data() # activated regions from question 1
    # wm_mask, wmNonZeroList = CreateWMmask(Mask, FA, dmri)

    streamlines = tracking(T, wm_mask, wmNonZeroList)
    streamlines = Streamlines(streamlines)
    color = colormap.line_colors(streamlines)

    streamlines_actor = actor.line(streamlines,
                                   colormap.line_colors(streamlines))

    # Create the 3D display.
    scene = window.Scene()
    scene.add(streamlines_actor)  # Save still images for this static example. Or for interactivity use
    window.record(scene, out_path='tractogram_EuDX.png', size=(800, 800))
    window.show(scene)
    sft = StatefulTractogram(streamlines, dmri, Space.RASMM)
    save_trk(sft, "tractograw_EuDX.trk", streamlines)


if __name__ == "__main__":
    main()
