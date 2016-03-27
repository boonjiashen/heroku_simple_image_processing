import scipy.spatial
import scipy.misc
import numpy as np
import util

def unpickle(filename):
    import cPickle
    fo = open(filename, 'rb')
    dictionary = cPickle.load(fo)
    fo.close()
    return dictionary

class Mosaicker(object):

    def __init__(self, candidates):
        """
        `candidates` is a tile_size x tile_size x 3 x n array
        """

        self.candidates = candidates
        self.tile_size, _, n_channels, self.n = candidates.shape

        assert(n_channels == 3)
        assert(candidates.shape[0] == candidates.shape[1])

        self.X = np.vstack(candidates[:,:,:,i].flatten() for i in range(self.n))
        self.tree = scipy.spatial.cKDTree(self.X)


    def compute_mosaick(self, im_input):
        """Returns the photographic mosaick of the input

        `im_input` has height and width both multiples of tile_size
        `im_input` is a 3D image
        """

        src_height, src_width, n_channels = im_input.shape
        assert(n_channels == 3)
        assert(src_height % self.tile_size == 0)
        assert(src_width % self.tile_size == 0)

        windows, slice_tuples = zip(
                *util.yield_windows(im_input, 
                (self.tile_size, self.tile_size),
                (self.tile_size, self.tile_size),
                ))
        Y = np.vstack(window.flatten() for window in windows)

        _, neighbor_inds = self.tree.query(Y)

        im_output = im_input
        for neighbor_ind, slices in zip(neighbor_inds, slice_tuples):
            im_output[slices] = self.candidates[..., neighbor_ind]

        return im_output


def get_default_candidates():
    """Returns an 11x11x3x10000 matrix of candidate tiles"""

    filename = '/Users/jiashen/Downloads/cifar-10-batches-py/data_batch_1'
    all_candidates = unpickle(filename)['data'].T
    all_candidates = all_candidates.reshape([32, 32, 3, -1], order='F')
    all_candidates = all_candidates.transpose([1, 0, 2, 3])

    return all_candidates

def crop_to_a_multiple(input_image, step):
    """Returns a crop of a 3D or 2D image such that both height and width are
    multiples of `step`

    `input_image` is a 2D or 3D image.
    """
    assert(len(input_image.shape) >= 2)
    height, width = input_image.shape[:2]
    height = height - height%step
    width = width - width%step
    return input_image[:height, :width, ...]


def shrink_to_max_dim(input_image, max_dim):
    """Shrinks an input image such that output dimensions are all no larger
    than `max_dim`, either height or width are > max_dim, otherwise returns
    as-is.

    Shrink maintains aspect ratio.
    `input_image` is a 2D or 3D image.
    """

    assert(len(input_image.shape) >= 2)
    height, width = input_image.shape[:2]

    if (height <= max_dim and width <= max_dim):
        return input_image

    scale = float(max_dim) / max(height, width)
    return scipy.misc.imresize(input_image, scale)


class AppMosaicker(Mosaicker):
    """Default Mosaicker for Flask app"""

    def __init__(self, max_dim=500):
        """`max_size` of output image"""

        self.max_dim = max_dim  
        candidates = get_default_candidates()[::3,::3,:,:]
        Mosaicker.__init__(self, candidates)

    def compute_mosaick(self, input_image):

        input_image = shrink_to_max_dim(input_image, self.max_dim)
        input_image = crop_to_a_multiple(input_image, self.tile_size)
        output_image = Mosaicker.compute_mosaick(self, input_image)

        return output_image


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    mosaicker = AppMosaicker(500)
    im_original = scipy.misc.imread('/Users/jiashen/Downloads/sunset.jpg')
    output_image = mosaicker.compute_mosaick(im_original)

    plt.figure()
    plt.imshow(output_image)
    plt.show()
