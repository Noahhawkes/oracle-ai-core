import { detectConflicts } from '../continuity-analyzer/detectConflicts.js';
import { detectGaps } from '../continuity-analyzer/detectGaps.js';
import { evaluateProtocolState } from '../state-machine/evaluateProtocolState.js';

export function generateContinuityView(input: any) {
  const records = input.records ?? [];
  const gaps = detectGaps(records);
  const conflicts = detectConflicts(records);

  const hasPrimaryArtifacts = records.some((record: any) => record.validation_status === 'VALID_PRIMARY');
  const hasIdentityMismatch = records.some((record: any) => record.subject_id !== input.subject_id);

  const protocol_state = evaluateProtocolState({
    hasPrimaryArtifacts,
    hasIdentityMismatch,
    hasConflicts: conflicts.length > 0,
    hasGaps: gaps.length > 0
  });

  return {
    subject_id: input.subject_id,
    requested_scope: input.requested_scope,
    protocol_state,
    artifacts: records,
    gaps,
    conflicts,
    constraints: {
      allow_inference: protocol_state === 'OK_CONTINUITY_VIEW',
      forbid_speculation: true,
      require_citations: true
    }
  };
}
