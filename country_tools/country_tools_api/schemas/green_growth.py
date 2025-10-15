import graphene
from sqlalchemy.orm import scoped_session, sessionmaker

from country_tools.country_tools_api.database.base import db_session
from country_tools.country_tools_api.database import green_growth as green_growth_db

from country_tools.country_tools_api.schemas.util import sqlalchemy_filter


class GGSupplyChainProductMember(graphene.ObjectType):

    supply_chain_id = graphene.Int()
    product_id = graphene.Int()


class GGCountryProductYear(graphene.ObjectType):

    year = graphene.Int()
    country_id = graphene.Int()
    product_id = graphene.Int()
    export_rca = graphene.Float()
    normalized_export_rca = graphene.Float()
    export_value = graphene.Float()
    expected_exports = graphene.Float()
    normalized_pci = graphene.Float()
    normalized_cog = graphene.Float()
    feasibility = graphene.Float()
    effective_number_of_exporters = graphene.Float()
    market_growth = graphene.Float()
    pci_std = graphene.Float()
    cog_std = graphene.Float()
    feasibility_std = graphene.Float()
    pci_cog_feasibility_composite = graphene.Float()


class GGCountryProductYearSupplyChain(graphene.ObjectType):

    year = graphene.Int()
    country_id = graphene.Int()
    product_id = graphene.Int()
    supply_chain_id = graphene.Int()
    product_ranking = graphene.Int()


class GGSupplyChain(graphene.ObjectType):

    supply_chain_id = graphene.Int()
    supply_chain = graphene.String()


class GGLocationCountry(graphene.ObjectType):

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
    gg_supply_chain_product_member_list = graphene.List(GGSupplyChainProductMember)
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

    def resolve_gg_cpy_list(self, info, year, country_id):
        return (
            db_session.query(green_growth_db.GGCountryProductYear)
            .filter(green_growth_db.GGCountryProductYear.year == year)
            .filter(green_growth_db.GGCountryProductYear.country_id == country_id)
        )

    def resolve_gg_cpysc_list(self, info, year, country_id):
        return (
            db_session.query(green_growth_db.GGCountryProductYearSupplyChain)
            .filter(green_growth_db.GGCountryProductYearSupplyChain.year == year)
            .filter(
                green_growth_db.GGCountryProductYearSupplyChain.country_id == country_id
            )
        )

    def resolve_gg_product_list(self, info, **args):
        return db_session.query(green_growth_db.GGProduct)

    def resolve_gg_location_country_list(self, info, **args):
        return db_session.query(green_growth_db.GGLocationCountry)

    def resolve_gg_supply_chain_list(self, info, **args):
        return db_session.query(green_growth_db.GGSupplyChain)

    def resolve_gg_supply_chain_product_member_list(self, info, **args):
        return db_session.query(green_growth_db.GGSupplyChainProductMember)