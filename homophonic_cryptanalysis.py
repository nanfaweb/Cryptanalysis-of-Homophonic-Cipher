from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

HOMOPHONE_RE = re.compile(r"^[a-z][0-9]$")
CIPHERTEXT_PATH = Path(__file__).with_name("ciphertext.txt")
PLOT_PATH = Path(__file__).with_name("homophone_frequencies.png")


def read_tokens(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [token.strip() for token in text.split("|")]


def is_homophone(token: str) -> bool:
    return bool(HOMOPHONE_RE.fullmatch(token))


def count_homophones(tokens: list[str]) -> Counter[str]:
    return Counter(token for token in tokens if is_homophone(token))


def plot_homophone_frequencies(counts: Counter[str], output_path: Path) -> None:
    # Sort by frequency descending for a readable bar chart
    items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    labels = [homophone for homophone, _ in items]
    frequencies = [freq for _, freq in items]

    fig, ax = plt.subplots(figsize=(max(12, len(labels) * 0.18), 6))
    ax.bar(range(len(labels)), frequencies, color="steelblue", edgecolor="none")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=6)
    ax.set_xlabel("Homophone")
    ax.set_ylabel("Frequency")
    ax.set_title("Homophone Frequency Counts")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)

    if plt.get_backend().lower() != "agg":
        plt.show()
    plt.close(fig)


def main() -> None:
    tokens = read_tokens(CIPHERTEXT_PATH)
    counts = count_homophones(tokens)

    print(f"Unique homophones: {len(counts)}")
    print(f"Total homophone occurrences: {sum(counts.values())}")
    print("\nTop 20 homophones:")
    for homophone, freq in counts.most_common(20):
        print(f"  {homophone}: {freq}")

    plot_homophone_frequencies(counts, PLOT_PATH)
    print(f"\nChart saved to: {PLOT_PATH}")


if __name__ == "__main__":
    main()
