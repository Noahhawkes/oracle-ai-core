export interface Gap {
  start: string;
  end: string;
  reason: 'NO_PRIMARY_ARTIFACTS' | 'OUT_OF_SCOPE' | 'FILTERED_BY_POLICY';
}

export interface TimestampedRecord {
  artifact_id: string;
  timestamp: string;
}

export function detectGaps(records: TimestampedRecord[]): Gap[] {
  if (records.length < 2) {
    return [];
  }

  const sorted = [...records].sort((a, b) => {
    return new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime();
  });

  const gaps: Gap[] = [];

  for (let i = 0; i < sorted.length - 1; i++) {
    const current = new Date(sorted[i].timestamp).getTime();
    const next = new Date(sorted[i + 1].timestamp).getTime();

    const deltaDays = (next - current) / (1000 * 60 * 60 * 24);

    if (deltaDays > 365) {
      gaps.push({
        start: sorted[i].timestamp,
        end: sorted[i + 1].timestamp,
        reason: 'NO_PRIMARY_ARTIFACTS'
      });
    }
  }

  return gaps;
}
