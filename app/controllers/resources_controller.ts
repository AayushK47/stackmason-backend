import ResourceService from '#services/resource_service'
import { validateGetAllResourcesRequest } from '#validators/resource'
import { inject } from '@adonisjs/core'
import type { HttpContext } from '@adonisjs/core/http'

@inject()
export default class ResourcesController {
  constructor(private resourceService: ResourceService) {}
  async index({ request }: HttpContext) {
    const { regionId } = await validateGetAllResourcesRequest.validate(request.params())

    return await this.resourceService.getByRegion(regionId)
  }
}
