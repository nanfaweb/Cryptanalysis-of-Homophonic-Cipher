# Homophonic Cipher Cryptanalysis

Frequency analysis tooling for a pipe-separated homophonic ciphertext.

Homophones look like `p9` (lowercase letter + digit). Tokens are separated by `|`. Spaces, punctuation, and digits in the ciphertext are plaintext that was left unencrypted.

## Setup

```bash
pip install matplotlib
```

## Run

Place `ciphertext.txt` next to the script, then:

```bash
python homophonic_cryptanalysis.py
```

The script will:

1. Count all homophone frequencies and save a bar chart
2. Count valid bigrams (adjacent homophones only) and plot the top 15
3. Count valid trigrams and plot the top 10

A bigram/trigram is only counted when every token in the window is a homophone. A space or punctuation mark breaks the sequence.

Example: `y5|l8|v6| |e8|r6|` → bigrams `y5-l8`, `l8-v6`, `e8-r6` only.

## Outputs

| File | Description |
|------|-------------|
| `Task1_FreqCount.png` | Homophone frequency chart |
| `Task2_Top15.png` | Top 15 bigrams |
| `Task3_Top10.png` | Top 10 trigrams |
| `Key and Rationale.txt` | Partial key guess from n-gram analysis |

## Key guess (high confidence)

| Letter | Homophones |
|--------|------------|
| a | l8, v9 |
| e | p0, e1, p5, q7, y3, d8, c6 |
| h | b6, m6, j6, t1 |
| o | p1 |
| r | k4, j9 |
| s | s0, g2, q0, w6 |
| t | m3, s2, b3, i7 |

Derived mainly from common English patterns (`th`/`he` → `the`, `er`/`re`, `ate`) and short word checks (`the`, `she`, `she's`, `others`, `that's`). Other letters and remaining homophones are not fully resolved yet.

## Project layout

```
homophonic_cryptanalysis.py   # analysis + plots
ciphertext.txt                # input
Key and Rationale.txt         # key notes
Task1_FreqCount.png
Task2_Top15.png
Task3_Top10.png
```
