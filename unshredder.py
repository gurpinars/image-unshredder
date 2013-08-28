from PIL import Image
import ipdb
import argparse


class ShreddedImage(object):
    def __init__(self, image):
        self.obj_img = Image.open(image)
        self.size = self.width, self.height = self.image.size


def get_pixel_value(img, x, y):
    pixel = img.image.load()
    return pixel[x, y]


def calculate_difference(first, second):
    return sum(
        (abs(first[0] - second[0]),
         abs(first[1] - second[1]),
         abs(first[2] - second[2])
         ))


def get_first_pixels(image):
    first_pixels = [get_pixel_value(image, 0, y) for y in xrange(image.height)]
    return first_pixels


def get_last_pixels(image):
    last_pixels = [get_pixel_value(image, 31, y) for y in xrange(image.height)]
    return last_pixels


def find_next(shreds, src_key):
    diff = {}
    last_pixels = get_last_pixels(shreds[src_key])

    for i, key in enumerate(shreds.keys()):
        first_pixels = get_first_pixels(shreds[key])
        sm = 0
        for y in xrange(shreds[src_key].height):
            difference = calculate_difference(last_pixels[y], first_pixels[y])
            sm += difference

        if src_key != key:
            diff[i] = sm

    return min(diff, key=diff.get)


def save(image, match_li, shred_li):
    SHREDS = 20
    shredded = Image.new("RGBA", image.size)
    shred_width = image.width / SHREDS
    temp = []
    temp.insert(0, 0)

    for i, v in enumerate(match_li):
        if not temp[i]:
            temp.insert(i, match_li[temp[i - 1]])

    for i, k in enumerate(temp):
        shredded.paste(shred_li[k], (shred_width * i, 0))

    shredded.save("unshredded_image.png")


def split(image):
    shred_w = image.width / 20
    shreds = {}
    shred_li = []
    for x in xrange(0, image.width, shred_w):
        img = image.obj_img.crop((x, 0, shred_w + x, image.height))
        shreds[x] = img
        shred_li.append(img)

    return shreds, shred_li


def main():
    # ipdb.set_trace()
    parser = argparse.ArgumentParser(description='unshredder')
    parser.add_argument('image', help='image to be unshredded')
    args = parser.parse_args()

    image = ShreddedImage(args.image)
    shreds, shred_li = split(image)
    match_li = []

    for k in shreds.keys():
        match_li.append(find_next(shreds, k))

    save(image, match_li, shred_li)


if __name__ == '__main__':
    main()
