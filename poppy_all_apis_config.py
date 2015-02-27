from oslo_config import cfg
from oslo_config import types

NonNegativeInt = types.Integer(min=0)

cfg.CONF.register_opts([
    cfg.StrOpt('tenant_id', help='the tenant used for all requests'),
    # TODO: maybe this should be api_key or password and the test auto-fetches a token
    cfg.StrOpt('token', help='a valid token for the tenant'),
    cfg.StrOpt('host', help='the API endpoint'),
    cfg.Opt('min_wait', type=NonNegativeInt, default=1000,
            help='the min wait time between tasks in milliseconds'),
    cfg.Opt('max_wait', type=NonNegativeInt, default=1000,
            help='the max wait time between tasks in milliseconds'),
    cfg.ListOpt('flavors', default=['cdn'],
                help='a list of flavor ids to use for GETs'),
], group='test:perf')

cfg.CONF.register_opts([
    cfg.Opt("create_service", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("update_service_domain", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("update_service_rule", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("update_service_origin", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("delete_service", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("delete_asset", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("delete_all_assets", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("list_services", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("get_service", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("list_flavors", type=NonNegativeInt, default=0,
            help='the weight for this task'),
    cfg.Opt("get_flavors", type=NonNegativeInt, default=0,
            help='the weight for this task'),
], group='test:perf:weights')
