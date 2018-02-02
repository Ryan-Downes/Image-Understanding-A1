## CSC320 Winter 2017 
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION 
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS 
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions, 
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################
from os.path import isfile

#########################################

#
# The Matting Class
#
# This class contains all methods required for implementing 
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing 
    # algorithms. These images are initialized to None and populated/accessed by 
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = { 
            'backA': None, 
            'backB': None, 
            'compA': None, 
            'compB': None, 
            'colOut': None,
            'alphaOut': None, 
            'backIn': None, 
            'colIn': None, 
            'alphaIn': None, 
            'compOut': None, 
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self): 
        return {
            'backA':{'msg':'Image filename for Background A Color','default':None},
            'backB':{'msg':'Image filename for Background B Color','default':None},
            'compA':{'msg':'Image filename for Composite A Color','default':None},
            'compB':{'msg':'Image filename for Composite B Color','default':None},
        }
    # Same as above, but for the output arguments
    def mattingOutput(self): 
        return {
            'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
            'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
        }
    def compositingInput(self):
        return {
            'colIn':{'msg':'Image filename for Object Color','default':None},
            'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
            'backIn':{'msg':'Image filename for Background Color','default':None},
        }
    def compositingOutput(self):
        return {
            'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
        }
    
    # Copy the output of the triangulation matting algorithm (i.e., the 
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the 
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################
            
    # Use OpenCV to read an image from a file and copy its contents to the 
    # matting instance's private dictionary object. The key 
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################

        self._images[key] = cv.imread(fileName)
        if self._images[key] is None:
            if not isfile(fileName):
                msg = fileName + ' can not be found.'
            else:
                msg = 'The file ' + fileName + ' can be found but not read.'
        else:
            success = True

        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the 
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63. 
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################

        # check's to see if the image exists

        if self._images[key] is None:
            msg = 'Unable to save empty image to ' + fileName + ' .'

        else:
            cv.imwrite(fileName, self._images[key])
            success = True

        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary 
    # ojbect. 
    def triangulationMatting(self):
        """
success, errorMessage = triangulationMatting(self)
        
        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        
        shape = np.shape(self._images['compA'])
        size = np.prod(shape)
        
        comp_a_shape = np.shape(self._images['compA'])
        compB_shape = np.shape(self._images['backA'])
        backA_shape = np.shape(self._images['backA'])
        backB_shape = np.shape(self._images['backB'])
        
        if shape != compB_shape or shape != backA_shape or shape != backB_shape :
            msg = "Images not of the same size."
            
        else:
            comp_a = np.array(self._images['compA'].ravel().astype(np.float32))
            comp_b = np.array(self._images['compB'].ravel().astype(np.float32))
            back_a = np.array(self._images['backA'].ravel().astype(np.float32))
            back_b = np.array(self._images['backB'].ravel().astype(np.float32))

            r_comp_dif = comp_a[::3] - comp_b[::3]
            b_comp_dif = comp_a[1::3] - comp_b[1::3]
            g_comp_dif = comp_a[2::3] - comp_b[2::3]
            r_back_dif = back_a[::3] - back_b[::3]
            b_back_dif = back_a[1::3] - back_b[1::3]
            g_back_dif = back_a[2::3] - back_b[2::3]

            with np.errstate(divide="ignore", invalid='ignore'):
                alpha = 1 - np.divide((r_comp_dif + b_comp_dif + g_comp_dif), (r_back_dif + b_back_dif + g_back_dif))

            alpha_img = np.empty(size)

            alpha_img[::3] = alpha
            alpha_img[1::3] = alpha
            alpha_img[2::3] = alpha

            alpha_img = np.clip(alpha_img, 0, 1)

            col_img = comp_a - back_a * (1 -alpha_img)
            col_img = col_img.reshape(comp_a_shape)

            alpha_img *= 255
            alpha_img = alpha_img.reshape(comp_a_shape)

            self._images['alphaOut'] = alpha_img
            self._images['colOut'] = col_img
            success = True
            
            ## Below is an alternate implementation that uses reduction in noise to gain speed benifits
            ## for the example image noise level is set to 15 and this creates nicer images then the code above 
            ## it runs in ~ 2 second.

            # neg_backA = np.negative(np.array(self._images['backA']).ravel().astype(np.int16))
            # neg_backB = np.negative(np.array(self._images['backB']).ravel().astype(np.int16))
            #
            # rgb_num = len(neg_backA) # the number of picsals times 3 (RGB)
            #
            # C_delta_A = np.array((self._images['compA']).astype(np.int16) - (self._images['backA']).astype(np.int16)).ravel()
            # C_delta_B = np.array((self._images['compB']).astype(np.int16) - (self._images['backB']).astype(np.int16)).ravel()
            #
            # sqare_eye = np.eye(3, 3)
            # tiled_eye = np.tile(sqare_eye, ((rgb_num * 2) / 3, 1))
            #
            # C_delta = np.empty(rgb_num * 2)
            # neg_col = np.empty(rgb_num * 2)
            # for i in range(0, 3):
            #     neg_col[i::6] = neg_backA[i::3]
            #     neg_col[i + 3::6] = neg_backB[i::3]
            #     C_delta[i::6] = C_delta_A[i::3]
            #     C_delta[i + 3::6] = C_delta_B[i::3]
            #
            # prob_mat = np.concatenate((tiled_eye, np.array([neg_col]).T), axis=1)
            #
            # col = np.empty(rgb_num)
            # alpha = np.empty(rgb_num)
            # for i in range(0, (rgb_num * 2) - 6 ,6):
            #
            #     # setting noise_level = 0 leads to a solution in the same time as the solution provided.
            #     noise_level = 15
            #
            #     if max(np.absolute(C_delta[i:i + 6])) < noise_level:
            #         col[(i / 6) * 3] = 0
            #         col[((i / 6) * 3) + 1] = 0
            #         col[((i / 6) * 3) + 2] = 0
            #         alpha[(i / 6) * 3] = 0
            #         alpha[((i / 6) * 3) + 1] = 0
            #         alpha[((i / 6) * 3) + 2] = 0
            #     else:
            #         U, s, V = np.linalg.svd(prob_mat[i: i+6])
            #
            #         s = np.reciprocal(s)
            #         S = np.zeros((6,4))
            #         S[:4,:4] = np.diag(s)
            #
            #         sol = np.dot(V.T, np.dot(S.T, np.dot(U.T, np.transpose([C_delta[i:i + 6]]))))
            #
            #         col[(i / 6) * 3] = sol[0]
            #         col[((i / 6) * 3) + 1] = sol[1]
            #         col[((i / 6) * 3) + 2] = sol[2]
            #         alpha[(i / 6) * 3] = sol[3] * 255
            #         alpha[((i / 6) * 3) + 1] = sol[3] * 255
            #         alpha[((i / 6) * 3) + 2] = sol[3] * 255
            #
            # col = col.reshape(comp_a_shape)
            # alpha = alpha.reshape(comp_a_shape)
            #
            # self._images['colOut'] = col
            # self._images['alphaOut'] = alpha
            # success = True

        #########################################

        return success, msg
        
    def createComposite(self):
        """
success, errorMessage = createComposite(self)
        
        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
"""

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        shape = np.shape(self._images['alphaIn'])
        
        if shape != np.shape(self._images['backIn']):
            msg = "Images not of the same size."
        else:
        
            alpha = (self._images['alphaIn']).astype(np.float32)

            col = self._images['colIn']
            neg_alpha = (255 - alpha)/255
    
            back = self._images['backIn']
            a_col = col * (alpha/255)
            b_col = back * neg_alpha
            self._images['compOut'] = a_col + b_col
            success = True


        #########################################

        return success, msg


