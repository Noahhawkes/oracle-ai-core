import Ajv from 'ajv';
import schema from '../../schemas/continuity-record.schema.json' assert { type: 'json' };

const ajv = new Ajv({ allErrors: true });
const validate = ajv.compile(schema);

export function validateContinuityRecord(record: unknown) {
  const valid = validate(record);

  if (valid) {
    return {
      valid: true,
      errors: []
    };
  }

  return {
    valid: false,
    errors: validate.errors ?? []
  };
}
