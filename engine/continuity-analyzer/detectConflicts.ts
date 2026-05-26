export interface ContinuityRecordLike {
  artifact_id: string;
  subject_id: string;
  timestamp?: string;
  continuity_scope?: string;
  claims?: Record<string, unknown>;
}

export interface Conflict {
  field: string;
  records: string[];
  description: string;
}

export function detectConflicts(records: ContinuityRecordLike[]): Conflict[] {
  const conflicts: Conflict[] = [];
  const claimIndex = new Map<string, Map<string, string[]>>();

  for (const record of records) {
    if (!record.claims) continue;

    for (const [field, value] of Object.entries(record.claims)) {
      const normalizedValue = JSON.stringify(value);

      if (!claimIndex.has(field)) {
        claimIndex.set(field, new Map());
      }

      const values = claimIndex.get(field)!;
      const artifactIds = values.get(normalizedValue) ?? [];
      artifactIds.push(record.artifact_id);
      values.set(normalizedValue, artifactIds);
    }
  }

  for (const [field, values] of claimIndex.entries()) {
    if (values.size <= 1) continue;

    conflicts.push({
      field,
      records: Array.from(values.values()).flat(),
      description: `Conflicting values detected for field: ${field}.`
    });
  }

  return conflicts;
}
