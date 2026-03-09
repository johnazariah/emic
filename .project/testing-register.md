# Testing Register

A complete catalogue of every test in the emic test suite.

**Classification**:

- **Fact** — Verifies a deterministic, structural truth (e.g. "a frozen dataclass is immutable", "the Golden Mean machine has 2 states")
- **Theory** — Verifies a mathematical or analytical relationship derived from computational mechanics theory (e.g. "E ≤ Cμ always", "Golden Mean Cμ ≈ 0.918")
- **Property** — Verifies an invariant that should hold across inputs or configurations (e.g. "same seed → same output", "all algorithms agree on state count")

**Last updated**: 2026-03-09 · **Total tests**: 429

---

## Types (`tests/unit/test_states.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 1 | `test_basic_transition` | A Transition can be created with symbol, probability, and target | Fact |
| 2 | `test_probability_must_be_positive` | Transition rejects probability ≤ 0 | Fact |
| 3 | `test_probability_at_most_one` | Transition rejects probability > 1 | Fact |
| 4 | `test_immutable` | Transition is a frozen dataclass | Fact |
| 5 | `test_hashable` | Transition is hashable (can be used in sets/dicts) | Fact |
| 6 | `test_basic_state` | A CausalState can be created with id and transitions | Fact |
| 7 | `test_alphabet_property` | CausalState.alphabet returns symbols with transitions | Fact |
| 8 | `test_transition_distribution` | CausalState gives correct distribution over next states | Fact |
| 9 | `test_transition_distribution_missing_symbol` | KeyError raised for symbol with no transitions | Fact |
| 10 | `test_emission_distribution` | Emission distribution sums probabilities correctly | Fact |
| 11 | `test_next_states` | Get possible next states for a given symbol | Fact |
| 12 | `test_probabilities_sum_validation` | Transitions for same symbol cannot sum to > 1 | Fact |
| 13 | `test_immutable` (CausalState) | CausalState is a frozen dataclass | Fact |
| 14 | `test_empty_state` | A state with no transitions is valid (sink state) | Fact |

## Types — Probability (`tests/unit/test_probability.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 15 | `test_basic_distribution` | Distribution can be created with valid probabilities | Fact |
| 16 | `test_missing_symbol_returns_zero` | Querying absent symbol returns 0.0 | Fact |
| 17 | `test_probabilities_must_sum_to_one` | Distribution rejects probabilities not summing to 1 | Fact |
| 18 | `test_probabilities_in_valid_range` | Distribution rejects probabilities outside [0, 1] | Fact |
| 19 | `test_support` | Support returns symbols with non-zero probability | Fact |
| 20 | `test_entropy_uniform` | Entropy of uniform binary distribution is 1 bit | Theory |
| 21 | `test_entropy_deterministic` | Entropy of deterministic distribution is 0 | Theory |
| 22 | `test_entropy_calculation` | Entropy computation matches hand calculation | Theory |
| 23 | `test_uniform` | Uniform distribution has equal probabilities | Fact |
| 24 | `test_uniform_empty_raises` | Uniform over empty set raises ValueError | Fact |
| 25 | `test_deterministic` | Deterministic distribution puts all mass on one symbol | Fact |
| 26 | `test_iteration` | Distribution is iterable over its support | Fact |
| 27 | `test_len` | Length equals size of support | Fact |
| 28 | `test_immutable` (Distribution) | Distribution is a frozen dataclass | Fact |

## Types — Alphabet (`tests/unit/test_alphabet.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 29 | `test_binary_alphabet` | Binary alphabet contains 0 and 1 | Fact |
| 30 | `test_from_symbols` | Alphabet can be created from a set of symbols | Fact |
| 31 | `test_iteration` | Alphabet is iterable | Fact |
| 32 | `test_symbols_property` | Symbols property returns frozenset | Fact |
| 33 | `test_immutable` | Alphabet is immutable | Fact |
| 34 | `test_hashable` | Alphabet is hashable | Fact |
| 35 | `test_equality` | Alphabets with same symbols are equal | Fact |
| 36 | `test_empty_alphabet` | Empty alphabet is valid | Fact |

## Types — Machine (`tests/unit/test_machine.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 37 | `test_basic_machine` | EpsilonMachine can be built via builder | Fact |
| 38 | `test_get_state` | get_state retrieves state by ID | Fact |
| 39 | `test_get_state_not_found` | get_state raises KeyError for missing state | Fact |
| 40 | `test_is_unifilar` | Machine with deterministic (state, symbol) → target is unifilar | Fact |
| 41 | `test_transition_matrix` | transition_matrix returns correct mapping | Fact |
| 42 | `test_invalid_start_state` | Construction rejects unknown start state | Fact |
| 43 | `test_invalid_stationary_distribution` | Construction rejects stationary dist over unknown states | Fact |
| 44 | `test_unifilarity_violation` | Construction rejects non-unifilar machines | Fact |
| 45 | `test_is_ergodic_not_implemented` | is_ergodic raises NotImplementedError (unimplemented) | Fact |
| 46 | `test_fluent_api` | Builder supports method chaining | Fact |
| 47 | `test_auto_creates_states` | add_transition auto-creates source and target states | Fact |
| 48 | `test_auto_creates_alphabet` | add_transition auto-adds symbol to alphabet | Fact |
| 49 | `test_missing_start_state` | Build without start state raises ValueError | Fact |
| 50 | `test_default_stationary_distribution` | Builder computes stationary distribution if not provided | Fact |
| 51 | `test_golden_mean_machine` | Builder can construct the Golden Mean ε-machine | Theory |

## Analysis (`tests/unit/test_analysis.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 52 | `test_state_count` | state_count returns correct number | Fact |
| 53 | `test_transition_count` | transition_count returns correct number | Fact |
| 54 | `test_topological_complexity` | topological_complexity is log₂(number of states) | Theory |
| 55 | `test_statistical_complexity_single_state` | Single-state machine has Cμ = 0 | Theory |
| 56 | `test_statistical_complexity_golden_mean` | Golden Mean has Cμ ≈ 0.918 (= H(2/3, 1/3)) | Theory |
| 57 | `test_entropy_rate_fair_coin` | Fair coin has hμ = 1 bit | Theory |
| 58 | `test_entropy_rate_biased_coin` | Biased coin (p=0.9) has hμ ≈ 0.47 | Theory |
| 59 | `test_entropy_rate_periodic_is_zero` | Periodic process has hμ = 0 | Theory |
| 60 | `test_excess_entropy_iid_is_zero` | IID process has E = 0 | Theory |
| 61 | `test_excess_entropy_golden_mean` | Golden Mean has E ≈ 0.252 | Theory |
| 62 | `test_excess_entropy_less_than_complexity` | E ≤ Cμ always (fundamental bound) | Theory |
| 63 | `test_excess_entropy_periodic_equals_complexity` | Periodic process has E = Cμ (χ = 0) | Theory |
| 64 | `test_excess_entropy_even_process` | Even Process has E ≈ Cμ (χ ≈ 0) | Theory |
| 65 | `test_crypticity_golden_mean` | Golden Mean has χ ≈ 0.667 (= hμ) | Theory |
| 66 | `test_crypticity_iid_is_zero` | IID process has χ = 0 | Theory |
| 67 | `test_crypticity_periodic_is_zero` | Periodic process has χ = 0 | Theory |
| 68 | `test_analyze_returns_summary` | analyze() returns an AnalysisSummary | Fact |
| 69 | `test_summary_has_all_fields` | Summary populates all expected fields with correct signs | Fact |
| 70 | `test_summary_to_dict` | to_dict() returns dictionary with expected keys | Fact |
| 71 | `test_summary_str` | String representation is informative | Fact |

## Sources — Protocol (`tests/unit/test_sources_protocol.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 72 | `test_can_iterate_minimal_implementation` | SequenceSource protocol: minimal impl is iterable | Fact |
| 73 | `test_has_alphabet` | SequenceSource protocol: has alphabet property | Fact |
| 74 | `test_biased_coin_source_can_iterate` | BiasedCoinSource satisfies SequenceSource | Fact |
| 75 | `test_has_seed_property` | SeededSource protocol: has seed property | Fact |
| 76 | `test_has_with_seed` | SeededSource protocol: has with_seed method | Fact |
| 77 | `test_biased_coin_source_has_seed` | BiasedCoinSource satisfies SeededSource | Fact |
| 78 | `test_biased_coin_source_with_seed` | with_seed returns new source with given seed | Fact |

## Sources — Base (`tests/unit/test_sources_base.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 79 | `test_seed_property` | Seed is stored and retrievable | Fact |
| 80 | `test_default_seed_is_none` | Default seed is None | Fact |
| 81 | `test_iter_yields_symbols` | __iter__ yields symbols from the source | Fact |
| 82 | `test_alphabet_property` | Alphabet property returns the symbol set | Fact |
| 83 | `test_rng_is_seeded_reproducibly` | Seeded RNG produces reproducible values | Property |
| 84 | `test_rng_differs_with_different_seeds` | Different seeds produce different values | Property |
| 85 | `test_pipeline_with_take_transform` | >> operator works with TakeN | Fact |
| 86 | `test_pipeline_with_skip_transform` | >> operator works with SkipN | Fact |
| 87 | `test_pipeline_chaining` | Multiple transforms can be chained with >> | Fact |

## Sources — Synthetic (`tests/unit/test_sources_synthetic.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 88 | `GoldenMean::test_generates_binary_symbols` | Output contains only 0 and 1 | Fact |
| 89 | `GoldenMean::test_no_consecutive_ones` | No two consecutive 1s appear | Theory |
| 90 | `GoldenMean::test_reproducibility_with_seed` | Same seed → same sequence | Property |
| 91 | `GoldenMean::test_different_seeds_produce_different_sequences` | Different seeds → different sequences | Property |
| 92 | `GoldenMean::test_true_machine_returns_epsilon_machine` | true_machine returns valid EpsilonMachine | Fact |
| 93 | `GoldenMean::test_true_machine_is_unifilar` | True machine passes unifilarity validation | Theory |
| 94 | `GoldenMean::test_invalid_p_zero` | p=0 raises ValueError | Fact |
| 95 | `GoldenMean::test_invalid_p_one` | p=1 raises ValueError | Fact |
| 96 | `GoldenMean::test_invalid_p_negative` | Negative p raises ValueError | Fact |
| 97 | `GoldenMean::test_with_seed_returns_new_source` | with_seed returns new source | Fact |
| 98 | `EvenProcess::test_generates_binary_symbols` | Output contains only 0 and 1 | Fact |
| 99 | `EvenProcess::test_even_ones_between_zeros` | Even number of 1s between each pair of 0s | Theory |
| 100 | `EvenProcess::test_reproducibility_with_seed` | Same seed → same sequence | Property |
| 101 | `EvenProcess::test_true_machine_returns_epsilon_machine` | true_machine returns valid EpsilonMachine | Fact |
| 102 | `EvenProcess::test_invalid_p_zero` | p=0 raises ValueError | Fact |
| 103 | `EvenProcess::test_invalid_p_one` | p=1 raises ValueError | Fact |
| 104 | `EvenProcess::test_with_seed_returns_new_source` | with_seed returns new source | Fact |
| 105 | `BiasedCoin::test_generates_binary_symbols` | Output contains only 0 and 1 | Fact |
| 106 | `BiasedCoin::test_fair_coin_approximately_balanced` | Fair coin produces roughly equal 0s and 1s | Property |
| 107 | `BiasedCoin::test_heavily_biased_coin` | Heavily biased coin produces mostly one symbol | Property |
| 108 | `BiasedCoin::test_p_zero_all_zeros` | p=0 produces all zeros | Fact |
| 109 | `BiasedCoin::test_p_one_all_ones` | p=1 produces all ones | Fact |
| 110 | `BiasedCoin::test_invalid_probability_raises_error` | Invalid probability raises ValueError | Fact |
| 111 | `BiasedCoin::test_true_machine_returns_epsilon_machine` | true_machine returns valid EpsilonMachine | Fact |
| 112 | `BiasedCoin::test_true_machine_has_correct_probabilities` | Machine encodes correct emission probabilities | Theory |
| 113 | `Periodic::test_generates_periodic_sequence` | Output repeats the pattern periodically | Fact |
| 114 | `Periodic::test_single_symbol_pattern` | Single symbol pattern → constant output | Fact |
| 115 | `Periodic::test_empty_pattern_raises_error` | Empty pattern raises ValueError | Fact |
| 116 | `Periodic::test_binary_pattern` | Binary patterns work correctly | Fact |
| 117 | `Periodic::test_true_machine_returns_epsilon_machine` | true_machine returns valid EpsilonMachine | Fact |
| 118 | `Periodic::test_true_machine_deterministic` | Periodic machine is fully deterministic (hμ = 0) | Theory |
| 119 | `Periodic::test_pipeline_operator_with_callable` | >> operator works with callable transforms | Fact |
| 120 | `Periodic::test_pipeline_operator_with_non_callable` | >> with non-callable returns NotImplemented | Fact |

## Sources — Empirical (`tests/unit/test_sources_empirical.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 121 | `test_from_string_splits_characters` | from_string splits string into characters | Fact |
| 122 | `test_from_binary_string_zeros_and_ones` | from_binary_string converts to integers | Fact |
| 123 | `test_from_binary_string_invalid_chars` | from_binary_string rejects invalid characters | Fact |
| 124 | `test_from_tuple` | Direct construction from sequence | Fact |
| 125 | `test_length` | Length returns correct count | Fact |
| 126 | `test_iteration` | Can iterate multiple times | Fact |
| 127 | `test_symbols_property` | Symbols tuple is accessible | Fact |
| 128 | `test_empty_sequence` | Empty sequence is valid | Fact |
| 129 | `test_alphabet_inferred` | Alphabet is inferred from symbols | Fact |
| 130 | `test_alphabet_explicit` | Explicit alphabet overrides inference | Fact |
| 131 | `test_frozen` | SequenceData is immutable | Fact |
| 132 | `test_pipeline_with_take` | SequenceData works with TakeN | Fact |
| 133 | `test_pipeline_with_skip` | SequenceData works with SkipN | Fact |
| 134 | `test_pipeline_chaining` | Multiple transforms chain correctly | Fact |

## Sources — Transforms (`tests/unit/test_sources_transforms.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 135 | `TakeN::test_takes_first_n_elements` | TakeN returns first n elements | Fact |
| 136 | `TakeN::test_takes_all_if_n_exceeds_length` | TakeN returns all if n > length | Fact |
| 137 | `TakeN::test_take_zero` | TakeN(0) returns empty | Fact |
| 138 | `TakeN::test_take_from_empty` | TakeN from empty source returns empty | Fact |
| 139 | `TakeN::test_repr` | TakeN has informative repr | Fact |
| 140 | `TakeN::test_callable_protocol` | TakeN can be called as function | Fact |
| 141 | `SkipN::test_skips_first_n_elements` | SkipN skips first n elements | Fact |
| 142 | `SkipN::test_skip_all_returns_empty` | Skipping all elements returns empty | Fact |
| 143 | `SkipN::test_skip_more_than_length` | Skipping more than length returns empty | Fact |
| 144 | `SkipN::test_skip_zero` | SkipN(0) returns all elements | Fact |
| 145 | `SkipN::test_skip_from_empty` | SkipN from empty source returns empty | Fact |
| 146 | `SkipN::test_repr` | SkipN has informative repr | Fact |
| 147 | `Chaining::test_skip_then_take` | Skip followed by take works correctly | Fact |
| 148 | `Chaining::test_take_then_skip` | Take followed by skip works correctly | Fact |
| 149 | `Chaining::test_multiple_takes` | Multiple takes take minimum | Fact |
| 150 | `Chaining::test_multiple_skips` | Multiple skips accumulate | Fact |
| 151 | `Chaining::test_complex_chain` | Complex chain of transforms | Fact |
| 152 | `BitFlipNoise::test_zero_noise_preserves_data` | BitFlipNoise(0) does not change data | Fact |
| 153 | `BitFlipNoise::test_noise_flips_some_symbols` | Non-zero flip probability changes some symbols | Property |
| 154 | `BitFlipNoise::test_deterministic_with_seed` | Same seed → same noise pattern | Property |
| 155 | `BitFlipNoise::test_different_seeds_differ` | Different seeds → different noise | Property |
| 156 | `BitFlipNoise::test_flip_prob_validation` | flip_prob must be in [0, 0.5] | Fact |
| 157 | `BitFlipNoise::test_alphabet_preserved` | Noisy source has same alphabet as original | Fact |
| 158 | `BitFlipNoise::test_pipeline_composition` | BitFlipNoise works in pipelines | Fact |
| 159 | `BitFlipNoise::test_repr` | BitFlipNoise has informative repr | Fact |

## Inference — CSSR (`tests/unit/test_inference_cssr.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 160 | `Config::test_valid_config` | Valid configuration is accepted | Fact |
| 161 | `Config::test_invalid_max_history` | max_history < 1 raises error | Fact |
| 162 | `Config::test_invalid_significance` | significance outside (0, 1) raises error | Fact |
| 163 | `Config::test_invalid_min_count` | min_count < 1 raises error | Fact |
| 164 | `Config::test_invalid_test` | Unknown test type raises error | Fact |
| 165 | `Inference::test_insufficient_data_raises_error` | Too few symbols raises InsufficientDataError | Fact |
| 166 | `Inference::test_infer_biased_coin_single_state` | CSSR finds 1 state for IID process | Theory |
| 167 | `Inference::test_infer_periodic_correct_states` | CSSR finds correct number of states for periodic | Theory |
| 168 | `Inference::test_infer_golden_mean_approximately_two_states` | CSSR finds ~2 states for Golden Mean | Theory |
| 169 | `Inference::test_result_has_diagnostics` | InferenceResult contains diagnostics | Fact |
| 170 | `Inference::test_pipeline_operator` | >> operator works with CSSR | Fact |
| 171 | `MachineProps::test_inferred_machine_is_valid` | Inferred machine passes all validation | Property |
| 172 | `MachineProps::test_inferred_machine_has_correct_alphabet` | Inferred machine has correct alphabet | Fact |
| 173 | `StatTests::test_cssr_with_gtest` | CSSR works with G-test variant | Fact |
| 174 | `StatTests::test_cssr_with_proportion_test` | CSSR works with proportion test variant | Fact |
| 175 | `StatTests::test_cssr_with_ks_test` | CSSR works with KS test variant | Fact |
| 176 | `EdgeCases::test_cssr_with_merge_significance` | CSSR respects merge_significance parameter | Fact |
| 177 | `EdgeCases::test_cssr_with_explicit_alphabet` | CSSR respects explicit alphabet | Fact |
| 178 | `EdgeCases::test_cssr_single_symbol_sequence` | CSSR handles constant sequences | Fact |
| 179 | `EdgeCases::test_cssr_alternating_sequence` | CSSR handles perfectly alternating sequences | Fact |
| 180 | `EdgeCases::test_cssr_very_short_max_history` | CSSR works with max_history=1 | Fact |
| 181 | `EdgeCases::test_cssr_strict_significance` | CSSR with very strict significance level | Property |
| 182 | `EdgeCases::test_cssr_lenient_significance` | CSSR with lenient significance level | Property |
| 183 | `EdgeCases::test_cssr_high_min_count` | CSSR with high min_count threshold | Fact |
| 184 | `EdgeCases::test_cssr_three_symbol_alphabet` | CSSR handles three-symbol alphabet | Fact |

## Inference — CSM (`tests/unit/test_inference_csm.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 185 | `Config::test_valid_config` | Valid configuration is accepted | Fact |
| 186 | `Config::test_default_values` | Default configuration values are correct | Fact |
| 187 | `Config::test_invalid_history_length` | history_length < 1 raises error | Fact |
| 188 | `Config::test_invalid_merge_threshold` | merge_threshold ≤ 0 raises error | Fact |
| 189 | `Config::test_invalid_min_count` | min_count < 1 raises error | Fact |
| 190 | `Config::test_invalid_distance_metric` | Unknown distance_metric raises error | Fact |
| 191 | `Config::test_all_valid_metrics` | All valid distance metrics accepted | Fact |
| 192 | `Inference::test_insufficient_data_raises_error` | Too few symbols raises InsufficientDataError | Fact |
| 193 | `Inference::test_infer_biased_coin_single_state` | CSM finds 1 state for IID process | Theory |
| 194 | `Inference::test_infer_periodic_correct_states` | CSM finds correct states for periodic | Theory |
| 195 | `Inference::test_infer_golden_mean_approximately_two_states` | CSM finds ~2 states for Golden Mean | Theory |
| 196 | `Inference::test_result_has_diagnostics` | InferenceResult contains diagnostics | Fact |
| 197 | `Inference::test_pipeline_operator` | >> operator works with CSM | Fact |
| 198 | `Metrics::test_hellinger_metric` | Hellinger distance produces valid results | Fact |
| 199 | `Metrics::test_tv_metric` | Total variation distance produces valid results | Fact |
| 200 | `Metrics::test_chi2_metric` | Chi-squared distance produces valid results | Fact |
| 201 | `vsCSSR::test_both_find_single_state_for_iid` | CSM and CSSR agree on 1 state for IID | Property |
| 202 | `vsCSSR::test_both_find_similar_states_for_golden_mean` | CSM and CSSR agree on ~2 states for Golden Mean | Property |

## Inference — BSI (`tests/unit/test_inference_bsi.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 203 | `Config::test_valid_config` | Valid configuration is accepted | Fact |
| 204 | `Config::test_default_values` | Default configuration values are correct | Fact |
| 205 | `Config::test_invalid_max_states` | max_states must be positive | Fact |
| 206 | `Config::test_invalid_max_history` | max_history must be positive | Fact |
| 207 | `Config::test_invalid_alpha_prior` | alpha_prior must be positive | Fact |
| 208 | `Config::test_invalid_n_samples` | n_samples must be positive | Fact |
| 209 | `Config::test_invalid_burnin` | burnin must be non-negative | Fact |
| 210 | `Config::test_invalid_thin` | thin must be positive | Fact |
| 211 | `Config::test_with_seed` | Configuration accepts seed | Fact |
| 212 | `Inference::test_insufficient_data_raises_error` | Short sequences raise InsufficientDataError | Fact |
| 213 | `Inference::test_infer_biased_coin_single_state` | BSI finds ~1 state for IID process | Theory |
| 214 | `Inference::test_infer_periodic_finds_states` | BSI finds states for periodic process | Theory |
| 215 | `Inference::test_infer_golden_mean` | BSI finds states for Golden Mean | Theory |
| 216 | `Inference::test_result_has_diagnostics` | Result contains diagnostic information | Fact |
| 217 | `Inference::test_pipeline_operator` | >> operator works with BSI | Fact |
| 218 | `Inference::test_with_explicit_alphabet` | BSI respects explicit alphabet | Fact |
| 219 | `Inference::test_reproducibility_with_seed` | Same seed → same result | Property |
| 220 | `MCMC::test_different_seeds_give_different_results` | Different seeds can give different results | Property |
| 221 | `MCMC::test_more_samples_doesnt_crash` | More MCMC samples runs without error | Fact |
| 222 | `MCMC::test_thinning` | Thinning parameter works | Fact |
| 223 | `EdgeCases::test_single_symbol_sequence` | Handles single-symbol data | Fact |
| 224 | `EdgeCases::test_high_alpha_prior` | High Dirichlet concentration works | Fact |
| 225 | `EdgeCases::test_low_alpha_prior` | Low Dirichlet concentration works | Fact |

## Inference — NSD (`tests/unit/test_inference_nsd.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 226 | `Config::test_valid_config` | Valid configuration is accepted | Fact |
| 227 | `Config::test_default_values` | Default configuration values are correct | Fact |
| 228 | `Config::test_invalid_max_states` | max_states must be positive | Fact |
| 229 | `Config::test_invalid_history_length` | history_length must be positive | Fact |
| 230 | `Config::test_invalid_embedding_dim` | embedding_dim must be positive | Fact |
| 231 | `Config::test_invalid_n_iterations` | n_iterations must be positive | Fact |
| 232 | `Config::test_invalid_convergence_threshold` | convergence_threshold must be positive | Fact |
| 233 | `Config::test_with_seed` | Configuration accepts seed | Fact |
| 234 | `Inference::test_insufficient_data_raises_error` | Short sequences raise InsufficientDataError | Fact |
| 235 | `Inference::test_infer_biased_coin` | NSD infers biased coin | Theory |
| 236 | `Inference::test_infer_periodic_finds_states` | NSD finds states for periodic | Theory |
| 237 | `Inference::test_infer_golden_mean` | NSD finds states for Golden Mean | Theory |
| 238 | `Inference::test_result_has_diagnostics` | Result contains diagnostics | Fact |
| 239 | `Inference::test_pipeline_operator` | >> operator works with NSD | Fact |
| 240 | `Inference::test_with_explicit_alphabet` | NSD respects explicit alphabet | Fact |
| 241 | `Inference::test_reproducibility_with_seed` | Same seed → same result | Property |
| 242 | `Clustering::test_different_seeds_may_give_different_results` | Different seeds can give different clustering | Property |
| 243 | `Clustering::test_more_iterations` | More k-means iterations works | Fact |
| 244 | `Clustering::test_convergence_detection` | Algorithm can converge early | Fact |
| 245 | `EdgeCases::test_single_symbol_sequence` | Handles single-symbol data | Fact |
| 246 | `EdgeCases::test_short_history_length` | Short history length works | Fact |
| 247 | `EdgeCases::test_many_max_states` | High max_states limit works | Fact |
| 248 | `EdgeCases::test_trivial_fallback` | Trivial machine built when few histories found | Fact |
| 249 | `Embeddings::test_embeddings_capture_predictive_distribution` | Embeddings reflect predictive distributions | Property |
| 250 | `Embeddings::test_rare_histories_filtered` | Rare histories are filtered out | Fact |

## Inference — Spectral (`tests/unit/test_inference_spectral.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 251 | `Config::test_valid_config` | Valid configuration is accepted | Fact |
| 252 | `Config::test_default_values` | Default configuration values are correct | Fact |
| 253 | `Config::test_invalid_max_history` | max_history must be positive | Fact |
| 254 | `Config::test_invalid_rank_threshold` | rank_threshold must be in (0, 1) | Fact |
| 255 | `Config::test_invalid_rank` | rank must be positive if specified | Fact |
| 256 | `Config::test_invalid_regularization` | regularization must be non-negative | Fact |
| 257 | `Config::test_invalid_min_count` | min_count must be positive | Fact |
| 258 | `Config::test_fixed_rank` | Fixed rank can be specified | Fact |
| 259 | `Inference::test_insufficient_data_raises_error` | Short sequences raise InsufficientDataError | Fact |
| 260 | `Inference::test_infer_biased_coin_single_state` | Spectral finds ~1 state for IID | Theory |
| 261 | `Inference::test_infer_periodic_finds_states` | Spectral finds states for periodic | Theory |
| 262 | `Inference::test_infer_golden_mean` | Spectral finds states for Golden Mean | Theory |
| 263 | `Inference::test_result_has_diagnostics` | Result contains diagnostics | Fact |
| 264 | `Inference::test_pipeline_operator` | >> operator works with Spectral | Fact |
| 265 | `Inference::test_with_explicit_alphabet` | Spectral respects explicit alphabet | Fact |
| 266 | `Hankel::test_hankel_counts_basic` | Hankel matrix is built correctly | Fact |
| 267 | `Hankel::test_hankel_with_single_symbol` | Hankel matrix handles single-symbol data | Fact |
| 268 | `EdgeCases::test_minimum_valid_sequence` | Minimum valid sequence length works | Fact |
| 269 | `EdgeCases::test_with_regularization` | Regularization parameter is respected | Fact |
| 270 | `EdgeCases::test_with_fixed_rank` | Fixed rank works | Fact |
| 271 | `EdgeCases::test_with_high_rank` | Higher fixed rank works | Fact |
| 272 | `EdgeCases::test_with_very_low_rank_threshold` | Very low rank threshold works | Fact |
| 273 | `EdgeCases::test_with_high_rank_threshold` | High (conservative) rank threshold works | Fact |
| 274 | `EdgeCases::test_three_symbol_alphabet` | Three-symbol alphabet works | Fact |
| 275 | `EdgeCases::test_long_period_pattern` | Longer periodic pattern works | Fact |
| 276 | `EdgeCases::test_short_history_length` | Short max_history works | Fact |
| 277 | `Extraction::test_trivial_machine_fallback` | Trivial machine built for edge cases | Fact |
| 278 | `Extraction::test_small_sequence_handling` | Small but valid sequences handled | Fact |
| 279 | `Extraction::test_operators_convergence` | Operators converge to valid machine | Property |
| 280 | `Operators::test_rank_selection_with_high_rank` | Rank selection for complex process | Property |
| 281 | `Operators::test_automatic_rank_selection` | Automatic rank selection on simple process | Property |
| 282 | `Operators::test_with_various_regularizations` | Different regularization values work | Property |
| 283 | `StateMerging::test_state_merging_occurs` | Similar states get merged | Property |
| 284 | `StateMerging::test_large_data_with_merging` | Merging works on larger dataset | Property |
| 285 | `ExtractionInternals::test_build_trivial_machine` | build_trivial_machine works | Fact |
| 286 | `ExtractionInternals::test_build_trivial_machine_empty_symbols` | Empty symbol list handled | Fact |
| 287 | `ExtractionInternals::test_merge_similar_states` | merge_similar_states merges correctly | Fact |
| 288 | `ExtractionInternals::test_merge_similar_states_distinct` | Distinct states are not merged | Fact |

## Inference — Internals (`tests/unit/test_inference_internals.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 289 | `HistoryStats::test_add_observation` | add_observation updates counts | Fact |
| 290 | `HistoryStats::test_next_symbol_distribution` | Correct predictive distribution from counts | Fact |
| 291 | `HistoryStats::test_empty_distribution` | Empty stats has count 0 | Fact |
| 292 | `HistoryStats::test_next_symbol_distribution_empty` | Empty stats returns None | Fact |
| 293 | `SuffixTree::test_build_from_sequence` | Suffix tree collects statistics | Fact |
| 294 | `SuffixTree::test_histories_of_length` | Returns histories of specified length | Fact |
| 295 | `SuffixTree::test_all_histories` | Iterates over all histories | Fact |
| 296 | `SuffixTree::test_add_observation_truncates` | Long histories truncated | Fact |
| 297 | `SuffixTree::test_get_stats_nonexistent` | None for unobserved history | Fact |
| 298 | `SuffixTree::test_build_records_empty_history` | Empty history is recorded | Fact |
| 299 | `SuffixTree::test_build_respects_max_depth` | Max depth honoured | Fact |
| 300 | `Partition::test_assign_and_get` | assign() and get_state() work | Fact |
| 301 | `Partition::test_get_histories` | Returns all histories in a state | Fact |
| 302 | `Partition::test_num_states` | Correct state count | Fact |
| 303 | `Partition::test_copy` | copy() creates independent copy | Fact |
| 304 | `Partition::test_merge_states` | merge_states combines states | Fact |
| 305 | `Partition::test_merge_states_empty_list` | Merge with empty list returns new state | Fact |
| 306 | `Partition::test_split_state_nonexistent` | Split nonexistent state returns empty list | Fact |
| 307 | `Partition::test_split_state_with_remaining` | Split keeps remaining histories | Fact |
| 308 | `Partition::test_equality_with_non_partition` | Comparing to non-partition returns NotImplemented | Fact |
| 309 | `Partition::test_equality_same_content` | Same content partitions are equal | Fact |
| 310 | `Partition::test_equality_different_content` | Different content partitions differ | Fact |
| 311 | `Partition::test_reassign_removes_from_old` | Reassigning history removes it from old state | Fact |
| 312 | `Partition::test_reassign_last_removes_state` | Removing last history deletes the state | Fact |
| 313 | `Partition::test_get_histories_nonexistent` | Nonexistent state returns empty set | Fact |
| 314 | `Partition::test_state_ids_empty` | Empty partition has no state IDs | Fact |
| 315 | `Partition::test_new_state_id_increments` | State IDs increment | Fact |
| 316 | `Partition::test_copy_preserves_counter` | Copy preserves next state ID counter | Fact |
| 317 | `StatTests::test_chi_squared_same` | Same distribution → not significantly different | Theory |
| 318 | `StatTests::test_chi_squared_different` | Very different distributions → significantly different | Theory |
| 319 | `StatTests::test_chi_squared_insufficient` | Insufficient counts → not significant | Theory |
| 320 | `StatTests::test_g_test` | G-test variant works | Fact |
| 321 | `StatTests::test_ks_test` | KS test variant works | Fact |
| 322 | `StatTests::test_proportion_test` | Proportion test variant works | Fact |
| 323 | `StatTests::test_unknown_defaults_chi2` | Unknown test type defaults to chi-squared | Fact |
| 324 | `StatTests::test_different_significance_levels` | Different significance levels handled | Property |
| 325 | `StatTests::test_high_dof` | High degrees of freedom handled | Fact |
| 326 | `StatTests::test_zero_expected` | Zero expected values handled gracefully | Fact |
| 327 | `Errors::test_insufficient_data_explain` | InsufficientDataError has explain() | Fact |
| 328 | `Errors::test_non_convergence_explain` | NonConvergenceError has explain() | Fact |

## Output (`tests/unit/test_output.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 329 | `DiagramStyle::test_default_values` | Default style values work | Fact |
| 330 | `DiagramStyle::test_custom_values` | Custom style values accepted | Fact |
| 331 | `DiagramStyle::test_frozen` | DiagramStyle is immutable | Fact |
| 332 | `Render::test_render_golden_mean` | Renders Golden Mean machine | Fact |
| 333 | `Render::test_render_with_custom_style` | Renders with custom style | Fact |
| 334 | `Render::test_render_with_size` | Renders with size option | Fact |
| 335 | `TikZ::test_tikz_structure` | TikZ output has correct LaTeX structure | Fact |
| 336 | `TikZ::test_tikz_with_custom_labels` | TikZ output uses custom labels | Fact |
| 337 | `LaTeX::test_table_structure` | LaTeX table has correct structure | Fact |
| 338 | `LaTeX::test_custom_measures` | Table with custom measure selection | Fact |
| 339 | `JSON::test_round_trip` | JSON serialization round-trips correctly | Fact |
| 340 | `JSON::test_json_valid` | Output is valid JSON | Fact |
| 341 | `JSON::test_json_contains_transitions` | JSON contains all transitions | Fact |
| 342 | `DOT::test_dot_structure` | DOT output has correct structure | Fact |
| 343 | `DOT::test_dot_contains_states` | DOT contains all states | Fact |
| 344 | `Mermaid::test_mermaid_structure` | Mermaid output has correct structure | Fact |
| 345 | `Mermaid::test_mermaid_contains_transitions` | Mermaid contains transitions with labels | Fact |
| 346 | `Display::test_display_exists` | display_state_diagram function exists | Fact |
| 347 | `Display::test_display_with_mock_ipython` | display works with mocked IPython | Fact |
| 348 | `Display::test_render_returns_graphviz_digraph` | render returns graphviz.Digraph object | Fact |

## Package (`tests/unit/test_package.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 349 | `test_version_exists` | Package has a __version__ string | Fact |
| 350 | `test_version_format` | Version follows semver pattern | Fact |

## Experiments (`tests/unit/test_experiments.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 351 | `AlgorithmRegistry::test_default_registry` | Default registry has all algorithms | Fact |
| 352 | `AlgorithmRegistry::test_get_algorithm` | Get algorithm by name | Fact |
| 353 | `AlgorithmRegistry::test_bsi_is_slow` | BSI is marked as slow | Fact |
| 354 | `AlgorithmRegistry::test_list_excluding_slow` | Can list non-slow algorithms | Fact |
| 355 | `ProcessRegistry::test_default_registry` | Default registry has all processes | Fact |
| 356 | `ProcessRegistry::test_get_process` | Get process by name | Fact |
| 357 | `ProcessRegistry::test_create_source` | Create source from process | Fact |
| 358 | `ProcessRegistry::test_unknown_process` | Unknown process raises error | Fact |
| 359 | `BenchmarkResult::test_create_result` | BenchmarkResult can be created | Fact |
| 360 | `BenchmarkResult::test_result_with_error` | Result can record error | Fact |
| 361 | `BenchmarkResult::test_to_dict` | to_dict returns dict | Fact |
| 362 | `ExperimentConfig::test_default_config` | Default config values are correct | Fact |
| 363 | `ExperimentConfig::test_total_runs` | total_runs computation is correct | Fact |
| 364 | `ResultsWriter::test_write_results` | Results writer writes JSON | Fact |
| 365 | `CLI::test_list_experiments` | --list flag works | Fact |
| 366 | `CLI::test_parser_help` | --help works | Fact |
| 367 | `RunBenchmark::test_run_benchmark` | Single benchmark runs successfully | Fact |
| 368 | `Sharding::test_parse_shard_valid` | Valid shard spec parsed | Fact |
| 369 | `Sharding::test_parse_shard_invalid` | Invalid shard spec raises error | Fact |
| 370 | `Sharding::test_combine_shard_results` | Shard results combine | Fact |
| 371 | `Sharding::test_results_writer_with_shard` | Results writer handles shards | Fact |

## Golden Tests (`tests/golden/test_inference_golden.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 372 | `BiasedCoin::test_cssr_finds_one_state` | CSSR finds 1 state for IID process | Theory |
| 373 | `BiasedCoin::test_csm_finds_one_state` | CSM finds 1 state for IID process | Theory |
| 374 | `BiasedCoin::test_bsi_finds_one_state` | BSI finds 1 state for IID process | Theory |
| 375 | `BiasedCoin::test_nsd_finds_one_state` | NSD finds 1 state for IID process | Theory |
| 376 | `BiasedCoin::test_spectral_finds_one_state` | Spectral finds 1 state for IID process | Theory |
| 377 | `GoldenMean::test_cssr_finds_two_states` | CSSR finds 2 states for Golden Mean | Theory |
| 378 | `GoldenMean::test_csm_finds_two_states` | CSM finds 2 states for Golden Mean | Theory |
| 379 | `GoldenMean::test_bsi_finds_two_states` | BSI finds ~2 states for Golden Mean | Theory |
| 380 | `GoldenMean::test_nsd_finds_two_states` | NSD finds ~2 states for Golden Mean | Theory |
| 381 | `GoldenMean::test_spectral_finds_two_states` | Spectral finds ~2 states for Golden Mean | Theory |
| 382 | `GoldenMean::test_machine_forbids_consecutive_ones` | Inferred machine forbids 1→1 transitions | Theory |
| 383 | `Periodic::test_period_2_cssr` | CSSR finds 2 states for period-2 | Theory |
| 384 | `Periodic::test_period_2_csm` | CSM finds 2 states for period-2 | Theory |
| 385 | `Periodic::test_period_2_bsi` | BSI finds 2 states for period-2 | Theory |
| 386 | `Periodic::test_period_2_nsd` | NSD finds 2 states for period-2 | Theory |
| 387 | `Periodic::test_period_2_spectral` | Spectral finds 2 states for period-2 | Theory |
| 388 | `Periodic::test_period_3_cssr` | CSSR finds 3 states for period-3 | Theory |
| 389 | `Periodic::test_period_3_csm` | CSM finds 3 states for period-3 | Theory |
| 390 | `Periodic::test_period_3_bsi` | BSI finds 3 states for period-3 | Theory |
| 391 | `Periodic::test_period_3_nsd` | NSD finds 3 states for period-3 | Theory |
| 392 | `Periodic::test_period_3_spectral` | Spectral finds 3 states for period-3 | Theory |
| 393 | `EvenProcess::test_cssr_finds_two_states` | CSSR finds ~2 states for Even Process | Theory |
| 394 | `EvenProcess::test_csm_finds_two_states` | CSM finds ~2 states for Even Process | Theory |
| 395 | `EvenProcess::test_bsi_finds_two_states` | BSI finds ~2 states for Even Process | Theory |
| 396 | `EvenProcess::test_nsd_finds_two_states` | NSD finds ~2 states for Even Process | Theory |
| 397 | `EvenProcess::test_spectral_finds_two_states` | Spectral finds ~2 states for Even Process | Theory |
| 398 | `EvenProcess::test_machine_enforces_even_ones` | Inferred machine shows 1s come in pairs | Theory |
| 399 | `Consistency::test_algorithms_agree_on_state_count` | Core algorithms agree on state count for known processes (×4 processes) | Property |
| 400 | `Invariants::test_stochastic_transitions_golden_mean` | All algorithms produce stochastic machines on Golden Mean (×5 algos) | Property |
| 401 | `Invariants::test_stochastic_transitions_even_process` | All algorithms produce stochastic machines on Even Process (×5 algos) | Property |
| 402 | `Measures::test_cssr_golden_mean_measures` | CSSR on Golden Mean: Cμ≈0.918, hμ≈0.667, E≈0.252, χ≈0.667 | Theory |
| 403 | `Measures::test_spectral_golden_mean_measures` | Spectral on Golden Mean: same analytical targets | Theory |
| 404 | `Measures::test_cssr_biased_coin_measures` | CSSR on Biased Coin: Cμ=0, E=0, χ=0 | Theory |
| 405 | `Measures::test_excess_entropy_bounded_by_complexity` | E ≤ Cμ holds for all algorithms on Golden Mean | Theory |

## Integration (`tests/integration/test_pipeline.py`)

| # | Test | Intent | Kind |
|---|------|--------|------|
| 406 | `Pipeline::test_source_to_transform` | Source >> Transform works | Fact |
| 407 | `Pipeline::test_source_to_transform_to_inference` | Source >> Transform >> Inference works | Fact |
| 408 | `Pipeline::test_full_pipeline` | Source >> Transform >> Inference >> Analysis works | Fact |
| 409 | `Pipeline::test_different_sources` | Pipeline works with different sources | Fact |
| 410 | `Tap::test_tap_returns_input` | tap() returns input unchanged | Fact |
| 411 | `Tap::test_tap_in_pipeline` | tap works in a pipeline | Fact |
| 412 | `Identity::test_identity_returns_input` | identity returns input unchanged | Fact |
| 413 | `Builder::test_empty_pipeline` | Empty pipeline returns initial value | Fact |
| 414 | `Builder::test_single_stage` | Pipeline with single stage | Fact |
| 415 | `Builder::test_multiple_stages` | Pipeline with multiple stages | Fact |

---

## Summary

| Category | Fact | Theory | Property | Total |
|----------|------|--------|----------|-------|
| Types (states, probability, alphabet, machine) | 47 | 4 | 0 | 51 |
| Analysis | 5 | 15 | 0 | 20 |
| Sources (protocol, base, synthetic, empirical, transforms) | 52 | 7 | 10 | 69 |
| Inference — CSSR | 20 | 3 | 2 | 25 |
| Inference — CSM | 13 | 2 | 2 | 17 |
| Inference — BSI | 17 | 3 | 2 | 22 |
| Inference — NSD | 17 | 3 | 3 | 23 |
| Inference — Spectral | 23 | 3 | 6 | 32 |
| Inference — Internals | 34 | 3 | 1 | 38 |
| Output | 19 | 0 | 0 | 19 |
| Package | 2 | 0 | 0 | 2 |
| Experiments | 21 | 0 | 0 | 21 |
| Golden tests | 0 | 30 | 4 | 34 |
| Integration | 10 | 0 | 0 | 10 |
| **Total** | **280** | **73** | **30** | **383** |

> **Note**: 383 unique test definitions expand to 429 test items due to
> parametrized tests (e.g. `test_algorithms_agree_on_state_count` ×4 processes,
> `test_stochastic_transitions_*` ×5 algorithms each).
