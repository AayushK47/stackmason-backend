import RegionModel from '#models/region'

export default class RegionService {
  async get() {
    return await RegionModel.all()
  }
}
