import { derivePolicyFromProtocolState } from './derivePolicyFromProtocolState.js';
import { enforceCitationRules } from './enforceCitationRules.js';
import { enforceInferenceRules } from './enforceInferenceRules.js';

export async function boundedSynthesis(view: any, task: string, llm: any) {
  const policy = derivePolicyFromProtocolState(view);

  if (!policy.allowIdentityClaims) {
    return {
      content:
        'The continuity protocol cannot safely generate identity-affecting output for this subject under the current state.',
      source_refs: [],
      surfaced_gaps: view.gaps,
      surfaced_conflicts: view.conflicts,
      protocol_state: view.protocol_state
    };
  }

  const llmInput = {
    system:
      'You are operating under a continuity governance protocol. Only produce claims grounded in provided artifacts.',
    context: {
      continuity_view: view,
      policy
    },
    task
  };

  const rawOutput = await llm(llmInput);

  let analyzed = rawOutput;

  analyzed = enforceCitationRules(analyzed, policy);
  analyzed = enforceInferenceRules(analyzed, policy);

  return {
    content: analyzed.segments.map((s: any) => s.text).join(' '),
    source_refs: analyzed.segments.flatMap((s: any) =>
      s.artifactIds.map((id: string) => ({
        artifact_id: id,
        inference_level: s.inferenceLevel
      }))
    ),
    surfaced_gaps: view.gaps,
    surfaced_conflicts: view.conflicts,
    protocol_state: view.protocol_state
  };
}
