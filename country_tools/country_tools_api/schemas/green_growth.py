import graphene
from graphene.relay import Node

from sqlalchemy.orm import scoped_session, sessionmaker

from country_tools.country_tools_api.database.base import db_session
from country_tools.country_tools_api.database import green_growth as green_growth_db
from country_tools.country_tools_api.schemas.util import sqlalchemy_filter


class GGSupplyChainClusterProductMember(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGSupplyChainClusterProductMember
        interfaces = (Node,)

    supply_chain_id = graphene.Int()
    product_id = graphene.Int()
    cluster_id = graphene.Int()


class GGCountryYear(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGCountryYear
        interfaces = (Node,)

    country_id = graphene.Int()
    year = graphene.Int()
    coi_green = graphene.Float()
    lntotnetnrexp_pc = graphene.Float()
    lnypc = graphene.Float()
    x_resid = graphene.Float()
    policy_recommendation = graphene.String()
    strategy = graphene.String()
    rank = graphene.Int()
    ranking_metric = graphene.String()


class GGCountryProductYear(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGCountryProductYear
        interfaces = (Node,)

    year = graphene.Int()
    country_id = graphene.Int()
    product_id = graphene.Int()
    export_rca = graphene.Float()
    export_value = graphene.Float()
    expected_exports = graphene.Float()
    normalized_pci = graphene.Float()
    normalized_cog = graphene.Float()
    density = graphene.Float()
    global_market_share = graphene.Float()
    product_market_share_growth = graphene.Float()
    product_market_share = graphene.Float()
    pci_std = graphene.Float()
    cog_std = graphene.Float()
    feasibility_std = graphene.Float()
    strategy_balanced_portfolio = graphene.Float()
    strategy_long_jump = graphene.Float()
    strategy_low_hanging_fruit = graphene.Float()
    strategy_frontier = graphene.Float()


class GGCountryProductYearSupplyChain(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGCountryProductYearSupplyChain
        interfaces = (Node,)

    year = graphene.Int()
    country_id = graphene.Int()
    product_id = graphene.Int()
    supply_chain_id = graphene.Int()
    product_ranking = graphene.Int()


class GGClusterCountryYear(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGClusterCountryYear
        interfaces = (Node,)

    year = graphene.Int()
    country_id = graphene.Int()
    cluster_id = graphene.Int()
    pci = graphene.Float()
    cog = graphene.Float()
    density = graphene.Float()
    rca = graphene.Float()
    strategy_balanced_portfolio = graphene.Float()
    strategy_long_jump = graphene.Float()
    strategy_low_hanging_fruit = graphene.Float()
    strategy_frontier = graphene.Float()
    cluster_market_share = graphene.Float()


class GGSupplyChain(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGSupplyChain
        interfaces = (Node,)

    supply_chain_id = graphene.Int()
    supply_chain = graphene.String()


class GGCluster(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGCluster
        interfaces = (Node,)

    cluster_id = graphene.Int()
    cluster_name = graphene.String()


class GGLocationRegion(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGLocationRegion
        interfaces = (Node,)

    region_id = graphene.Int()
    name = graphene.String()
    region_code = graphene.String()
    country_id = graphene.Int()


class GGLocationCountry(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGLocationCountry
        interfaces = (Node,)

    country_id = graphene.Int()
    name_en = graphene.String()
    name_short_en = graphene.String()
    name_es = graphene.String()
    name_short_es = graphene.String()
    iso3_code = graphene.String()
    iso2_code = graphene.String()
    legacy_location_id = graphene.Int()
    parent_id = graphene.Int()
    name_abbr_en = graphene.String()
    the_prefix = graphene.Boolean()
    former_country = graphene.Boolean()
    rankings_override = graphene.Boolean()
    cp_override = graphene.Boolean()
    incomelevel_enum = graphene.String()
    country_project = graphene.Boolean()


class GGProduct(graphene.ObjectType):
    class Meta:
        model = green_growth_db.GGProduct
        interfaces = (Node,)

    product_id = graphene.Int()
    code = graphene.String()
    name_en = graphene.String()
    name_short_en = graphene.String()
    product_level = graphene.Int()
    parent_id = graphene.Int()
    product_id_hierarchy = graphene.String()
    top_parent_id = graphene.Int()
    show_feasibility = graphene.Boolean()


class GreenGrowthQuery(graphene.ObjectType):
    gg_product_list = graphene.List(GGProduct)
    gg_location_country_list = graphene.List(GGLocationCountry)
    gg_supply_chain_list = graphene.List(GGSupplyChain)
    gg_supply_chain_cluster_product_member_list = graphene.List(
        GGSupplyChainClusterProductMember,
        supply_chain_id=graphene.Int(required=True),
        cluster_id=graphene.Int(required=False),
        product_id=graphene.Int(required=False),
    )
    gg_cluster_list = graphene.List(GGCluster)
    gg_location_region_list = graphene.List(GGLocationRegion)
    gg_cluster_country_year_list = graphene.List(
        GGClusterCountryYear,
        cluster_id=graphene.Int(required=False),
        country_id=graphene.Int(required=True),
        year=graphene.Int(required=True),
    )
    gg_cpy_list = graphene.List(
        GGCountryProductYear,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=True),
    )
    gg_cpysc_list = graphene.List(
        GGCountryProductYearSupplyChain,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=True),
    )
    gg_country_year_list = graphene.List(
        GGCountryYear,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=False),
    )

    def resolve_gg_country_year_list(self, info, year, country_id=None):
        return (
            db_session.query(green_growth_db.GGCountryYear)
            .filter(green_growth_db.GGCountryYear.year == year)
            .filter(green_growth_db.GGCountryYear.country_id == country_id)
            .all()
            if country_id
            else db_session.query(green_growth_db.GGCountryYear)
            .filter(green_growth_db.GGCountryYear.year == year)
            .all()
        )

    def resolve_gg_cluster_country_year_list(self, info, cluster_id, country_id, year):
        return (
            db_session.query(green_growth_db.GGClusterCountryYear)
            .filter(green_growth_db.GGClusterCountryYear.cluster_id == cluster_id)
            .filter(green_growth_db.GGClusterCountryYear.country_id == country_id)
            .filter(green_growth_db.GGClusterCountryYear.year == year)
            .all()
        )

    def resolve_gg_cpy_list(self, info, year, country_id):
        return (
            db_session.query(green_growth_db.GGCountryProductYear)
            .filter(green_growth_db.GGCountryProductYear.year == year)
            .filter(green_growth_db.GGCountryProductYear.country_id == country_id)
            .all()
        )

    def resolve_gg_cpysc_list(self, info, year, country_id):
        return (
            db_session.query(green_growth_db.GGCountryProductYearSupplyChain)
            .filter(green_growth_db.GGCountryProductYearSupplyChain.year == year)
            .filter(
                green_growth_db.GGCountryProductYearSupplyChain.country_id == country_id
            )
            .all()
        )

    def resolve_gg_product_list(self, info, **args):
        return db_session.query(green_growth_db.GGProduct).all()

    def resolve_gg_location_country_list(self, info, **args):
        return db_session.query(green_growth_db.GGLocationCountry).all()

    def resolve_gg_cluster_list(self, info, **args):
        return db_session.query(green_growth_db.GGCluster).all()

    def resolve_gg_location_region_list(self, info, **args):
        return db_session.query(green_growth_db.GGLocationRegion).all()

    def resolve_gg_supply_chain_list(self, info, **args):
        return db_session.query(green_growth_db.GGSupplyChain).all()

    def resolve_gg_supply_chain_cluster_product_member_list(self, info, **args):
        return db_session.query(green_growth_db.GGSupplyChainClusterProductMember).all()
