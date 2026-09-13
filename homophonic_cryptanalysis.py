from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

HOMOPHONE_RE = re.compile(r"^[a-z][0-9]$")
CIPHERTEXT_PATH = Path(__file__).with_name("ciphertext.txt")
UNIGRAM_PLOT_PATH = Path(__file__).with_name("Task1_FreqCount.png")
BIGRAM_PLOT_PATH = Path(__file__).with_name("Task2_Top15.png")
TRIGRAM_PLOT_PATH = Path(__file__).with_name("Task3_Top10.png")


def read_tokens(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [token.strip() for token in text.split("|")]


def is_homophone(token: str) -> bool:
    return bool(HOMOPHONE_RE.fullmatch(token))


def count_homophones(tokens: list[str]) -> Counter[str]:
    return Counter(token for token in tokens if is_homophone(token))


def count_bigrams(tokens: list[str]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for left, right in zip(tokens, tokens[1:]):
        if is_homophone(left) and is_homophone(right):
            counts[f"{left}-{right}"] += 1
    return counts


def count_trigrams(tokens: list[str]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for a, b, c in zip(tokens, tokens[1:], tokens[2:]):
        if is_homophone(a) and is_homophone(b) and is_homophone(c):
            counts[f"{a}-{b}-{c}"] += 1
    return counts


def _save_bar_chart(
    labels: list[str],
    frequencies: list[int],
    title: str,
    xlabel: str,
    output_path: Path,
    figsize: tuple[float, float],
    rotation: int = 45,
) -> None:
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(range(len(labels)), frequencies, color="steelblue", edgecolor="none")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=rotation, ha="right" if rotation else "center", fontsize=8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Frequency")
    ax.set_title(title)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    if plt.get_backend().lower() != "agg":
        plt.show()
    plt.close(fig)


def plot_homophone_frequencies(counts: Counter[str], output_path: Path) -> None:
    items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    labels = [homophone for homophone, _ in items]
    frequencies = [freq for _, freq in items]
    _save_bar_chart(
        labels,
        frequencies,
        title="Homophone Frequency Counts",
        xlabel="Homophone",
        output_path=output_path,
        figsize=(max(12, len(labels) * 0.18), 6),
        rotation=90,
    )


def plot_top_bigrams(counts: Counter[str], output_path: Path, top_n: int = 15) -> None:
    top = counts.most_common(top_n)
    labels = [bigram for bigram, _ in top]
    frequencies = [freq for _, freq in top]
    _save_bar_chart(
        labels,
        frequencies,
        title=f"Top {top_n} Homophone Bigrams",
        xlabel="Bigram",
        output_path=output_path,
        figsize=(10, 6),
        rotation=45,
    )


def plot_top_trigrams(counts: Counter[str], output_path: Path, top_n: int = 10) -> None:
    top = counts.most_common(top_n)
    labels = [trigram for trigram, _ in top]
    frequencies = [freq for _, freq in top]
    _save_bar_chart(
        labels,
        frequencies,
        title=f"Top {top_n} Homophone Trigrams",
        xlabel="Trigram",
        output_path=output_path,
        figsize=(10, 6),
        rotation=45,
    )


def main() -> None:
    tokens = read_tokens(CIPHERTEXT_PATH)

    # --- Task 1 ---
    unigram_counts = count_homophones(tokens)
    print(f"Unique homophones: {len(unigram_counts)}")
    print(f"Total homophone occurrences: {sum(unigram_counts.values())}")
    print("\nTop 20 homophones:")
    for homophone, freq in unigram_counts.most_common(20):
        print(f"  {homophone}: {freq}")
    plot_homophone_frequencies(unigram_counts, UNIGRAM_PLOT_PATH)
    print(f"\nUnigram chart saved to: {UNIGRAM_PLOT_PATH}")

    # --- Task 2 ---
    bigram_counts = count_bigrams(tokens)
    print(f"\nUnique bigrams: {len(bigram_counts)}")
    print(f"Total valid bigram occurrences: {sum(bigram_counts.values())}")
    print("\nTop 15 bigrams:")
    for bigram, freq in bigram_counts.most_common(15):
        print(f"  {bigram}: {freq}")
    plot_top_bigrams(bigram_counts, BIGRAM_PLOT_PATH, top_n=15)
    print(f"\nBigram chart saved to: {BIGRAM_PLOT_PATH}")

    # --- Task 3 ---
    trigram_counts = count_trigrams(tokens)
    print(f"\nUnique trigrams: {len(trigram_counts)}")
    print(f"Total valid trigram occurrences: {sum(trigram_counts.values())}")
    print("\nTop 10 trigrams:")
    for trigram, freq in trigram_counts.most_common(10):
        print(f"  {trigram}: {freq}")
    plot_top_trigrams(trigram_counts, TRIGRAM_PLOT_PATH, top_n=10)
    print(f"\nTrigram chart saved to: {TRIGRAM_PLOT_PATH}")


if __name__ == "__main__":
    main()
