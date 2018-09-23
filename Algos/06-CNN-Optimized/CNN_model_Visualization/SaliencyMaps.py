import numpy as np
import keras.backend as K
import tensorflow as tf


class SaliencyMask(object):
    """Base class for saliency masks."""
    def __init__(self, model, output_index=0):
        """Constructs a SaliencyMask.

        Args:
            model: the keras model used to make prediction
            output_index: the index of the node in the last layer to take derivative on
        """
        pass

    def get_mask(self, input_image):
        """Returns an unsmoothed mask.

        Args:
            input_image: input image with shape (H, W, 3).
        """
        pass

    def get_smoothed_mask(self, input_image, stdev_spread=.2, nsamples=50):
        """Returns a mask that is smoothed with the SmoothGrad method.

        Args:
            input_image: input image with shape (H, W, 3).
        """
        stdev = stdev_spread * (np.max(input_image) - np.min(input_image))

        total_gradients = np.zeros_like(input_image)
        for i in range(nsamples):
            noise = np.random.normal(0, stdev, input_image.shape)
            x_value_plus_noise = input_image + noise

            total_gradients += self.get_mask(x_value_plus_noise)

        return total_gradients / nsamples

from keras.models import load_model


class GradientSaliency(SaliencyMask):
    """A SaliencyMask class that computes saliency masks with a gradient."""

    def __init__(self, model, output_index=0):
        # Define the function to compute the gradient
        input_tensors = [model.input,        # placeholder for input image tensor
                         K.learning_phase(), # placeholder for mode (train or test) tense
                        ]
        gradients = model.optimizer.get_gradients(model.output[0][output_index], model.input)
        self.compute_gradients = K.function(inputs=input_tensors, outputs=gradients)

    def get_mask(self, input_image):
        """Returns a vanilla gradient mask.

        Args:
            input_image: input image with shape (H, W, 3).
        """
        
        # Execute the function to compute the gradient
        x_value = np.expand_dims(input_image, axis=0)
        gradients = self.compute_gradients([x_value, 0])[0][0]

        return gradients

class GuidedBackprop(SaliencyMask):
    """A SaliencyMask class that computes saliency masks with GuidedBackProp.

    This implementation copies the TensorFlow graph to a new graph with the ReLU
    gradient overwritten as in the paper:
    https://arxiv.org/abs/1412.6806
    """

    GuidedReluRegistered = False

    def __init__(self, model, output_index=0, custom_loss=None):
        """Constructs a GuidedBackprop SaliencyMask."""

        if GuidedBackprop.GuidedReluRegistered is False:
            @tf.RegisterGradient("GuidedRelu")
            def _GuidedReluGrad(op, grad):
                gate_g = tf.cast(grad > 0, "float32")
                gate_y = tf.cast(op.outputs[0] > 0, "float32")
                return gate_y * gate_g * grad
        GuidedBackprop.GuidedReluRegistered = True
        
        """ 
            Create a dummy session to set the learning phase to 0 (test mode in keras) without 
            inteferring with the session in the original keras model. This is a workaround
            for the problem that tf.gradients returns error with keras models that contains 
            Dropout or BatchNormalization.

            Basic Idea: save keras model => create new keras model with learning phase set to 0 => save
            the tensorflow graph => create new tensorflow graph with ReLU replaced by GuiededReLU.
        """   

        model.save('gb_keras.h5') 
        with tf.Graph().as_default(): 
            with tf.Session().as_default(): 
                K.set_learning_phase(0)
                load_model('gb_keras.h5', custom_objects={"custom_loss":custom_loss})
                session = K.get_session()
                tf.train.export_meta_graph()
                
                saver = tf.train.Saver()
                saver.save(session, "tmp/guided_backprop_ckpt")

        self.guided_graph = tf.Graph()
        with self.guided_graph.as_default():
            self.guided_sess = tf.Session(graph = self.guided_graph)

            with self.guided_graph.gradient_override_map({'Relu': 'GuidedRelu'}):
                saver = tf.train.import_meta_graph("tmp/guided_backprop_ckpt.meta")
                saver.restore(self.guided_sess, "tmp/guided_backprop_ckpt")

                self.imported_y = self.guided_graph.get_tensor_by_name(model.output.name)[0][output_index]
                self.imported_x = self.guided_graph.get_tensor_by_name(model.input.name)

                self.guided_grads_node = tf.gradients(self.imported_y, self.imported_x)
        
    def get_mask(self, input_image):
        """Returns a GuidedBackprop mask."""
        x_value = np.expand_dims(input_image, axis=0)
        guided_feed_dict = {}
        guided_feed_dict[self.imported_x] = x_value        

        gradients = self.guided_sess.run(self.guided_grads_node, feed_dict = guided_feed_dict)[0][0]

        return gradients

class IntegratedGradients(GradientSaliency):
    """A SaliencyMask class that implements the integrated gradients method.

    https://arxiv.org/abs/1703.01365
    """

    def GetMask(self, input_image, input_baseline=None, nsamples=100):
        """Returns a integrated gradients mask."""
        if input_baseline == None:
            input_baseline = np.zeros_like(input_image)

        assert input_baseline.shape == input_image.shape

        input_diff = input_image - input_baseline

        total_gradients = np.zeros_like(input_image)

        for alpha in np.linspace(0, 1, nsamples):
            input_step = input_baseline + alpha * input_diff
            total_gradients += super(IntegratedGradients, self).get_mast(input_step)

        return total_gradients * input_diff


from keras.layers import Input, Conv2DTranspose
from keras.models import Model
from keras.initializers import Ones, Zeros


class VisualBackprop(SaliencyMask):
    """A SaliencyMask class that computes saliency masks with VisualBackprop (https://arxiv.org/abs/1611.05418).
    """

    def __init__(self, model, output_index=0):
        """Constructs a VisualProp SaliencyMask."""
        inps = [model.input, K.learning_phase()]           # input placeholder
        outs = [layer.output for layer in model.layers]    # all layer outputs
        self.forward_pass = K.function(inps, outs)         # evaluation function
        
        self.model = model

    def get_mask(self, input_image):
        """Returns a VisualBackprop mask."""
        x_value = np.expand_dims(input_image, axis=0)
        
        visual_bpr = None
        layer_outs = self.forward_pass([x_value, 0])

        for i in range(len(self.model.layers)-1, -1, -1):
            if 'Conv2D' in str(type(self.model.layers[i])):
                layer = np.mean(layer_outs[i], axis=3, keepdims=True)
                layer = layer - np.min(layer)
                layer = layer/(np.max(layer)-np.min(layer)+1e-6)

                if visual_bpr is not None:
                    if visual_bpr.shape != layer.shape:
                        visual_bpr = self._deconv(visual_bpr)
                    visual_bpr = visual_bpr * layer
                else:
                    visual_bpr = layer
                print(visual_bpr.shape)

        return visual_bpr[0]
    
    def _deconv(self, feature_map):
        """The deconvolution operation to upsample the average feature map downstream"""
        x = Input(shape=(None, None, 1))
        y = Conv2DTranspose(filters=1, 
                            kernel_size=(3,3), 
                            strides=(2,2), 
                            padding='same', 
                            kernel_initializer=Ones(), 
                            bias_initializer=Zeros())(x)

        deconv_model = Model(inputs=[x], outputs=[y])

        inps = [deconv_model.input, K.learning_phase()]   # input placeholder                                
        outs = [deconv_model.layers[-1].output]           # output placeholder
        deconv_func = K.function(inps, outs)              # evaluation function
        
        return deconv_func([feature_map, 0])[0]
