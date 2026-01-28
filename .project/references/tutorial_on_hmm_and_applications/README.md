# A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition

**Author:** Lawrence R. Rabiner

**Source:** Proceedings of the IEEE, Vol. 77, No. 2, February 1989

**PDF File:** `tutorial on hmm and applications.pdf`

---

## Status

⚠️ **Cannot extract text** - This PDF appears to be image-based (scanned from the 1989 IEEE Proceedings). OCR would be required for text extraction.

---

## About This Paper

This is the seminal tutorial on Hidden Markov Models by Rabiner, widely cited (~65,000+ citations) as the foundational reference for HMM theory and applications.

### Key Topics Covered

1. **Discrete Markov Processes** - States, transitions, observations
2. **Hidden Markov Models** - Observable outputs vs hidden states
3. **Three Basic Problems of HMMs:**
   - **Evaluation:** $P(O|\lambda)$ - probability of observation sequence
   - **Decoding:** Find optimal state sequence (Viterbi algorithm)
   - **Learning:** Adjust model parameters $\lambda$ to maximize $P(O|\lambda)$ (Baum-Welch)
4. **Types of HMMs** - Ergodic, left-right, continuous observation densities
5. **Speech Recognition Applications**

### Relevance to emic

This is a foundational reference for understanding the relationship between:
- Hidden Markov Models (HMMs)
- ε-machines (unifilar HMMs with causal state structure)
- Spectral learning algorithms

The ε-machine is a special case of an HMM where the hidden states have a precise predictive interpretation (causal states).

---

## Alternative Sources

The full text is available from:
- IEEE Xplore: https://ieeexplore.ieee.org/document/18626
- Many university repositories have text versions

---

## Citation

```bibtex
@article{rabiner1989tutorial,
  title={A tutorial on hidden Markov models and selected applications in speech recognition},
  author={Rabiner, Lawrence R},
  journal={Proceedings of the IEEE},
  volume={77},
  number={2},
  pages={257--286},
  year={1989},
  publisher={IEEE}
}
```
