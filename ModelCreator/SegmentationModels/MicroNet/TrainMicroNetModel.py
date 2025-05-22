#-----------------------------------------------------------------------------------------
#
#   TrainMicroNetModel.py
#
#   PURPOSE: Train a MicroNet Model
#
#   INPUTS:
#       MicroNetData    Data structure containing all MicroNet Settings
#-----------------------------------------------------------------------------------------
def TrainMicroNetModel(MicroNetData):
    # Import Modules
    import albumentations as albu
    import matplotlib.pyplot as plt
    import numpy as np
    import os
    from pathlib import Path
    import pretrained_microscopy_models as pmm
    import random
    import segmentation_models_pytorch as smp
    import shutil
    from tkinter import filedialog
    from tkinter import messagebox
    import torch

    # Set Directory Names
    x_train_dir = MicroNetData['Paths']['Train']
    y_train_dir = MicroNetData['Paths']['TrainL']
    x_valid_dir = MicroNetData['Paths']['Validation']
    y_valid_dir = MicroNetData['Paths']['ValidationL']
    x_test_dir = MicroNetData['Paths']['Test']
    y_test_dir = MicroNetData['Paths']['TestL']

    # Set random seeds for repeatability
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)

    # Get model parameters
    architecture = MicroNetData['Model']['Architecture']
    encoder = MicroNetData['Model']['Encoder']
    pretrained_weights = MicroNetData['Model']['PreWeights']
    if MicroNetData['Settings']['GPU'] == True:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = 'cpu'

    # Create the Unet model with a resnet backbone that is pre-trained on micronet
    model = pmm.segmentation_training.create_segmentation_model(
        architecture=architecture,
        encoder = encoder,
        encoder_weights=pretrained_weights, 
        classes=len(MicroNetData['Classes'].keys())
        )
    
    # Define Image Augmentation Functions
    def get_training_augmentation():
        train_transform = [
            albu.RandomCrop(MicroNetData['Augmentation']['Crop'], MicroNetData['Augmentation']['Crop']),
            albu.HorizontalFlip(p=MicroNetData['Augmentation']['HorzFlip']),
            albu.VerticalFlip(p=MicroNetData['Augmentation']['VertFlip']),
            albu.RandomRotate90(p=MicroNetData['Augmentation']['RRot90']),       
            albu.GaussNoise(p=MicroNetData['Augmentation']['RGaussNoise']),
            
            albu.OneOf(
                [
                    albu.CLAHE(p=MicroNetData['Augmentation']['CLAHE']),
                    albu.RandomBrightnessContrast(
                        brightness_limit=MicroNetData['Augmentation']['RBrightness'][1], 
                        contrast_limit=0.0, 
                        p=MicroNetData['Augmentation']['RBrightness'][0]),
                    albu.RandomGamma(p=MicroNetData['Augmentation']['RGamma']),
                ],
                p=0.50,
            ),

            albu.OneOf(
                [
                    albu.Sharpen(p=MicroNetData['Augmentation']['Sharpen']),
                    albu.Blur(
                        blur_limit=MicroNetData['Augmentation']['Blur'][1], 
                        p=MicroNetData['Augmentation']['Blur'][0]),
                ],
                p=0.50,
            ),

            albu.OneOf(
                [
                    albu.RandomBrightnessContrast(
                        brightness_limit=0.0, 
                        contrast_limit=MicroNetData['Augmentation']['RContrast'][1], 
                        p=MicroNetData['Augmentation']['RContrast'][0]),
                    albu.HueSaturationValue(p=MicroNetData['Augmentation']['HueSat']),
                ],
                p=0.50,
            ),
        ]
        return albu.Compose(train_transform)
    
    def get_validation_augmentation():
        """Add paddings to make image shape divisible by 32"""
        # This is turned off for this dataset
        test_transform = [
            albu.CenterCrop(MicroNetData['Augmentation']['Crop'],MicroNetData['Augmentation']['Crop'])
        ]
        return albu.Compose(test_transform)

    def to_tensor(x, **kwargs):
        return x.transpose(2, 0, 1).astype('float32')
    
    def get_preprocessing(preprocessing_fn):
        """Construct preprocessing transform
        
        Args:
            preprocessing_fn (callbale): data normalization function 
                (can be specific for each pretrained neural network)
        Return:
            transform: albumentations.Compose
        
        """
        
        _transform = [
            albu.Lambda(image=preprocessing_fn),
            albu.Lambda(image=to_tensor, mask=to_tensor),
        ]
        return albu.Compose(_transform)
    
    # How the images will be normalized. Use imagenet statistics even on micronet pre-training
    preprocessing_fn = smp.encoders.get_preprocessing_fn(encoder, 'imagenet')

    # Define class values
    class_values = MicroNetData['Classes']

    # Define Data Sets
    training_dataset = pmm.io.Dataset(
                                    images=x_train_dir,
                                    masks=y_train_dir,
                                    class_values=class_values,
                                    augmentation=get_training_augmentation(),
                                    preprocessing=get_preprocessing(preprocessing_fn)
                                    )
    
    validation_dataset = pmm.io.Dataset(
                                    images=x_valid_dir,
                                    masks=y_valid_dir,
                                    class_values=class_values,
                                    augmentation=get_validation_augmentation(),
                                    preprocessing=get_preprocessing(preprocessing_fn)
                                )

    test_dataset = pmm.io.Dataset(
                                    images=x_test_dir,
                                    masks=y_test_dir,
                                    class_values=class_values,
                                    augmentation=get_validation_augmentation(),
                                    preprocessing=get_preprocessing(preprocessing_fn)
                                )
    
    # Visuzalize Data Sets
    # -- Training
    if MicroNetData['Settings']['TrainViz'] == True:
        augmented_dataset = pmm.io.Dataset(
            images=x_train_dir,
            masks=y_train_dir,
            class_values=class_values,
            augmentation=get_training_augmentation(),
        )

        for im, mask in augmented_dataset:
            pmm.util.visualize(
                image=im,
                matrix_mask=mask[...,0].squeeze(),
                secondary_mask=mask[...,1].squeeze(),
                tertiary=mask[...,2].squeeze(),
            )

    # -- Validation
    if MicroNetData['Settings']['ValViz'] == True:
        visualize_dataset = pmm.io.Dataset(
            images=x_valid_dir,
            masks=y_valid_dir,
            class_values=class_values,
            augmentation=get_validation_augmentation(),
        )

        for im, mask in visualize_dataset:
            pmm.util.visualize(
                image=im,
                matrix_mask=mask.squeeze(),
                secondary_mask=mask[...,1].squeeze(),
                tertiary=mask[...,2].squeeze(),
            )

    if MicroNetData['Train']['Epochs'] is not None:
        state = pmm.segmentation_training.train_segmentation_model(
                    model=model,
                    architecture=architecture,
                    encoder=encoder,
                    train_dataset=training_dataset,
                    validation_dataset=validation_dataset,
                    class_values=class_values,
                    epochs= int(MicroNetData['Train']['Epochs']),
                    device=device,
                    lr=MicroNetData['Train']['LearnRate'],
                    batch_size=int(MicroNetData['Train']['BatchSize']),
                    val_batch_size=int(MicroNetData['Train']['ValBatchSize']),
                    save_folder='Temp',
                    save_name='new_model.tar'
                )
    elif MicroNetData['Train']['Patience'] is not None:
        state = pmm.segmentation_training.train_segmentation_model(
                    model=model,
                    architecture=architecture,
                    encoder=encoder,
                    train_dataset=training_dataset,
                    validation_dataset=validation_dataset,
                    class_values=class_values,
                    patience = int(MicroNetData['Train']['Patience']),
                    device=device,
                    lr=MicroNetData['Train']['LearnRate'],
                    batch_size=int(MicroNetData['Train']['BatchSize']),
                    val_batch_size=int(MicroNetData['Train']['ValBatchSize']),
                    save_folder='Temp',
                    save_name='new_model.tar'
                )
    else:
        raise Exception('Either Epochs or Patience must be defined.')
    
    # Show learning curves when finished
    plt.plot(state['train_loss'], label='train_loss')
    plt.plot(state['valid_loss'], label='valid_loss')
    plt.legend()
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.show()

    # Ask for additional training or save
    cont_flag = 0

    while cont_flag == 0:
        answer = messagebox.askyesno("Continue Training","Continue Training?")
        if answer == True:
            model_path = Path('Temp', 'new_model.tar')
            if MicroNetData['Train']['Epochs'] is not None:
                state = pmm.segmentation_training.train_segmentation_model(
                            model=model,
                            architecture=architecture,
                            encoder=encoder,
                            train_dataset=training_dataset,
                            validation_dataset=validation_dataset,
                            class_values=class_values,
                            epochs= int(MicroNetData['Train']['Epochs']),
                            device=device,
                            lr=MicroNetData['Train']['LearnRate'],
                            batch_size=int(MicroNetData['Train']['BatchSize']),
                            val_batch_size=int(MicroNetData['Train']['ValBatchSize']),
                            save_folder='Temp',
                            save_name='new_model.tar'
                        )
            elif MicroNetData['Train']['Patience'] is not None:
                state = pmm.segmentation_training.train_segmentation_model(
                            model=model,
                            architecture=architecture,
                            encoder=encoder,
                            train_dataset=training_dataset,
                            validation_dataset=validation_dataset,
                            class_values=class_values,
                            patience = int(MicroNetData['Train']['Patience']),
                            device=device,
                            lr=MicroNetData['Train']['LearnRate']/10,
                            batch_size=int(MicroNetData['Train']['BatchSize']),
                            val_batch_size=int(MicroNetData['Train']['ValBatchSize']),
                            save_folder='Temp',
                            save_name='new_model.tar'
                        )
                
            # Show learning curves when finished
            plt.plot(state['train_loss'], label='train_loss')
            plt.plot(state['valid_loss'], label='valid_loss')
            plt.legend()
            plt.xlabel('epoch')
            plt.ylabel('loss')
            plt.show()
        else:
            cont_flag = 1

    # Ask for save information
    file_path = ''
    while '.tar' not in file_path:
        file_path = filedialog.asksaveasfilename(
            title="Save the model",
            filetypes=(("Micronet Model", "*.tar"),)
        )

        if file_path != '':
            if '.tar' not in file_path:
                file_path = file_path + '.tar'

    # Move file
    shutil.move(os.path.join(os.getcwd(),'Temp','new_model.tar'),file_path)
    
    return