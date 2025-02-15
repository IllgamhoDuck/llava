import json
import zipfile
from datasets import load_dataset
import os

DATA_DIR = '/content/drive/MyDrive/구직/Twelvelabs/llava/playground/data'
PRETRAINING_DATA_DIR = f'{DATA_DIR}/LLaVA-Pretrain'
SAMPLE_JSON_PATH = f'{PRETRAINING_DATA_DIR}/blip_laion_cc_sbu_558k_100_sample.json'
IMAGES_DIR = f'{PRETRAINING_DATA_DIR}/images'

# [ pretraining datasets ]
if not os.path.exists(SAMPLE_JSON_PATH):
    dataset = load_dataset(
        'liuhaotian/LLaVA-Pretrain',
        data_files={'train': 'blip_laion_cc_sbu_558k.json'}
    )
    # sample only 100 datas
    dataset['train'] = dataset['train'].select(range(100))
    dataset['train'].to_json(SAMPLE_JSON_PATH, lines=False, indent=2)

    # Extract images only if the images directory doesn't exist
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR, exist_ok=True)
        image_files = [item['image'] for item in dataset['train']]

        IMAGE_ZIP = f'{PRETRAINING_DATA_DIR}/images.zip'
        with zipfile.ZipFile(IMAGE_ZIP, 'r') as zip_ref:
            for file in image_files:
                zip_ref.extract(file, IMAGES_DIR)

# [ finetuning datasets ]
if not os.path.exists(f'{DATA_DIR}/llava_v1_5_mix665k_100_sample.json'):
    json_file = f'{DATA_DIR}/llava_v1_5_mix665k.json'
    with open(json_file, 'r') as f:
        data = json.load(f)

    # sample only 100 datas
    TOTAL_DATA = 100

    # retrieve only 100 coco datas from data checking one by one
    coco_samples = []
    count = 0
    for item in data:
        # Check if the image path contains 'coco'
        if item['image'].startswith('coco'):
            coco_samples.append(item)
            count += 1
            if count >= TOTAL_DATA:
                break

    # save as json
    with open(f'{DATA_DIR}/llava_v1_5_mix665k_100_sample.json', 'w') as f:
        json.dump(coco_samples, f, indent=2, ensure_ascii=False)

    # For COCO images, extract only selected images
    IMAGE_ZIP = f'{DATA_DIR}/coco/train2017.zip'
    with zipfile.ZipFile(IMAGE_ZIP, 'r') as zip_ref:
        # check the filelist
        filelist = zip_ref.namelist()
        for sample in coco_samples:
            image_name = '/'.join(sample['image'].split('/')[-2:])
            try:
                zip_ref.extract(image_name, f'{DATA_DIR}/coco')
            except KeyError:
                print(f"Warning: Could not find {image_name} in zip file")
