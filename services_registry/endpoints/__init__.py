from aiohttp import web

from . import (service_info_handler,
               services_handler,
               dispatcher,
               cohorts,
               )

routes = [
    # Info
    web.get('/info'                         , service_info_handler.handler_info),
    web.get('/'                             , service_info_handler.handler_info),
    web.get('/service-info'                 , service_info_handler.handler_ga4gh_service_info),
    web.get('/bn_service_types'             , service_info_handler.handler_services_types),
    web.get('/services/types'               , service_info_handler.handler_ga4gh_services_types),
    web.get('/registered_services'          , service_info_handler.handler_registered_services),
    # Services info
    web.get('/bn_services'                  , services_handler.handler_services),
    web.get('/bn_services/{service_id}'     , services_handler.handler_services_by_id),
    web.get('/services'                     , services_handler.handler_ga4gh_services),
    web.get('/services/{service_id}'        , services_handler.handler_ga4gh_services_by_id),
    # Cohorts chapuza
    web.get('/cohorts'                      , cohorts.handler),
    # Dispatcher
    web.get('/api{anything:.+}'                , dispatcher.forward_get),
]
