# Attendance System  repo backend 

Backend for Attendance sys repo

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install syllabus.



Train a face classifier model with your own set of images from: [Google Collab](https://colab.research.google.com/drive/1D4Nn5ToPBbovpEjdnrVRMvqVe1sQkPuD?usp=sharing)
The folder structure in your google drive to store the training and test datasets should be:
```bash
Your Drive
├── ...
├── project                
│   ├── datasets            
│       ├── train
|            ├── DESIRED_LABEL_FOR_IMAGES(eg.075BCT001, or RAM)
|                ├── any_filename.jpg
|                ├── any_filename2.jpg  #store nearly 20 training images
|             ├── DESIRED_LABEL_FOR_IMAGES2(eg.075BCT002, or RAM2)
|                ├── any_filename.jpg
|                ├── any_filename2.jpg #store nearly 20 training images
|                
|       ├── val
|            ├── DESIRED_LABEL_FOR_IMAGES(eg.075BCT001, or RAM)
|                ├── any_filename.jpg
|                ├── any_filename2.jpg #store nearly 8 validating images
|            ├── DESIRED_LABEL_FOR_IMAGES2(eg.075BCT002, or RAM2)
|                ├── any_filename.jpg
|                ├── any_filename2.jpg #store nearly 8 validating images
│                   
└── ...
```
The model will be saved inside `gdrive/My Drive/project` of your google drive, download into your cloned folder as `model.sav`.
Also, download `datasets-embeddings.npz` from `gdrive/My Drive/project` into your cloned dir.

```bash
pip install -r requirements.txt
source ./run.sh
```

Cheers! There you go....

## Contributers / Team Members

- [Aaditya Subedi](https://github.com/AadityaSubedi)
- [Arpan Gyawali](https://github.com/ArpanGyawali)
- [Bijay Shrestha](https://github.com/Hakudon)
- [Bidhan Khatiwada](https://github.com/Bidhan123)
