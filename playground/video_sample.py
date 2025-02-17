import json
from datasets import load_dataset
import os

DATA_DIR = '/content/drive/MyDrive/구직/Twelvelabs/llava/playground/data'

# Download and extract video archive
video_dir = os.path.join(DATA_DIR, 'llava_video', 'videos')
os.makedirs(video_dir, exist_ok=True)

import requests
import tarfile
from tqdm import tqdm

# Download the first video archive
archive_url = "https://huggingface.co/datasets/lmms-lab/LLaVA-Video-178K/resolve/main/0_30_s_youtube_v0_1/0_30_s_youtube_v0_1_videos_1.tar.gz"
archive_path = os.path.join(DATA_DIR, '0_30_s_youtube_v0_1_videos_1.tar.gz')

if not os.path.exists(archive_path):
    print("Downloading video archive...")
    response = requests.get(archive_url, stream=True)
    response.raise_for_status()

    with open(archive_path, 'wb') as f:
        for chunk in tqdm(response.iter_content(chunk_size=8192)):
            if chunk:
                f.write(chunk)

    print("Download complete. Extracting files...")

    # Extract the archive
    with tarfile.open(archive_path, 'r:gz') as tar:
        tar.extractall(path=video_dir)

    print("Extraction complete!")
else:
    print("Archive already exists, skipping download")



# Load the dataset
video_folder = os.path.join(video_dir, 'liwei_youtube_videos/videos/youtube_video_2024')
output_json = f'{DATA_DIR}/llava_youtube_video_2024_100_sample.json'

if not os.path.exists(output_json):
    # Get list of MP4 files in the folder
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

    # Load original dataset for metadata
    dataset = load_dataset('lmms-lab/LLaVA-Video-178K', '0_30_s_youtube_v0_1')

    # Create mapping of video filenames to their metadata
    video_metadata = {}
    for split in ['caption', 'open_ended', 'multi_choice']:
        for item in dataset[split]:
            if item['video'].endswith('.mp4'):
                video_name = os.path.basename(item['video'])
                video_metadata[video_name] = item

    # Create formatted data for videos that exist in our folder
    formatted_data = []
    for video_file in video_files[:100]:  # Take first 100 videos
        if video_file in video_metadata:
            item = video_metadata[video_file]
            formatted_item = {
                'id': item['id'],
                'conversations': item['conversations'],
                'data_source': item['data_source'],
                'image': f'youtube_video_2024/{video_file}'  # Update path to reflect local structure
            }
            formatted_data.append(formatted_item)

    print(f"Total samples collected: {len(formatted_data)}")

    # Save as JSON
    with open(output_json, 'w') as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)

    print(f"Data saved to {output_json}")
