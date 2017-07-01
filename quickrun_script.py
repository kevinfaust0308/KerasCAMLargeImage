from keras.models import load_model
import time
import cv2

from heatmap_generator import overlay_multi_layered_cam_large_image, overlay_single_layered_cam_large_image

##################################################### CONFIGS #########################################################

INPUT_IMAGE_PATH = 'input.jpg'
OUTPUT_IMAGE_PATH = 'output_heatmap.jpg'

trained_img_size = 512  # size of each tile (size our cnn was trained on)
conv_block = 'block5_pool'  # name of the final convolutional layer (for vgg) (can view layers using model.summary())
classes = ['Blank', 'Gray Mat.', 'Lesion', 'White Mat.']  # classes model was trained on. ordering matters
a = 0.3  # heatmap transparency

# single layer configs
heatmap_class = 'Gray Mat.'  # get heatmap of specified class

# multi layer configs
show_top_x_classes = len(classes)  # show colors of all classes

################################################# END OF CONFIGS ######################################################

# load model
model = load_model('VGG19_trained.h5')


def generate_heatmap(img_path, save_path, multi=True):
    # image to do heatmap on
    im = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)

    if multi:
        cam, avg_pred = overlay_multi_layered_cam_large_image(model, trained_img_size, classes, im, conv_block,
                                                              show_top_x_classes=show_top_x_classes, overlay_alpha=a)
    else:
        cam, avg_pred = overlay_single_layered_cam_large_image(model, trained_img_size, classes, im, conv_block,
                                                               class_name=heatmap_class, overlay_alpha=a)

    # save heatmap generated
    cv2.imwrite(save_path, cv2.cvtColor(cam, cv2.COLOR_RGB2BGR))

    return avg_pred


if __name__ == '__main__':
    start_time = time.clock()
    # heatmap, avg_pred = generate_heatmap_single_layer('small_tiled_tissue.jpg', 'single_class_heatmap_GRAYMATTER.jpg')
    avg_pred = generate_heatmap(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH)
    print('\n' + avg_pred + '\n')
    print(time.clock() - start_time, "seconds")
