from base import Base
from albania import (
    NACEIndustry,
    Country,
    FDIMarkets,
    FDIMarketsOvertime,
    Factors,
    Script,
)

if __name__ == "__main__":
    Base.metadata.create_all()
