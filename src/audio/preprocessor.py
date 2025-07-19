"""
Audio preprocessing functionality for the Voice-to-Voice AI Assistant.
"""

import numpy as np
import librosa
from typing import Tuple, Optional
from ..config.constants import AUDIO_SETTINGS
from ..utils.error_handler import ErrorHandler

class AudioPreprocessor:
    """Handles audio preprocessing for better transcription quality."""
    
    def __init__(self):
        self.target_sample_rate = AUDIO_SETTINGS["DEFAULT_SAMPLE_RATE"]
    
    def preprocess_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int = AUDIO_SETTINGS["DEFAULT_SAMPLE_RATE"]
    ) -> Tuple[np.ndarray, int]:
        """
        Preprocess audio for optimal transcription quality.
        
        Args:
            audio_data: Raw audio data
            sample_rate: Original sample rate
            
        Returns:
            Tuple of (processed_audio, target_sample_rate)
        """
        try:
            # Resample to target sample rate if needed
            if sample_rate != self.target_sample_rate:
                audio_data = librosa.resample(
                    audio_data,
                    orig_sr=sample_rate,
                    target_sr=self.target_sample_rate
                )
                sample_rate = self.target_sample_rate
            
            # Remove DC offset
            audio_data = audio_data - np.mean(audio_data)
            
            # Normalize to prevent clipping
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                audio_data = audio_data / max_val * 0.95
            
            # Apply noise reduction (simple high-pass filter)
            audio_data = self._apply_noise_reduction(audio_data, sample_rate)
            
            return audio_data, sample_rate
            
        except Exception as e:
            ErrorHandler.handle_audio_error(e, "preprocessing")
            return audio_data, sample_rate
    
    def _apply_noise_reduction(
        self,
        audio_data: np.ndarray,
        sample_rate: int
    ) -> np.ndarray:
        """
        Apply simple noise reduction using high-pass filter.
        
        Args:
            audio_data: Audio data
            sample_rate: Sample rate
            
        Returns:
            Filtered audio data
        """
        try:
            # High-pass filter to remove low-frequency noise
            # Cutoff frequency of 80 Hz (typical for speech)
            cutoff_freq = 80
            nyquist = sample_rate / 2
            normalized_cutoff = cutoff_freq / nyquist
            
            # Apply high-pass filter
            filtered_audio = librosa.effects.preemphasis(
                audio_data,
                coef=normalized_cutoff
            )
            
            return filtered_audio
            
        except Exception as e:
            ErrorHandler.log_error(f"Noise reduction failed: {e}")
            return audio_data
    
    def enhance_audio_quality(
        self,
        audio_data: np.ndarray,
        sample_rate: int
    ) -> Tuple[np.ndarray, int]:
        """
        Apply additional audio enhancement techniques.
        
        Args:
            audio_data: Audio data
            sample_rate: Sample rate
            
        Returns:
            Tuple of (enhanced_audio, sample_rate)
        """
        try:
            # Apply spectral subtraction for noise reduction
            enhanced_audio = self._spectral_subtraction(audio_data, sample_rate)
            
            # Apply dynamic range compression
            enhanced_audio = self._compress_dynamic_range(enhanced_audio)
            
            return enhanced_audio, sample_rate
            
        except Exception as e:
            ErrorHandler.log_error(f"Audio enhancement failed: {e}")
            return audio_data, sample_rate
    
    def _spectral_subtraction(
        self,
        audio_data: np.ndarray,
        sample_rate: int
    ) -> np.ndarray:
        """
        Apply spectral subtraction for noise reduction.
        
        Args:
            audio_data: Audio data
            sample_rate: Sample rate
            
        Returns:
            Noise-reduced audio data
        """
        try:
            # Simple spectral subtraction
            # This is a basic implementation - more sophisticated methods exist
            
            # Compute spectrogram
            stft = librosa.stft(audio_data)
            magnitude = np.abs(stft)
            
            # Estimate noise from first 0.1 seconds
            noise_frames = int(0.1 * sample_rate / 512)  # Assuming 512 frame size
            noise_spectrum = np.mean(magnitude[:, :noise_frames], axis=1, keepdims=True)
            
            # Subtract noise spectrum
            cleaned_magnitude = magnitude - 0.5 * noise_spectrum
            cleaned_magnitude = np.maximum(cleaned_magnitude, 0.01 * magnitude)
            
            # Reconstruct audio
            cleaned_stft = stft * cleaned_magnitude / magnitude
            cleaned_audio = librosa.istft(cleaned_stft)
            
            return cleaned_audio
            
        except Exception as e:
            ErrorHandler.log_error(f"Spectral subtraction failed: {e}")
            return audio_data
    
    def _compress_dynamic_range(
        self,
        audio_data: np.ndarray,
        threshold: float = 0.7,
        ratio: float = 4.0
    ) -> np.ndarray:
        """
        Apply dynamic range compression.
        
        Args:
            audio_data: Audio data
            threshold: Compression threshold
            ratio: Compression ratio
            
        Returns:
            Compressed audio data
        """
        try:
            # Simple dynamic range compression
            magnitude = np.abs(audio_data)
            
            # Apply compression above threshold
            compressed = np.where(
                magnitude > threshold,
                threshold + (magnitude - threshold) / ratio,
                magnitude
            )
            
            # Preserve sign
            compressed_audio = np.sign(audio_data) * compressed
            
            return compressed_audio
            
        except Exception as e:
            ErrorHandler.log_error(f"Dynamic range compression failed: {e}")
            return audio_data
    
    def validate_audio_data(
        self,
        audio_data: np.ndarray,
        sample_rate: int
    ) -> bool:
        """
        Validate audio data quality.
        
        Args:
            audio_data: Audio data to validate
            sample_rate: Sample rate
            
        Returns:
            True if audio data is valid, False otherwise
        """
        try:
            # Check if audio data is not empty
            if len(audio_data) == 0:
                return False
            
            # Check if audio has sufficient amplitude
            if np.max(np.abs(audio_data)) < 0.01:
                return False
            
            # Check if sample rate is reasonable
            if sample_rate < 8000 or sample_rate > 48000:
                return False
            
            # Check for NaN or infinite values
            if np.any(np.isnan(audio_data)) or np.any(np.isinf(audio_data)):
                return False
            
            return True
            
        except Exception as e:
            ErrorHandler.log_error(f"Audio validation failed: {e}")
            return False
    
    def get_audio_statistics(
        self,
        audio_data: np.ndarray,
        sample_rate: int
    ) -> dict:
        """
        Get audio quality statistics.
        
        Args:
            audio_data: Audio data
            sample_rate: Sample rate
            
        Returns:
            Dictionary with audio statistics
        """
        try:
            duration = len(audio_data) / sample_rate
            rms = np.sqrt(np.mean(audio_data**2))
            peak = np.max(np.abs(audio_data))
            snr = 20 * np.log10(peak / (rms + 1e-10))
            
            return {
                'duration': duration,
                'sample_rate': sample_rate,
                'rms': rms,
                'peak': peak,
                'snr': snr,
                'is_valid': self.validate_audio_data(audio_data, sample_rate)
            }
            
        except Exception as e:
            ErrorHandler.log_error(f"Failed to get audio statistics: {e}")
            return {
                'duration': 0,
                'sample_rate': sample_rate,
                'rms': 0,
                'peak': 0,
                'snr': 0,
                'is_valid': False
            } 