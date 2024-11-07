/*
|--------------------------------------------------------------------------
| Routes file
|--------------------------------------------------------------------------
|
| The routes file is used for defining the HTTP routes.
|
*/

import router from '@adonisjs/core/services/router'
const RegionController = () => import('#controllers/regions_controller')
const ResourcesController = () => import('#controllers/resources_controller')

router
  .group(() => {
    router.get('', [RegionController, 'index'])
    router.get(':regionId/resources/', [ResourcesController, 'index'])
  })
  .prefix('api/regions')
