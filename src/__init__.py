"""Backward compatibility package forwarder for src.* imports."""

import sys
import orbit_tied_qnbp
import orbit_tied_qnbp.circuits as circuits
import orbit_tied_qnbp.data as data
import orbit_tied_qnbp.decoder as decoder
import orbit_tied_qnbp.experiments as experiments
import orbit_tied_qnbp.utils as utils

sys.modules["src.circuits"] = circuits
sys.modules["src.data"] = data
sys.modules["src.decoder"] = decoder
sys.modules["src.experiments"] = experiments
sys.modules["src.utils"] = utils
