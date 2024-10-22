#!/usr/bin/env bash
set -e
set -u
set -o pipefail

./asr.sh \
        --stage 10 \
        --stop_stage 10 \
        --train_set train_dev \
        --valid_set train_nodev \
        --test_sets train_nodev \
        --nj 16 \
        --asr_config conf/train_asr_demo_transformer.yaml