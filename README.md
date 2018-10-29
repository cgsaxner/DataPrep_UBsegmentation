# Exploit 18F-FDG enhanced urinary bladder in PET data for Deep Learning Ground Truth Generation in CT scans

MeVisLab macro module for the preparation of training and testing data for urinary bladder segmentation using deep learning.

Contains a general network for loading and vizualisation of CT and PET data, as well as the DataPreparation macro module for the generation of a ground truth from PET data and data augmentation.

## Requirements

To use the network, you need:

1. [MeVisLab](https://www.mevislab.de/download/) 3.0.1 with a valid licence
2. [Python](https://www.python.org/download/releases/2.7/) 2.7 with [NumPy](http://www.numpy.org/)

## Getting Started

1. Clone the repository:
```git clone https://github.com/cgsaxner/DataPrep_UBsegmentation.git```
2. Open the ```generalNetwork.mlab``` in MeVisLab
3. To use the ```DataPreperationMacro``` Module, import it to the general network by navigating to File -> Add Local Macro... and importing the ```DataPreparation.script``` file located in the DataPreparationMacro folder.

## License

If you use the software/network, please cite the following paper:

Gsaxner, Christina et al. **Exploit 18F-FDG Enhanced Urinary Bladder in PET Data for Deep Learning Ground Truth Generation in CT Scans.** SPIE Medical Imaging 2018.

    @inproceedings{gsaxner2018exploit,
      title={Exploit 18 F-FDG enhanced urinary bladder in PET data for deep learning ground truth generation in CT scans},
      author={Gsaxner, Christina and Pfarrkirchner, Birgit and Lindner, Lydia and Jakse, Norbert and Wallner, J{\"u}rgen and Schmalstieg, Dieter and Egger, Jan},
      booktitle={Medical Imaging 2018: Biomedical Applications in Molecular, Structural, and Functional Imaging},
      volume={10578},
      pages={105781Z},
      year={2018},
      organization={International Society for Optics and Photonics}
    }
