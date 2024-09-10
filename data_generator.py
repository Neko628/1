from trdg.generators import GeneratorFromStrings
import xml.etree.ElementTree as ET
import os
import pandas as pd
import cv2 as cv
from PIL import Image

namespace = {'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}

def get_data_from_transkribus(folder):
    all_data = []
    for file in os.listdir(folder):
        if str(file).endswith('.xml'):
            all_data.append(get_text_from_transkribus(os.path.join(folder, file)))
    return all_data
        
def get_text_from_transkribus(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data_lines = []
    
    for text_line in root.findall('.//ns:TextLine', namespace):
        words = []
        for word in text_line.findall('.//ns:Word', namespace):
            word_text = word.find('.//ns:Unicode', namespace).text
            words.append((word_text))
        data_lines.append(words)
    return data_lines
        

def synthesizer(path, output, font_folder):
    index = 0
    csv_file_name = []
    csv_text = []
    list_data = get_data_from_transkribus(path)
    generator_list = []
    fonts = []

    for sentences in list_data:
        for sentence in sentences:
            generator_string = ""
            for word in sentence:
                generator_string = f'{generator_string} {word}'
            if generator_string:
                generator_list.append(generator_string)
    print(len(generator_list))

    for font in os.listdir(font_folder):
        fonts.append(os.path.join(font_folder, font))

    """
    strings: List[str],
            count: int = -1,
            fonts: List[str] = [],
            language: str = "en",
            size: int = 32,
            skewing_angle: int = 0,
            random_skew: bool = False,
            blur: int = 0,
            random_blur: bool = False,
            background_type: int = 0,
            distorsion_type: int = 0,
            distorsion_orientation: int = 0,
            is_handwritten: bool = False,
            width: int = -1,
            alignment: int = 1,
            text_color: str = "#282828",
            orientation: int = 0,
            space_width: float = 1.0,
            character_spacing: int = 0,
            margins: Tuple[int, int, int, int] = (5, 5, 5, 5),
            fit: bool = False,
            output_mask: bool = False,
            word_split: bool = False,
            image_dir: str = os.path.join(
                "..", os.path.split(os.path.realpath(__file__))[0], "images"
            ),
            stroke_width: int = 0,
            stroke_fill: str = "#282828",
            image_mode: str = "RGB",
            output_bboxes: int = 0,
            rtl: bool = False,

    """
    
    generator = GeneratorFromStrings(
        generator_list,
        random_skew=True,
        skewing_angle=1,
        count=10,
        background_type=1,
        fonts=fonts,
        text_color='#000000',
        size=50
    )
    for img, lbl in generator:
            filename = os.path.join(output, f'Syn_{index}_{str(lbl)[0:5]}.png')
            csv_file_name.append(filename)
            csv_text.append(lbl)
            img.save(filename)
            index += 1

    df = pd.DataFrame({
    'file_name': csv_file_name,
    'text': csv_text
    })

    df.to_csv(os.path.join(output, 'ground_truth.csv'), index=False)

        



