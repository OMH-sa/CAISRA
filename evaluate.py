"""Evaluate the outage detector against the outage injected by network_sim.py.

Uses the committed network_data.csv and the same Isolation Forest settings as
threat_detector.py, so the numbers are reproducible.

Run:  python evaluate.py
"""
import pandas as pd
from sklearn.ensemble import IsolationForest

# network_sim.py injects the outage from second 600 up to (not including) second 800.
OUTAGE_START, OUTAGE_END = 600, 800
FEATURES = ["Ping(ms)", "Jitter(ms)", "Packet_Loss(%)"]


def score(pred, truth):
    tp = int(((pred == 1) & (truth == 1)).sum())
    fp = int(((pred == 1) & (truth == 0)).sum())
    fn = int(((pred == 0) & (truth == 1)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return tp, fp, fn, precision, recall


def main():
    df = pd.read_csv("network_data.csv")
    truth = ((df["Time(s)"] >= OUTAGE_START) & (df["Time(s)"] < OUTAGE_END)).astype(int)

    # Same settings as threat_detector.py: fit and predict on the same 1,000 seconds.
    model = IsolationForest(contamination=0.2, random_state=42)
    iforest = (model.fit_predict(df[FEATURES]) == -1).astype(int)

    # Baseline: flag every second that has any packet loss.
    rule = (df["Packet_Loss(%)"] > 0).astype(int)

    print(f"Seconds: {len(df)} | injected outage seconds: {int(truth.sum())}")
    print(f"{'Method':<24}{'Flagged':>8}{'TP':>6}{'FP':>6}{'FN':>6}{'Precision':>11}{'Recall':>8}")
    for name, pred in [("Isolation Forest", iforest), ("Rule: packet loss > 0", rule)]:
        tp, fp, fn, precision, recall = score(pred, truth)
        print(f"{name:<24}{int(pred.sum()):>8}{tp:>6}{fp:>6}{fn:>6}{precision:>11.2f}{recall:>8.2f}")


if __name__ == "__main__":
    main()
