export function enforceInferenceRules(output: any, policy: any) {
  return {
    segments: output.segments.filter((segment: any) => {
      if (segment.inferenceLevel === 'SPECULATIVE') {
        return false;
      }

      if (
        segment.inferenceLevel === 'WEAK_INFERENCE' &&
        !policy.allowWeakInference
      ) {
        return false;
      }

      return true;
    })
  };
}
