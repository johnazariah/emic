# Run Experiment Session

This prompt guides an interactive experiment session for emic. When invoked, Copilot will walk through the steps of setting up, running, and documenting an experiment.

## Workflow

### Step 1: Create Experiment Worktree

First, I'll help you create a dedicated git worktree for this experiment:

1. **Ask for experiment name**: Short, descriptive (e.g., "cssr-convergence-2026-01")
2. **Create worktree**: `git worktree add worktrees/experiments/<name> -b experiment/<name>`
3. **Switch context** to the new worktree

### Step 2: Capture Intent (Optional)

Ask if they want to document the experiment's purpose:
- What hypothesis are you testing?
- What do you expect to observe?
- Any relevant background?

Create `experiments/runs/<name>/intent.md` with their response.

### Step 3: Configure Experiment

Help them choose:
- **Experiment type**: accuracy, convergence, scalability, or custom
- **Quick mode?**: Reduced sample sizes for faster iteration
- **Custom config?**: Override default parameters

### Step 4: Run Experiment

Execute the experiment:
```bash
cd /workspace/worktrees/experiments/<name>
emic-experiment <type> --output-dir experiments/runs/<name>
```

For long runs, offer sharding:
```bash
emic-experiment <type> --parallel 4 --output-dir experiments/runs/<name>
```

### Step 5: Generate Summary Statistics

After the run completes:
1. Read `experiments/runs/<name>/results.parquet`
2. Compute summary statistics (accuracy, mean errors, timing)
3. Generate a `summary.md` with key findings

### Step 6: Prepare Commit

Stage the experiment files:
```bash
git add experiments/runs/<name>/
```

Show what will be committed and ask if they want to:
- Review the results first
- Add conclusions to the summary
- Commit now and merge later

## Key Commands

```bash
# List available experiments
emic-experiment --list

# Run with verbose output
emic-experiment accuracy

# Run in quick mode
emic-experiment accuracy --quick

# Run with parallelism
emic-experiment accuracy --parallel 4

# Combine shard results
emic-experiment --combine experiments/runs/<name>/
```

## Output Structure

```
experiments/runs/<name>/
├── intent.md           # Why this experiment (optional)
├── config.yaml         # Configuration used (auto-generated)
├── metadata.yaml       # Runtime info (git, timing)
├── results.parquet     # Raw benchmark data
└── summary.md          # Summary statistics (auto-generated)
```

## Example Session

```
User: I want to run an experiment to validate CSSR convergence

Copilot: Let's set up your experiment!

1. What would you like to name this experiment?
   Suggestion: cssr-convergence-validation

User: cssr-convergence-jan26

Copilot: Creating worktree at worktrees/experiments/cssr-convergence-jan26...
   ✓ Worktree created
   ✓ Switched to branch experiment/cssr-convergence-jan26

2. Would you like to document your intent? (optional)
   What hypothesis are you testing?

User: Testing that CSSR converges to correct state count for N > 5000

Copilot: ✓ Saved to experiments/runs/cssr-convergence-jan26/intent.md

3. Which experiment would you like to run?
   - accuracy (recommended for validation)
   - convergence
   - scalability

User: accuracy

Copilot: Running accuracy experiment...
   ████████████████████ 100% (36/36 runs)
   ✓ Complete in 45.2s

4. Generating summary...
   - State count accuracy: 100% (all correct)
   - Mean Cμ error: 0.015 ± 0.008
   - Mean hμ error: 0.003 ± 0.002

5. Ready to commit. Files staged:
   experiments/runs/cssr-convergence-jan26/
     ├── intent.md
     ├── metadata.yaml
     ├── results.parquet
     └── summary.md

   Would you like to review the results before committing?
```
