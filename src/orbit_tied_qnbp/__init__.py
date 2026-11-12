"""Orbit-Tied Quantized Neural Belief Propagation (QNBP) Library.

A high-performance quantum error correction library for real-time
sliding-window decoding of bivariate-bicycle (BB) codes.
"""

__version__ = "1.0.0"
__author__ = "Md. Nazmul, Musrat Jahan Gungun, Maheli Ahmed"
__email__ = "nazmulhas36@gmail.com"

from orbit_tied_qnbp.circuits.bivariate_bicycle import BivariateBicycleCode
from orbit_tied_qnbp.data.dem_graph import DemGraph
from orbit_tied_qnbp.decoder.baselines import DecodeResult, MinSumDecoder, RelayBPDecoder
from orbit_tied_qnbp.decoder.integer_reference import IntegerQNBP
from orbit_tied_qnbp.decoder.orbits import DemOrbitManager
from orbit_tied_qnbp.decoder.qnbp import OrbitTiedQNBP
from orbit_tied_qnbp.decoder.quantization import (
    CanonicalSignedDigit,
    PowerOfTwoQuantizer,
)
from orbit_tied_qnbp.decoder.sliding_window import (
    ConfidenceGate,
    SlidingWindowManager,
    TraceDrivenQueueSimulator,
)
from orbit_tied_qnbp.decoder.streaming_window_decoder import StreamingSlidingWindowDecoder

__all__ = [
    "__version__",
    "BivariateBicycleCode",
    "DemGraph",
    "DemOrbitManager",
    "OrbitTiedQNBP",
    "IntegerQNBP",
    "CanonicalSignedDigit",
    "PowerOfTwoQuantizer",
    "MinSumDecoder",
    "RelayBPDecoder",
    "ConfidenceGate",
    "SlidingWindowManager",
    "TraceDrivenQueueSimulator",
    "StreamingSlidingWindowDecoder",
    "DecodeResult",
]
