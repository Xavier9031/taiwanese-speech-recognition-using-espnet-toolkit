import os
import torchaudio
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import pandas as pd
import tqdm

def prepare_audio_file(audio_input, sr, processor, max_input_length_in_sec=10):
    # 確保音頻為單聲道
    if audio_input.shape[0] > 1:
        audio_input = audio_input.mean(dim=0, keepdim=True)

    # 重新採樣至16000Hz
    if sr != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
        audio_input = resampler(audio_input)

    # Check audio length in seconds
    audio_length_seconds = audio_input.shape[1] / 16000
    if audio_length_seconds > max_input_length_in_sec or audio_length_seconds < 1:
        return None, None

    # 處理音頻並獲取模型輸入
    input_values = processor(audio_input.squeeze(0), sampling_rate=16000, return_tensors="pt").input_features[0]
    return input_values, audio_length_seconds

def load_and_transcribe_audio(directory, model, processor, max_input_length_in_sec=10):
    results = []
    for filename in tqdm.tqdm(os.listdir(directory)):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            audio_input, sr = torchaudio.load(file_path)

            input_values, audio_length_seconds = prepare_audio_file(audio_input, sr, processor, max_input_length_in_sec)
            if input_values is None:
                continue  # Skip files that do not meet the duration criteria

            # 生成文字
            generated_ids = model.generate(input_values)
            transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            results.append({"id": filename, "text": transcription})
    return results

def save_to_csv(results, output_file):
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)

def main(audio_directory, output_csv, pretrain_model):
    processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
    model = WhisperForConditionalGeneration.from_pretrained(pretrain_model)
    transcriptions = load_and_transcribe_audio(audio_directory, model, processor)
    save_to_csv(transcriptions, output_csv)

if __name__ == "__main__":
    sound_dir = "/mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/test/test"
    output_csv = "output/output_tiny-11700.csv"
    pretrain_model = "/mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/tiny_result/checkpoint-11700"
    main(sound_dir, output_csv, pretrain_model)
