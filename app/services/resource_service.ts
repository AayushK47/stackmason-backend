import RegionModel from '#models/region'
import ResourceModel from '#models/resource'

export default class ResourceService {
  async getByRegion(regionUlid: string): Promise<ResourceModel[]> {
    const region = await RegionModel.findBy({ ulid: regionUlid })
    return ResourceModel.findManyBy({ regionId: region?.id })
  }
}
