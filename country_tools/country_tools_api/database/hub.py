from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum, ARRAY, UniqueConstraint

project_categories = Enum(
    *[
        "atlas_projects",
        "annual_best_of",
        "country_dashboards",
        "visual_stories",
        "prototypes_experiments",
        "presentations",
        "software_packages",
    ],
    name="project_categories"
)
card_sizes = Enum(*["small", "medium", "large"], name="card_sizes")
project_statuses = Enum(*["active", "archived", "complete"], name="project_statuses")


class HubProjects(Base):

    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("ordering", name="uix_ordering"),
        {"schema": "hub"},
    )

    project_name = Column(String, primary_key=True)
    link = Column(String)
    local_file = Column(Boolean)
    project_category = Column(project_categories)
    show = Column(Boolean)
    data = Column(ARRAY(String))
    keywords = Column(ARRAY(String))
    card_size = Column(card_sizes)
    announcement = Column(String)
    ordering = Column(Integer)
    status = Column(project_statuses)
    card_image_hi = Column(String)
    card_image_lo = Column(String)

