fixed_positions = [334, 340, 342, 475, 477, 513]

sequences = []
current_header = ""
current_seq = ""

with open("results/proteinmpnn_run2_fixed/seqs/structures/brca2_cleaned.fa") as f:
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            if current_seq:
                sequences.append((current_header, current_seq))
            current_header = line
            current_seq = ""
        else:
            current_seq += line
    if current_seq:
        sequences.append((current_header, current_seq))

native_seq = sequences[0][1]
print("NATIVE amino acids at fixed positions:")
for pos in fixed_positions:
    print(f"  Position {pos}: {native_seq[pos-1]}")

print("\nDESIGNED sequences at fixed positions:")
for header, seq in sequences[1:]:
    sample = header.split("sample=")[1].split(",")[0] if "sample=" in header else "?"
    score = header.split("score=")[1].split(",")[0] if "score=" in header else "?"
    print(f"\n  Sample {sample} (score={score}):")
    all_fixed = True
    for pos in fixed_positions:
        native_aa = native_seq[pos-1]
        designed_aa = seq[pos-1]
        match = "✓" if native_aa == designed_aa else "✗ CHANGED"
        print(f"    Position {pos}: {designed_aa} (native: {native_aa}) {match}")
        if native_aa != designed_aa:
            all_fixed = False
    print(f"  All fixed correctly: {all_fixed}")