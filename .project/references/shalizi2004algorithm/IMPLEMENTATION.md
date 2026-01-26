# CSSR Reference Implementation

The canonical CSSR implementation is maintained at:

- **GitHub**: https://github.com/stites/CSSR
- **Language**: C++
- **Original URL** (from paper): http://bactra.org/CSSR/ (now archived)

## History

The original implementation was by Cosma Shalizi and Kristina Shalizi at the University of Michigan. The stites/CSSR repository is a maintained fork of the original codebase.

## Relation to emic

The emic Python implementation (`emic.inference.CSSR`) follows the same algorithmic structure:

1. Build suffix tree from observed sequences
2. Compute predictive distributions for each suffix
3. Use chi-squared tests to compare distributions
4. Split states when distributions differ significantly
5. Optionally merge over-split states

Key differences in emic:
- Pure Python implementation (vs C++)
- Type-annotated, immutable data structures
- Optional post-merge step to reduce over-splitting
- Integration with other inference algorithms (Spectral, CSM, BSI, NSD)
