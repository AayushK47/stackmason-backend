import type { FieldContext } from '@vinejs/vine/types'
import db from '@adonisjs/lucid/services/db'
import vine, { VineString } from '@vinejs/vine'

type Options = {
  table: string
  column: string
}

async function doesExists(value: unknown, options: Options, field: FieldContext) {
  if (typeof value !== 'string' && typeof value !== 'number') {
    return
  }

  const result = await db
    .from(options.table)
    .select(options.column)
    .where(options.column, value)
    .first()

  if (!result) {
    // Report that the value is NOT unique
    field.report('Value for {{ field }} does not exist', 'isExists', field)
  }
}

export const doesExistsRule = vine.createRule(doesExists)

declare module '@vinejs/vine' {
  interface VineString {
    doesExists(options: Options): this
  }
}

VineString.macro('doesExists', function (this: VineString, options: Options) {
  return this.use(doesExistsRule(options))
})
