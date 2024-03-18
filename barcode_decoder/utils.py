import matplotlib.pyplot as plt


def display_transformed_image(tensor):
    np_image = tensor.numpy().squeeze()
    plt.imshow(np_image, cmap='gray')
    plt.axis('off')
    plt.show()