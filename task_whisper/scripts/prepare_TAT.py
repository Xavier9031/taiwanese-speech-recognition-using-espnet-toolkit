import json
from tqdm import tqdm
from pathlib import Path
import pandas as pd
from functools import partial
import argparse

# Prepare TAT dataset in such format (https://github.com/voidful/asr-training):
"""
path,text
/xxx/2.wav,被你拒絕而記仇
/xxx/4.wav,電影界的人
/xxx/7.wav,其實我最近在想
"""

CLEAN_MAPPING = {
    "﹖": "?",
    "！": "!",
    "％": "%",
    "（": "(",
    "）": ")",
    "，": ",",
    "：": ":",
    "；": ";",
    "？": "?",
    "—": "--",
    "─": "-",
}
ACCEPTABLE_CHARS = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "àáéìîòúāō"
    " "
    '!"%()+,-./:;=?_~'
    "‘’“”'"
    "…⋯"
    "、。『』"
    "－"
)


def get_wav_from_txt(txt_path, wav_dir):
    f_name = txt_path.stem
    spk_name = txt_path.parent.name
    pattern = f"{f_name}-[0-9]*.wav"
    [wav_path] = (wav_dir / spk_name).glob(pattern)
    return wav_path


def get_transcription_from_json(json_path, transcript_type):
    with open(json_path) as f:
        json_data = json.load(f)
        txt = json_data[transcript_type]
        txt = clean_text(txt, transcript_type)
        return txt


def clean_text(txt, transcript_type):
    if transcript_type == "台羅數字調":
        txt = txt.strip()
        txt = txt.replace("'", " ")
        txt = txt.replace('"', " ")
        txt = txt.replace("“", " ")
        txt = txt.replace("”", " ")
        txt = txt.replace(":", " ")
        txt = txt.replace(")", " ")
        txt = txt.replace("(", " ")
        txt = txt.strip()
        if txt.endswith(","):
            txt = txt[:-1] + "."
        if txt[-1] not in "?!.":
            txt += "."
        return txt
    else:
        raise NotImplementedError


def validate_transcription(transcript, transcript_type, bad_count, verbose_fp=None):
    cleaned_transcript = transcript
    if transcript_type == "台羅數字調":
        for bad_char, good_char in CLEAN_MAPPING.items():
            cleaned_transcript = cleaned_transcript.replace(bad_char, good_char)
        for c in cleaned_transcript:
            if c not in ACCEPTABLE_CHARS:
                print(f"{bad_count + 1}\t{c}\t: {cleaned_transcript}", file=verbose_fp)
                return None, bad_count + 1
        return cleaned_transcript, bad_count
    else:
        raise NotImplementedError
        return cleaned_transcript, -1


def main(args):
    ############
    #  Config  #
    ############
    # args
    transcript_type = "台羅數字調"  # 台羅 or 漢羅台文 or 台羅數字調
    wav_type = "condenser"
    TAT_root = args.TAT_root
    output_root = args.output_root

    # paths
    TAT_root = Path(TAT_root).resolve()
    output_root = Path(output_root).resolve()
    output_path = output_root / f"{TAT_root.name}.csv"

    TAT_txt_dir = TAT_root / "json"
    TAT_wav_dir = TAT_root / wav_type / "wav"

    # data list
    TAT_txt_list = list(TAT_txt_dir.rglob("*.json"))
    TAT_wav_list = [get_wav_from_txt(txt_path, TAT_wav_dir) for txt_path in tqdm(TAT_txt_list)]

    assert len(TAT_txt_list) == len(TAT_wav_list)

    tqdm.pandas()
    TAT_df = pd.DataFrame(
        {
            "json_path": TAT_txt_list,
            "wav_path": TAT_wav_list,
        }
    )
    get_transcript = partial(get_transcription_from_json, transcript_type=transcript_type)
    TAT_df["transcription"] = TAT_df["json_path"].map(get_transcript)

    bad_count = 0
    output_buffer = []
    for idx, data in TAT_df[["wav_path", "transcription"]].iterrows():
        wav_path = data["wav_path"]
        transcript = data["transcription"]
        result, bad_count = validate_transcription(transcript, transcript_type, bad_count)
        if result is not None:
            output_buffer.append(
                [
                    wav_path,
                    result,
                ]
            )

    pd.DataFrame(output_buffer).to_csv(output_path, index=None, header=["path", "text"])
    print("Output at", output_path)


import pandas as pd
from pathlib import Path
from tqdm import tqdm
from functools import partial
import argparse

def get_wav_path_from_id(wav_dir, file_id):
    # 這裡假設 WAV 文件命名為 id 的數字後接 .wav，例如 1.wav
    return wav_dir / f"{file_id}.wav"

def clean_text(txt):
    # 這裡可以根據實際需求增加清洗文本的邏輯
    CLEAN_MAPPING = {
        "﹖": "?",
        "！": "!",
        "％": "%",
        "（": "(",
        "）": ")",
        "，": ",",
        "：": ":",
        "；": ";",
        "？": "?",
        "—": "--",
        "─": "-",
    }
    for bad_char, good_char in CLEAN_MAPPING.items():
        txt = txt.replace(bad_char, good_char)
    return txt

def main(args):
    # Config
    TAT_root = Path(args.TAT_root).resolve()
    output_root = Path(args.output_root).resolve()
    if not output_root.exists():
        output_root.mkdir(parents=True)
    
    if args.test:
        wav_dir = TAT_root
        output_path = output_root / f"{TAT_root.name}.csv"

        # 讀取整個資料夾的 WAV 文件
        wav_list = list(wav_dir.glob("*.wav"))
        df = pd.DataFrame(wav_list, columns=['path'])
        # 將檔名設為 text
        df['text'] = df['path'].apply(lambda x: "_"+x.stem)
        # 輸出到新的 CSV 文件
        df.to_csv(output_path, index=False)

    else:
        
        if args.toneless:
            csv_file = TAT_root / "text-toneless.csv"
            output_path = output_root / f"{TAT_root.name}-toneless"
        else:
            csv_file = TAT_root / "text.csv"
            output_path = output_root / f"{TAT_root.name}"

        if args.noisy:
            wav_dir = TAT_root / "noisy_sound_6"
            output_path = output_path.with_name(output_path.name + "-noisy_6")
        else:
            wav_dir = TAT_root / "sound"

        output_path = output_path.with_suffix(".csv")
        # 讀取 CSV 文件
        df = pd.read_csv(csv_file)

        # 匹配 WAV 文件
        df['path'] = df['id'].apply(lambda x: get_wav_path_from_id(wav_dir, x))
        
        # 文本清洗
        df['text'] = df['text'].apply(clean_text)

        # 輸出到新的 CSV 文件
        df[['path', 'text']].to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--TAT_root", type=str, required=True, help="Root directory of the dataset")
    parser.add_argument("--output_root", type=str, default="./processed_data", help="Directory to save the processed output")
    parser.add_argument("--toneless", action="store_true", help="Whether to remove tone in the transcription")
    parser.add_argument("--noisy", action="store_true", help="Whether to add noise to the audio")
    parser.add_argument("--test", action="store_true", help="Whether to process the test set")
    args = parser.parse_args()
    main(args)