// import type { HttpContext } from '@adonisjs/core/http'

import RegionService from '#services/region_service'
import { inject } from '@adonisjs/core'

@inject()
export default class RegionsController {
  constructor(private regionService: RegionService) {}

  index() {
    return this.regionService.get()
  }
}
