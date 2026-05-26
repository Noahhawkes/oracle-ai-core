export interface SynthesisPolicy {
  allowIdentityClaims: boolean;
  allowWeakInference: boolean;
  requireCitations: boolean;
  allowGapFilling: boolean;
}

export function derivePolicyFromProtocolState(view: any): SynthesisPolicy {
  switch (view.protocol_state) {
    case 'OK_CONTINUITY_VIEW':
    case 'PARTIAL_CONTINUITY':
      return {
        allowIdentityClaims: true,
        allowWeakInference: true,
        requireCitations: true,
        allowGapFilling: false
      };

    case 'NO_PRIMARY_ARTIFACTS':
    case 'IDENTITY_AMBIGUOUS':
    case 'CONTINUITY_BREAK':
    default:
      return {
        allowIdentityClaims: false,
        allowWeakInference: false,
        requireCitations: true,
        allowGapFilling: false
      };
  }
}
