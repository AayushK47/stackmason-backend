import vine from '@vinejs/vine'

export const validateGetAllResourcesRequest = vine.compile(
  vine.object({
    regionId: vine.string().trim().doesExists({ table: 'regions', column: 'ulid' }),
  })
)
