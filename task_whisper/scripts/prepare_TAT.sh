# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/train --output_root ../processed_data
# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/val --output_root ../processed_data
# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/tiny_train --output_root ../processed_data
# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/tiny_val --output_root ../processed_data

# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/train --output_root ../processed_data --toneless 
# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/val --output_root ../processed_data --toneless 
# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/tiny_train --output_root ../processed_data --toneless
# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/tiny_val --output_root ../processed_data --toneless

# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/test/test --output_root ../processed_data --test

python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/train --output_root ../processed_data --toneless --noisy
# python prepare_TAT.py --TAT_root /mnt/sda1/htchang/DL/HW1/Taiwanese-Whisper/data/val --output_root ../processed_data --toneless --noisy