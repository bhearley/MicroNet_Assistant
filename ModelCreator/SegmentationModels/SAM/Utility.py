def LoadModel(path, m_type):
    #-----------------------------------------------------------------------------------------
    #
    #   LoadModel.py
    #
    #   PURPOSE: Load the SAM Model
    #
    #   INPUTS:
    #       path        Path to the SAM Checkpoint
    #       m_type      SAM Model Type
    #
    #   OUTPUTS
    #       sam         Loaded model
    #       predictor   Predictor for the loaded model
    #
    #-----------------------------------------------------------------------------------------
    # Import Sys and add path
    import sys
    sys.path.append("..")

    # Import Segment Anything Module
    from segment_anything import sam_model_registry, SamPredictor
    import torch 

    # Set Device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    device = 'cpu'

    # Load the Model
    sam = sam_model_registry[m_type](checkpoint=path)
    sam.to(device)
    predictor = SamPredictor(sam)

    return sam, predictor

def SetImage(predictor, image_path):
    #-----------------------------------------------------------------------------------------
    #
    #   SetImage.py
    #
    #   PURPOSE: Load the SAM Model
    #
    #   INPUTS:
    #       predictor   Predictor for the loaded model
    #       image       SAM Model Type
    #
    #   OUTPUTS
    #       predictor   Predictor for the loaded image
    #       image_sam   CV2 image for SAM
    #
    #-----------------------------------------------------------------------------------------
    # Import Modules
    import cv2

    # Load the image
    image_sam = cv2.imread(image_path)
    image_sam = cv2.cvtColor(image_sam, cv2.COLOR_BGR2RGB)

    # Load the Image into the model
    predictor.set_image(image_sam)

    return predictor, image_sam

def GetMask(predictor, input_points, input_labels):
    #-----------------------------------------------------------------------------------------
    #
    #   GetMask.py
    #
    #   PURPOSE: Get the masks for the selected prompts
    #
    #   INPUTS:
    #       predictor       Predictor for the loaded model
    #       input_points    List of X,Y Pairs of Prompt Points
    #                           [[X1, Y1], [X2,Y2],...[XN,YN]]
    #       input_labels    List of labels of Prompt Points
    #                           0 = Background (exclude from segmentation)
    #                           1 = Forground (include in segmentation)
    #                           [1,1,0,...]
    #
    #   OUTPUTS
    #       mask            NxM array for each pixel indicating if it is in the segmentation
    #       score           Score associated with the best mask
    #       logit           Logit associated with the best mask
    #
    #-----------------------------------------------------------------------------------------
    # Import Modules
    import numpy as np
    
    # Convert to numpy array
    input_point = np.array(input_points)
    input_label = np.array(input_labels)

    # Set the multimask output flag
    if len(input_label) > 1:
        flag = False
    else:
        flag = True

    # Get the mask
    masks, scores, logits = predictor.predict(
                                            point_coords=input_point,
                                            point_labels=input_label,
                                            multimask_output=flag,
                                                )
    
    # Get the best mask
    mask = masks[0]
    score = scores[0]
    logit = logits[0]

    return mask, score, logit