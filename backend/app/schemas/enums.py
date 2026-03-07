import enum


class FacilityType(str, enum.Enum):
    FURNISHED = "furnished"
    SEMI_FURNISHED = "semi_furnished"
    PARKING = "parking"
    PRIVATE_BATHROOM = "private_bathroom"
    BALCONY = "balcony"
    WIFI = "wifi"


class ConstraintType(str, enum.Enum):
    SMOKING = "smoking"
    PETS = "pets"
    COUPLES = "couples"
    KIDS = "kids"
    VISITORS = "visitors"


class PropertyStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
