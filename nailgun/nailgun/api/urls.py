from django.conf.urls import patterns, include, url
from piston.resource import Resource

from nailgun.api.handlers import EnvironmentCollectionHandler, \
                     EnvironmentHandler, \
                     NodeCollectionHandler, NodeHandler, NodeRoleAvailable, \
                     RecipeCollectionHandler, RecipeHandler, \
                     RoleCollectionHandler, RoleHandler, \
                     ReleaseCollectionHandler, ReleaseHandler, \
                     ConfigHandler, \
                     TaskHandler


class JsonResource(Resource):
    def determine_emitter(self, request, *args, **kwargs):
        return 'json'


urlpatterns = patterns('',
    url(r'^validators/node_role_available/\
(?P<node_id>[\dA-F]{12})/(?P<role_id>\d+)/?$',
        JsonResource(NodeRoleAvailable),
        name='node_role_available'),
    url(r'^environments/?$',
        JsonResource(EnvironmentCollectionHandler),
        name='environment_collection_handler'),
    url(r'^environments/(?P<environment_id>\d+)/?$',
        JsonResource(EnvironmentHandler),
        name='environment_handler'),
    url(r'^nodes/?$',
        JsonResource(NodeCollectionHandler),
        name='node_collection_handler'),
    url(r'^nodes/(?P<node_id>[\dA-F]{12})/?$',
        JsonResource(NodeHandler),
        name='node_handler'),
    url(r'^environments/(?P<environment_id>\d+)/chef-config/?$',
        JsonResource(ConfigHandler),
        name='config_handler'),
    url(r'^tasks/(?P<task_id>[\da-f\-]{36})/?$',
        JsonResource(TaskHandler),
        name='task_handler'),
    url(r'^recipes/?$',
        JsonResource(RecipeCollectionHandler),
        name='recipe_collection_handler'),
    url(r'^recipe/(?P<recipe_id>\d+)?$',
        JsonResource(RecipeHandler),
        name='recipe_handler'),
    url(r'^roles/?$',
        JsonResource(RoleCollectionHandler),
        name='role_collection_handler'),
    url(r'^roles/(?P<role_id>\d+)/?$',
        JsonResource(RoleHandler),
        name='role_handler'),
    url(r'^releases/?$',
        JsonResource(ReleaseCollectionHandler),
        name='release_collection_handler'),
    url(r'^releases/(?P<release_id>\d+)/?$',
        JsonResource(ReleaseHandler),
        name='release_handler'),
)
