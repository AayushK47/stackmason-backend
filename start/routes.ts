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

router.group(() => {
  router.get('region', [RegionController, 'index'])
})
