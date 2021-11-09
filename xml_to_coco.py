import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import ast
import argparse


"""parser"""
parser = argparse.ArgumentParser()
parser.add_argument('--images_dir_path', default='demo/', help='path to the directory stored images')
parser.add_argument('--output_path', default='./data/val.txt', help='output text path styled with coco format')
parser.add_argument('--xml_dir_path', default='./demo/xml_files/', help='path to the xml file')
parser.add_argument('--annotation_file', default='coco_classnames.txt', help='path to annotation file storing class names')
args = parser.parse_args()


if __name__ == "__main__":
    open(args.output_path, 'w').close() # clear the output file
    for xml_file in os.listdir(args.xml_dir_path):
        xml_path = os.path.join(args.xml_dir_path, xml_file)
        """load xml file"""
        tree = ET.parse(xml_path)
        root = tree.getroot()

        data = []
        name_box_id = defaultdict(list)

        with open(args.annotation_file, 'r') as f:
            contents = f.read()
            data =  ast.literal_eval(contents)

            """generate labels"""
            for ant in root.iter('annotation'):
                id = ant.find('filename').text
                name = os.path.join(args.xml_dir_path, '{}'.format(id))

            for object in root.iter('object'):

                cat_name = object.find('name').text

                cat = [k for k, v in data.items() if v == str(cat_name)][0]

                if cat >= 1 and cat <= 11:
                    cat = cat - 1
                elif cat >= 13 and cat <= 25:
                    cat = cat - 2
                elif cat >= 27 and cat <= 28:
                    cat = cat - 3
                elif cat >= 31 and cat <= 44:
                    cat = cat - 5
                elif cat >= 46 and cat <= 65:
                    cat = cat - 6
                elif cat == 67:
                    cat = cat - 7
                elif cat == 70:
                    cat = cat - 9
                elif cat >= 72 and cat <= 82:
                    cat = cat - 10
                elif cat >= 84 and cat <= 90:
                    cat = cat - 11

                for bbox in object.iter('bndbox'):
                    xmin = bbox.find('xmin').text
                    ymin = bbox.find('ymin').text
                    xmax = bbox.find('xmax').text
                    ymax = bbox.find('ymax').text

                    name_box_id[name].append((xmin, ymin, xmax, ymax, cat))

            f.close()

        """write to txt"""
        with open(args.output_path, 'a') as f:
            for key in name_box_id.keys():
                f.write(key)
                box_infos = name_box_id[key]
                for info in box_infos:
                    x_min = int(info[0])
                    y_min = int(info[1])
                    x_max = int(info[2])
                    y_max = int(info[3])

                    box_info = " %d,%d,%d,%d,%d" % (
                        x_min, y_min, x_max, y_max, int(info[4]))
                    f.write(box_info)
                f.write('\n')
            f.close()