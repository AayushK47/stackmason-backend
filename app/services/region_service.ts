import RegionModel from '#models/region'

export default class RegionService {
  async get(): Promise<RegionModel[]> {
    return await RegionModel.all()
  }
}
