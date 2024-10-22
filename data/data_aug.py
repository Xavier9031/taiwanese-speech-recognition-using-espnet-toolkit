import glob, os
import numpy as np
from scipy.io import wavfile
from audiomentations import Compose, SomeOf, AddGaussianNoise, AddGaussianSNR, TimeStretch, PitchShift, Shift, AddBackgroundNoise, AddShortNoises, PolarityInversion, ApplyImpulseResponse
from audiomentations.core.audio_loading_utils import load_sound_file
import nlpaug.augmenter.audio as naa
import nlpaug.flow as naf
import argparse

parser = argparse.ArgumentParser(description='Data Augmentation')
parser.add_argument('--input', type=str, default='train/sound', help='Input path')
parser.add_argument('--output', type=str, default='train/noisy_sound', help='Output path')

args = parser.parse_args()

InPath = args.input
OutPath = args.output
if not os.path.exists(OutPath):
    os.makedirs(OutPath)
sr = 22050

augment1 = naf.Sometimes([
    naa.VtlpAug(sampling_rate=sr, zone=(0.0, 1.0), coverage=1.0, factor=(0.9, 1.1)),
    ], aug_p=0.4)

augment2 = Compose([
    AddGaussianSNR(min_snr_in_db=10, max_snr_in_db=30, p=0.2),
    TimeStretch(min_rate=0.8, max_rate=1.2, leave_length_unchanged=False, p=0.4),
    PitchShift(min_semitones=-4, max_semitones=4, p=0.4),
    AddBackgroundNoise(
        sounds_path="audiomentations/demo/background_noises",
        min_snr_in_db=10,
        max_snr_in_db=30.0,
        p=0.4),
    AddShortNoises(
    sounds_path="audiomentations/demo/short_noises",
    min_snr_in_db=10,
    max_snr_in_db=30.0,
    noise_rms="relative_to_whole_input",
    min_time_between_sounds=2.0,
    max_time_between_sounds=8.0,
    p=0.3),
    ApplyImpulseResponse(
            ir_path="audiomentations/demo/ir", p=0.4
        )
])

for file in os.listdir(InPath):
    if file.endswith(".wav"):
        samples, sample_rate = load_sound_file(
            os.path.join(InPath, file), sample_rate=None
        )
        print("#", os.path.join(InPath, file), sample_rate, len(samples))
        # Augment/transform/perturb the audio data
        augmented_samples1 = augment1.augment(samples)
        augmented_samples2 = augment2(samples=augmented_samples1[0], sample_rate=sample_rate)
        wavfile.write(
            os.path.join(OutPath, file), rate=sample_rate, data=augmented_samples2
        )
        print()
