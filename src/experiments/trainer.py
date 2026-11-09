"""Supervised training loop and model checkpointing for QNBP decoders.

Implements AdamW optimization with multi-iteration supervision on Stim shots.
"""

from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import torch
import torch.optim as optim

from src.decoder.qnbp import OrbitTiedQNBP


class QnbpTrainer:
    """Trains OrbitTiedQNBP models with multi-iteration supervision."""

    def __init__(
        self,
        model: OrbitTiedQNBP,
        lr: float = 0.01,
        weight_decay: float = 1e-4,
        device: str = "cpu",
    ) -> None:
        self.model = model.to(device)
        self.device = device
        self.optimizer = optim.AdamW(
            model.parameters(), lr=lr, weight_decay=weight_decay
        )

    def train_epoch(
        self,
        train_syndromes: np.ndarray,
        train_observables: np.ndarray,
        batch_size: int = 64,
        loss_type: str = "log_domain_obs",
    ) -> float:
        """Trains one epoch over the dataset."""
        self.model.train()
        n_samples = len(train_syndromes)
        indices = np.random.permutation(n_samples)
        total_loss = 0.0
        num_batches = 0

        for start in range(0, n_samples, batch_size):
            b_idx = indices[start : start + batch_size]
            syn_b = torch.from_numpy(train_syndromes[b_idx]).to(self.device)
            obs_b = torch.from_numpy(train_observables[b_idx]).to(self.device)

            self.optimizer.zero_grad()
            outputs = self.model(syn_b)
            loss = self.model.compute_loss(outputs, obs_b, syn_b, loss_type=loss_type)
            loss.backward()

            # Gradient clipping to prevent exploding gradients
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()

            total_loss += float(loss.item())
            num_batches += 1

        return total_loss / max(1, num_batches)

    def evaluate(
        self,
        val_syndromes: np.ndarray,
        val_observables: np.ndarray,
        batch_size: int = 128,
    ) -> Dict[str, float]:
        """Evaluates logical frame error rate on validation shots."""
        self.model.eval()
        n_samples = len(val_syndromes)
        num_errors = 0
        obs_matrix = self.model.obs_matrix.cpu().numpy()

        with torch.no_grad():
            for start in range(0, n_samples, batch_size):
                syn_b = torch.from_numpy(val_syndromes[start : start + batch_size]).to(self.device)
                true_b = val_observables[start : start + batch_size]

                outputs = self.model(syn_b)
                _, hard_corr = outputs[-1]
                hard_np = hard_corr.cpu().numpy()

                pred_obs = (hard_np @ obs_matrix.T) % 2
                frame_errors = np.any(pred_obs != true_b, axis=1)
                num_errors += int(np.sum(frame_errors))

        ler = num_errors / max(1, n_samples)
        return {"ler": ler, "errors": num_errors, "total": n_samples}
