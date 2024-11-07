import { DateTime } from 'luxon'
import { BaseModel, column } from '@adonisjs/lucid/orm'

export default class RegionModel extends BaseModel {
  public static table = 'regions'

  @column({ isPrimary: true, serializeAs: null })
  declare id: number

  @column({ serializeAs: 'id' })
  declare ulid: string

  @column()
  declare regionId: string

  @column()
  declare regionName: string

  @column()
  declare createdAt: DateTime

  @column()
  declare updatedAt: DateTime
}
