# # #!/usr/bin/env python3

# # # Copyright 2016  Allen Guo

# # # Licensed under the Apache License, Version 2.0 (the "License");
# # # you may not use this file except in compliance with the License.
# # # You may obtain a copy of the License at
# # #
# # #  http://www.apache.org/licenses/LICENSE-2.0
# # #
# # # THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# # # KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
# # # WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# # # MERCHANTABLITY OR NON-INFRINGEMENT.
# # # See the Apache 2 License for the specific language governing permissions and
# # # limitations under the License.

# # import os
# # import re
# # import sys

# # if len(sys.argv) != 3:
# #     print("Usage: python data_prep.py [an4_root] [sph2pipe]")
# #     sys.exit(1)
# # an4_root = sys.argv[1]
# # sph2pipe = sys.argv[2]

# # sph_dir = {"train": "an4_clstk", "test": "an4test_clstk"}

# # for x in ["train", "test"]:
# #     with open(
# #         os.path.join(an4_root, "etc", "an4_" + x + ".transcription")
# #     ) as transcript_f, open(os.path.join("data", x, "text"), "w") as text_f, open(
# #         os.path.join("data", x, "wav.scp"), "w"
# #     ) as wav_scp_f, open(
# #         os.path.join("data", x, "utt2spk"), "w"
# #     ) as utt2spk_f:
# #         text_f.truncate()
# #         wav_scp_f.truncate()
# #         utt2spk_f.truncate()

# #         lines = sorted(transcript_f.readlines(), key=lambda s: s.split(" ")[0])
# #         for line in lines:
# #             line = line.strip()
# #             if not line:
# #                 continue
# #             words = re.search(r"^(.*) \(", line).group(1)
# #             if words[:4] == "<s> ":
# #                 words = words[4:]
# #             if words[-5:] == " </s>":
# #                 words = words[:-5]
# #             source = re.search(r"\((.*)\)", line).group(1)
# #             pre, mid, last = source.split("-")
            
# #             utt_id = "-".join([mid, pre, last])

# #             text_f.write(utt_id + " " + words + "\n")
# #             wav_scp_f.write(
# #                 utt_id
# #                 + " "
# #                 + sph2pipe
# #                 + " -f wav -p -c 1 "
# #                 + os.path.join(an4_root, "wav", sph_dir[x], mid, source + ".sph")
# #                 + " |\n"
# #             )
# #             utt2spk_f.write(utt_id + " " + mid + "\n")


# # # def remove_commas(input_file_path, output_file_path):
# # #     """
# # #     Read the input file, remove all commas, and write the output to a new file.
    
# # #     Parameters:
# # #         input_file_path (str): The path to the input file.
# # #         output_file_path (str): The path to the output file where the result should be saved.
# # #     """
# # #     try:
# # #         with open(input_file_path, 'r', encoding='utf-8') as file:
# # #             content = file.read()

# # #         # Remove all commas
# # #         content_no_commas = content.replace(',', ' ')

# # #         with open(output_file_path, 'w', encoding='utf-8') as file:
# # #             file.write(content_no_commas)

# # #         print("Commas have been removed successfully.")
    
# # #     except Exception as e:
# # #         print(f"An error occurred: {e}")

# # # # Example usage
# # # input_file = "/mnt/maniac/data/train/train-toneless.txt"  # Update this path to the input file
# # # output_file = "/mnt/maniac/espnet/egs2/HW1/asr1/data/train/text.txt"  # Update this path for the output file

# # # remove_commas(input_file, output_file)
# # # print("Done!")

# import os

# # 定義路徑
# input_directory = '/mnt/maniac/espnet/egs2/HW1/asr1/downloads/an4/wav/an4test_clstk'
# output_file = '/mnt/maniac/espnet/egs2/HW1/asr1/data/test/wav.scp'
# sph2pipe_path = 'sph2pipe'  # sph2pipe 工具的路徑，如果在PATH中已設置 sph2pipe 可執行檔案，直接用 'sph2pipe'


# # 初始化一個列表來保存所有行
# lines = []

# # 遍歷目錄中的所有文件
# for filename in os.listdir(input_directory):
#     if filename.endswith(".sph"):  # 確保處理 .sph 文件
#         # 構建 utt_id 和 path
#         utt_id = filename.split('.')[0]  # 假設檔案名稱前綴為 utt_id
#         full_path = os.path.join(input_directory, filename)
        
#         # 格式化行並添加到列表
#         line = f"{utt_id} {sph2pipe_path} -f wav -p -c 1 {full_path} |\n"
#         lines.append((int(utt_id), line))

# # 對所有行按數字的 utt_id 排序
# lines.sort(key=lambda x: x[0])

# # 開啟輸出文件並寫入排序後的行
# with open(output_file, 'w', encoding='utf-8') as f:
#     for _, line in lines:
#         f.write(line)

# print(f"File '{output_file}' has been written with all .sph files from '{input_directory}', sorted by utt_id.")

# Define the input and output file paths
# input_file_path = '/mnt/maniac/espnet/egs2/HW1/asr1/data/test/wav.scp'
# output_file_path = '/mnt/maniac/espnet/egs2/HW1/asr1/data/test/wav.scp'

# # Read the content of the input file
# with open(input_file_path, 'r') as file:
#     lines = file.readlines()

# # Sort the lines alphabetically based on the second column
# sorted_lines = sorted(lines, key=lambda x: x.split()[0])

# # Write the sorted content to the output file
# with open(output_file_path, 'w') as file:
#     file.writelines(sorted_lines)

# print(f"File sorted and saved to: {output_file_path}")
# Specify the path to the input and output files
import os

# 指定輸入和輸出文件的路徑
input_path = '/mnt/maniac/espnet/egs2/HW1/asr1/exp/asr_train_asr_demo_transformer_raw_bpe74/decode_asr_asr_model_valid.acc.ave/org/test/logdir/output.1/1best_recog/text'
output_path = '/mnt/maniac/output.csv'

# 檢查輸入路徑是否存在
if not os.path.exists(input_path):
    raise SystemExit(f"Error: Input file does not exist at {input_path}")

# 開啟輸入文件和輸出文件
with open(input_path, 'r', encoding='utf-8') as infile, \
     open(output_path, 'w', encoding='utf-8') as outfile:
    # 讀取輸入文件的每一行
    for line in infile:
        # 找到第一個空格的位置並用逗號替換
        first_space_index = line.find(' ')
        if first_space_index != -1:
            # 構造新的行內容，並寫入到輸出文件
            new_line = line[:first_space_index] + ',' + line[first_space_index+1:]
            outfile.write(new_line)

print(f"Data has been processed and output to {output_path}.")
