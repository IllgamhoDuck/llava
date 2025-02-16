import os
import json
import pathlib


def create_multi_image_conversations(json_data, multi_image_ratio=0.5):
    """
    Converts a portion of the existing dataset into multi-image conversations.

    Args:
        json_data (list): Original conversation data
        multi_image_ratio (float): Ratio of data to convert to multi-image (0.0 ~ 1.0)

    Returns:
        list: Converted conversation data
    """
    import random
    import copy

    modified_data = copy.deepcopy(json_data)
    total_samples = len(modified_data)
    num_multi = int(total_samples * multi_image_ratio)

    multi_indices = random.sample(range(total_samples), num_multi)

    for idx in multi_indices:
        num_images = random.choice([2, 3])
        modified_data[idx]['image'] = [modified_data[idx]['image']] * num_images
        for conv in modified_data[idx]['conversations']:
            if '<image>' in conv['value']:
                for _ in range(num_images - 1):
                    conv['value'] += ' <image>'

    return modified_data


DATA_DIR = str(pathlib.Path(__file__).parent / 'data')
if not os.path.exists(f'{DATA_DIR}/llava_v1_5_mix665k_100_sample_multi.json'):
    with open(f'{DATA_DIR}/llava_v1_5_mix665k_100_sample.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    multi_image_data = create_multi_image_conversations(data)
    with open(f'{DATA_DIR}/multi_image_sample_100.json', 'w', encoding='utf-8') as f:
        json.dump(multi_image_data, f, indent=2, ensure_ascii=False)
