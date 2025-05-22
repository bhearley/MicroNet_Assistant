#-----------------------------------------------------------------------------------------
#
#   SegmentMicroNet.py
#
#   PURPOSE: Segment an image using a trained micronet model
#
#   INPUTS:
#       model_path  path to the model
#       image_path  path to the image
#       class_num   number of classes
#   OUTPUT:
#       pred        Array of size [n,m,class_num] containing Booleans for class prediction
#-----------------------------------------------------------------------------------------
def SegmentMicroNet(model_path, image_path, class_num):
    # Import Modules
    import imageio
    import numpy as np
    import pretrained_microscopy_models as pmm
    import segmentation_models_pytorch as smp
    from skimage import img_as_ubyte
    import torch
    import warnings

    def compare(prediction, truth, labels):
        out = np.zeros(truth.shape, dtype='uint8')
        trues = [np.all(truth == v, axis=-1) for v in labels]
        preds = [prediction[:,:,i] for i in range(prediction.shape[2])]
        for t, p in zip(trues, preds):
            out[t & p, :] = [255, 255, 255] # true posative
            out[t & ~p, :] = [255, 0, 255] # false negative
            out[~t & p, :] = [0, 255, 255] # false posative       
        return out

    def load_model(model_path, class_values = {'Class 1': 0, 'Class 2': 1, 'Class 3': 2}):
        model_data = torch.load(model_path)
        #DEVICE = 'cuda'
        DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        decoder = model_data['decoder']
        encoder = model_data['encoder']
        #class_values = best_model['class_values']
        
        activation = 'softmax2d' if len(class_values) > 1 else 'sigmoid' #'softmax2d' for multicalss segmentation
        try:
            preprocessing_fn = smp.encoders.get_preprocessing_fn(encoder, 'imagenet')
        except ValueError:
            preprocessing_fn = smp.encoders.get_preprocessing_fn(encoder, 'imagenet+5k')
        model = getattr(smp, decoder)(encoder_name=encoder, 
                                            encoder_weights=None,
                                            classes=len(class_values),
                                            activation=activation)

        model.load_state_dict(pmm.util.remove_module_from_state_dict(model_data['state_dict']))
        model.eval()
        return model, preprocessing_fn

    #-----helper function to split data into batches
    def divide_batch(l, n): 
        for i in range(0, l.shape[0], n):  
            yield l[i:i + n,::] 

    # https://github.com/choosehappy/PytorchDigitalPathology
    def segmentation_models_inference(io, model, preprocessing_fn, device = None, batch_size = 8, patch_size = 512,
                                    num_classes=3, probabilities=None):

        # This will not output the first class and assumes that the first class is wherever the other classes are not!

        io = preprocessing_fn(io)
        io_shape_orig = np.array(io.shape)
        stride_size = patch_size // 2
        if device is None:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # add half the stride as padding around the image, so that we can crop it away later
        io = np.pad(io, [(stride_size // 2, stride_size // 2), (stride_size // 2, stride_size // 2), (0, 0)],
                    mode="reflect")

        io_shape_wpad = np.array(io.shape)

        # pad to match an exact multiple of unet patch size, otherwise last row/column are lost
        npad0 = int(np.ceil(io_shape_wpad[0] / patch_size) * patch_size - io_shape_wpad[0])
        npad1 = int(np.ceil(io_shape_wpad[1] / patch_size) * patch_size - io_shape_wpad[1])

        io = np.pad(io, [(0, npad0), (0, npad1), (0, 0)], mode="constant")

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            arr_out = pmm.segmentation_training.extract_patches(io, (patch_size, patch_size, 3), stride_size)

        arr_out_shape = arr_out.shape
        arr_out = arr_out.reshape(-1, patch_size, patch_size, 3)

        # in case we have a large network, lets cut the list of tiles into batches
        output = np.zeros((0, num_classes, patch_size, patch_size))
        for batch_arr in divide_batch(arr_out, batch_size):
            arr_out_gpu = torch.from_numpy(batch_arr.transpose(0, 3, 1, 2).astype('float32')).to(device)

            # ---- get results
            output_batch = model.predict(arr_out_gpu)

            # --- pull from GPU and append to rest of output
            if probabilities is None:
                output_batch = output_batch.detach().cpu().numpy().round()
            else:
                output_batch = output_batch.detach().cpu().numpy()

            output = np.append(output, output_batch, axis=0)

        output = output.transpose((0, 2, 3, 1))

        # turn from a single list into a matrix of tiles
        output = output.reshape(arr_out_shape[0], arr_out_shape[1], patch_size, patch_size, output.shape[3])

        # remove the padding from each tile, we only keep the center
        output = output[:, :, stride_size // 2:-stride_size // 2, stride_size // 2:-stride_size // 2, :]

        # turn all the tiles into an image
        output = np.concatenate(np.concatenate(output, 1), 1)

        # incase there was extra padding to get a multiple of patch size, remove that as well
        output = output[0:io_shape_orig[0], 0:io_shape_orig[1], :]  # remove paddind, crop back

        if probabilities is None:
            if num_classes == 1:
                return output.astype('bool')
            else:
                return output[:, :, 1:].astype('bool')
        else:
            if num_classes == 1:
                output[:,:,0] = output[:,:,0] > probabilities
                return output.astype('bool')
            else:
                for i in range(num_classes-1): #don't care about background class
                    output[:,:,i+1] = output[:,:,i+1] > probabilities[i]
                return output[:, :, 1:].astype('bool')
    
    # Load the model
    if class_num == 2:
        class_num = 1
    model, preprocessing_fn = pmm.segmentation_training.load_segmentation_model(model_path, classes=class_num)

    # Load the image
    im = imageio.imread(image_path)
    im = im[:, :, :3] 
    im = img_as_ubyte(im)

    # Make the prediction
    pred = segmentation_models_inference(im, model, preprocessing_fn, batch_size=4, patch_size=512, num_classes=class_num)

    return pred