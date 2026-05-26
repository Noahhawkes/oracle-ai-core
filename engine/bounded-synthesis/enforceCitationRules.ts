export function enforceCitationRules(output: any, policy: any) {
  if (!policy.requireCitations) {
    return output;
  }

  return {
    segments: output.segments.filter((segment: any) => {
      return Array.isArray(segment.artifactIds) && segment.artifactIds.length > 0;
    })
  };
}
