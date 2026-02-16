# Publication Build System
#
# Usage:
#   make              Build all PDFs + arXiv tarballs
#   make pdf          Build PDFs only
#   make arxiv        Package arXiv tarballs (requires built PDFs)
#   make verify       Verify arXiv tarballs compile from source
#   make joss         Show JOSS build info (CI only)
#   make clean        Remove dist/ artifacts
#
#   make review       Build review paper PDF only
#   make techreport   Build technical report PDF only
#   make tutorial     Build tutorial PDF only
#
# Output: dist/
#   paper.pdf                          (from each paper dir)
#   arxiv-review-paper.tar.gz         (upload to arXiv)
#   arxiv-technical-report.tar.gz     (upload to arXiv)
#   arxiv-tutorial.tar.gz             (upload to arXiv)

.PHONY: all pdf arxiv verify joss review techreport tutorial clean help

SHELL := /bin/bash
BUILD := ./build-all.sh

all:
	@$(BUILD) all

pdf:
	@$(BUILD) pdf

arxiv:
	@$(BUILD) arxiv

verify:
	@$(BUILD) verify

joss:
	@$(BUILD) joss

review:
	@$(BUILD) review

techreport:
	@$(BUILD) techreport

tutorial:
	@$(BUILD) tutorial

clean:
	@$(BUILD) clean

help:
	@echo "Targets: all pdf arxiv verify joss review techreport tutorial clean"
	@echo "Run 'make' to build everything. Output goes to dist/."
