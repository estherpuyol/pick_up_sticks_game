import numpy as np
import argparse

try:
    import skimage
    from skimage import measure
except ImportError:
    print('Module skimage not found ')

if not int(skimage.__version__.split('.')[1]) > 17:
    raise RuntimeError('Version of the module skimage needs to be > 0.17 ')


# Digital differential analyzer (DDA) algorithm for line generation
# Mayorov, F. V. (1964). ELECTRONIC DIGITAL INTEGRATING COMPUTERS
# Digital Differential Analyzers. London: Iliffe Books Ltd.
def DDA(x0, y0, xEnd, yEnd):
    """
        :param x0: initial X position
        :param y0: initial Y position
        :param xEnd: initial X position
        :param yEnd: initial Y position
        :return:
    """
    # Calculate dx and dy
    dx = xEnd - x0
    dy = yEnd - y0

    # Calculate steps required for generating pixels
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = int(abs(dy))

    # Calculate increment in x and y for each steps
    dx = float(dx / steps)
    dy = float(dy / steps)

    # Generate an array where to save all pixels
    points = np.zeros((steps + 1, 2), dtype=int)
    # Initial pixel
    x = x0
    y = y0
    # Put pixel for each step
    for ii in range(steps + 1):
        points[ii, :] = [np.round(x, decimals=0), np.round(y, decimals=0)]
        x += dx
        y += dy
    return points


def main():
    # To compute the number of groups on the pick-up sticks game, I generated an 2D matrix (images) that contains the
    # location of all sticks and then use the image processing connected components to calculate the number of
    # groups. To draw the location of the sticks in image, I used the Digital differential analyzer (DDA) algorithm
    # that compute the location of the points over an interval between start and end point.
    # Generating of an image wil allow to have as many sticks as desired

    # Load file with the coordinates of the sticks
    try:
        line_segments_2D = np.loadtxt(args.filename)
    except FileNotFoundError:
        print("Filename {} does not exist".format(args.filename))

    # Cast line_segments_2D to be integers
    line_segments_2D -= np.min(line_segments_2D)
    line_segments_2D = line_segments_2D.astype(int)

    # Generate data_matrix that will store the location of the sticks as an image
    rows = np.round(np.max(line_segments_2D[:, [0, 2]]), decimals=0)
    cols = np.round(np.max(line_segments_2D[:, [1, 3]]), decimals=0)
    data_matrix = np.zeros((cols + 1, rows + 1), dtype=np.bool)

    # For each stick put it into the images
    for i, (x1, y1, x2, y2) in enumerate(line_segments_2D):
        p1 = DDA(x1, y1, x2, y2)
        # TODO: For speedup the code, adapt DDA in-built python function
        data_matrix[p1[:, 1], p1[:, 0]] = 1

    # Plot the images that contains all the sticks
    if args.debug:
        import matplotlib.pyplot as plt
        plt.imshow(data_matrix)

    # Compute connected components for the images
    labels, _num = measure.label(data_matrix, return_num=True)

    return _num


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to compute the number of groups in the pick-up sticks game')
    parser.add_argument('-f', '--filename', type=str,
                        help="full path to the txt file containing the coordinates of the "
                             "pick-up sticks game")
    parser.add_argument('-d', '--debug', type=bool, default=False,
                        help='Plot output')
    args = parser.parse_args()

    num = main()
    print('Number of groups for the pick-up sticks game: {:d}'.format(num))
