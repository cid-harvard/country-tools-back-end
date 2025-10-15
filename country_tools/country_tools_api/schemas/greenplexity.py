import graphene
from graphene.relay import Node

from sqlalchemy.orm import scoped_session, sessionmaker

from country_tools.country_tools_api.database.base import db_session
from country_tools.country_tools_api.database import greenplexity as greenplexity_db
from country_tools.country_tools_api.schemas.util import sqlalchemy_filter


class GPSupplyChainClusterProductMember(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPSupplyChainClusterProductMember
        interfaces = (Node,)

    supply_chain_id = graphene.Int()
    product_id = graphene.Int()
    cluster_id = graphene.Int()


class GPCountryYear(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPCountryYear
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


class GPCountryProductYear(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPCountryProductYear
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


class GPCountryProductYearSupplyChain(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPCountryProductYearSupplyChain
        interfaces = (Node,)

    year = graphene.Int()
    country_id = graphene.Int()
    product_id = graphene.Int()
    supply_chain_id = graphene.Int()
    product_ranking = graphene.Int()


class GPClusterCountryYear(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPClusterCountryYear
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
    global_market_share = graphene.Float()


class GPSupplyChain(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPSupplyChain
        interfaces = (Node,)

    supply_chain_id = graphene.Int()
    supply_chain = graphene.String()


class GPCluster(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPCluster
        interfaces = (Node,)

    cluster_id = graphene.Int()
    cluster_name = graphene.String()


class GPLocationRegion(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPLocationRegion
        interfaces = (Node,)

    region_id = graphene.Int()
    name = graphene.String()
    region_code = graphene.String()
    country_id = graphene.Int()


class GPLocationCountry(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPLocationCountry
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


class GPProduct(graphene.ObjectType):
    class Meta:
        model = greenplexity_db.GPProduct
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


class GreenplexityQuery(graphene.ObjectType):
    gp_product_list = graphene.List(GPProduct)
    gp_product_list = graphene.List(GPLocationCountry)
    gp_product_list = graphene.List(GPSupplyChain)
    gp_product_list = graphene.List(
        GPSupplyChainClusterProductMember,
        supply_chain_id=graphene.Int(required=True),
        cluster_id=graphene.Int(required=False),
        product_id=graphene.Int(required=False),
    )
    gp_product_list = graphene.List(GPCluster)
    gp_product_list = graphene.List(GPLocationRegion)
    gp_product_list = graphene.List(
        GPClusterCountryYear,
        cluster_id=graphene.Int(required=False),
        country_id=graphene.Int(required=True),
        year=graphene.Int(required=True),
    )
    gp_product_list = graphene.List(
        GPCountryProductYear,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=True),
    )
    gp_product_list = graphene.List(
        GPCountryProductYearSupplyChain,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=True),
    )
    gp_product_list = graphene.List(
        GPCountryYear,
        year=graphene.Int(required=True),
        country_id=graphene.Int(required=False),
    )

    def resolve_gp_country_year_list(self, info, year, country_id=None):
        return (
            db_session.query(greenplexity_db.GPCountryYear)
            .filter(greenplexity_db.GPCountryYear.year == year)
            .filter(greenplexity_db.GPCountryYear.country_id == country_id)
            .all()
            if country_id
            else db_session.query(greenplexity_db.GPCountryYear)
            .filter(greenplexity_db.GPCountryYear.year == year)
            .all()
        )

    def resolve_gp_cluster_country_year_list(self, info, cluster_id, country_id, year):
        return (
            db_session.query(greenplexity_db.GPClusterCountryYear)
            .filter(greenplexity_db.GPClusterCountryYear.cluster_id == cluster_id)
            .filter(greenplexity_db.GPClusterCountryYear.country_id == country_id)
            .filter(greenplexity_db.GPClusterCountryYear.year == year)
            .all()
        )

    def resolve_gp_cpy_list(self, info, year, country_id):
        return (
            db_session.query(greenplexity_db.GPCountryProductYear)
            .filter(greenplexity_db.GPCountryProductYear.year == year)
            .filter(greenplexity_db.GPCountryProductYear.country_id == country_id)
            .all()
        )

    def resolve_gp_cpysc_list(self, info, year, country_id):
        return (
            db_session.query(greenplexity_db.GPCountryProductYearSupplyChain)
            .filter(greenplexity_db.GPCountryProductYearSupplyChain.year == year)
            .filter(
                greenplexity_db.GPCountryProductYearSupplyChain.country_id == country_id
            )
            .all()
        )

    def resolve_gp_product_list(self, info, **args):
        return db_session.query(greenplexity_db.GPProduct).all()

    def resolve_gp_location_country_list(self, info, **args):
        return db_session.query(greenplexity_db.GPLocationCountry).all()

    def resolve_gp_cluster_list(self, info, **args):
        return db_session.query(greenplexity_db.GPCluster).all()

    def resolve_gp_location_region_list(self, info, **args):
        return db_session.query(greenplexity_db.GPLocationRegion).all()

    def resolve_gp_supply_chain_list(self, info, **args):
        return db_session.query(greenplexity_db.GPSupplyChain).all()

    def resolve_gp_supply_chain_cluster_product_member_list(self, info, **args):
        return db_session.query(greenplexity_db.GPSupplyChainClusterProductMember).all()
