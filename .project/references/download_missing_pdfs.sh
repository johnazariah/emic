#!/bin/bash
# Script to download the correct PDFs for mislabeled/corrupted references
# Run from the .project/references directory

set -e

echo "=== Downloading missing/mislabeled PDFs ==="
echo ""

# Directory for this script
REFS_DIR="/workspace/.project/references"
cd "$REFS_DIR"

# 1. Gu 2012 - Quantum mechanics can reduce the complexity of classical models
# arXiv:1102.1994
echo "1. Downloading gu2012quantum (arXiv:1102.1994)..."
rm -f gu2012quantum.pdf
curl -L -o gu2012quantum.pdf "https://arxiv.org/pdf/1102.1994.pdf"
echo "   ✓ Downloaded: Occam's Quantum Razor (Gu, Wiesner, Rieper, Vedral)"

# 2. Boots 2011 - Closing the learning-planning loop with PSRs
# arXiv:0912.2385 (submitted 2009, published ~2011)
echo "2. Downloading boots2011closing (arXiv:0912.2385)..."
rm -f boots2011closing.pdf
curl -L -o boots2011closing.pdf "https://arxiv.org/pdf/0912.2385.pdf"
echo "   ✓ Downloaded: Closing the Learning-Planning Loop (Boots, Siddiqi, Gordon)"

# 3. Hsu 2012 - A Spectral Algorithm for Learning Hidden Markov Models
# arXiv:0811.4413 (JCSS 2012)
echo "3. Downloading hsu2012spectral (arXiv:0811.4413)..."
rm -f hsu2012spectral.pdf
curl -L -o hsu2012spectral.pdf "https://arxiv.org/pdf/0811.4413.pdf"
echo "   ✓ Downloaded: A Spectral Algorithm for Learning HMMs (Hsu, Kakade, Zhang)"

# 4. James 2011 - Anatomy of a Bit
# arXiv:1105.2988
echo "4. Downloading james2011anatomy (arXiv:1105.2988)..."
rm -f james2011anatomy.pdf
curl -L -o james2011anatomy.pdf "https://arxiv.org/pdf/1105.2988.pdf"
echo "   ✓ Downloaded: Anatomy of a Bit (James, Ellison, Crutchfield)"

# 5. Shalizi 2001 - Computational Mechanics paper (not thesis)
# arXiv:cond-mat/9907176 - the correct paper
echo "5. Downloading shalizi2001computational (arXiv:cond-mat/9907176)..."
rm -f shalizi2001computational.pdf
curl -L -o shalizi2001computational.pdf "https://arxiv.org/pdf/cond-mat/9907176.pdf"
echo "   ✓ Downloaded: Computational Mechanics (Shalizi & Crutchfield)"

echo ""
echo "=== Papers that need manual download (not freely available) ==="
echo ""
echo "6. crutchfield1989inferring"
echo "   Title: Inferring Statistical Complexity"
echo "   Authors: Crutchfield & Young (1989)"
echo "   Journal: Physical Review Letters 63, 105"
echo "   DOI: https://doi.org/10.1103/PhysRevLett.63.105"
echo "   → Available via: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.63.105"
echo "   → Or try: https://www.academia.edu/download/86860578/fulltext.pdf"
echo ""

echo "7. grassberger1986toward"
echo "   Title: Toward a Quantitative Theory of Self-Generated Complexity"
echo "   Authors: Grassberger (1986)"
echo "   Journal: International Journal of Theoretical Physics 25, 907-938"
echo "   DOI: https://doi.org/10.1007/BF00668821"
echo "   → Available via institutional access"
echo ""

echo "8. rabiner1989tutorial"
echo "   Title: A Tutorial on Hidden Markov Models and Selected Applications"
echo "   Authors: Rabiner (1989)"
echo "   Journal: Proceedings of the IEEE 77(2), 257-286"
echo "   DOI: https://doi.org/10.1109/5.18626"
echo "   → Try: https://web.ece.ucsb.edu/Faculty/Rabiner/ece259/Reprints/tutorial%20on%20hmm%20and%20applications.pdf"
echo "   → Or: https://ieeexplore.ieee.org/document/18626"
echo ""

echo "=== Download complete! ==="
echo ""
echo "Re-extract the downloaded PDFs:"
echo "for pdf in gu2012quantum boots2011closing hsu2012spectral james2011anatomy shalizi2001computational; do"
echo "  rm -rf \"\${pdf}/\""
echo "  mkdir -p \"\${pdf}\""
echo "  pdftotext -layout \"\${pdf}.pdf\" \"\${pdf}/extracted.txt\""
echo "  echo \"Extracted: \${pdf}\""
echo "done"
