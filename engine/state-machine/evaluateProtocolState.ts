export type ProtocolState =
  | 'OK_CONTINUITY_VIEW'
  | 'PARTIAL_CONTINUITY'
  | 'NO_PRIMARY_ARTIFACTS'
  | 'IDENTITY_AMBIGUOUS'
  | 'CONTINUITY_BREAK';

interface EvaluateInput {
  hasPrimaryArtifacts: boolean;
  hasIdentityMismatch: boolean;
  hasConflicts: boolean;
  hasGaps: boolean;
}

export function evaluateProtocolState(input: EvaluateInput): ProtocolState {
  if (!input.hasPrimaryArtifacts) {
    return 'NO_PRIMARY_ARTIFACTS';
  }

  if (input.hasIdentityMismatch) {
    return 'CONTINUITY_BREAK';
  }

  if (input.hasConflicts) {
    return 'CONTINUITY_BREAK';
  }

  if (input.hasGaps) {
    return 'PARTIAL_CONTINUITY';
  }

  return 'OK_CONTINUITY_VIEW';
}
