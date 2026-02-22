class APIV1PrefixConfig:
    prefix: str = "/v1"
    categories: str = "/categories"
    products: str = "/products"
    last_seen_products: str = "/products/last-seen"


class APIPrefixConfig:
    prefix: str = "/api"
    v1: APIV1PrefixConfig = APIV1PrefixConfig()


api_prefix_config = APIPrefixConfig()
