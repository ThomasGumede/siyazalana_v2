from django.db import models

class PaymentStatus(models.TextChoices):
        PAID = ("PAID", "Paid")
        PENDING = ("PENDING", "Pending")
        NOT_PAID = ("NOT PAID", "Not paid")
        CANCELLED = ("CANCELLED", "Cancelled")

WALLET_STATUS = (
    ("No status", "No status"),
    ("Requested Payout Details", "Requested Payout Details"),
    ("Verifying Payout Details", "Verifying Payout Details"),
    ("Approved Payout", "Approved Payout"),
    ("Payout Declined", "Payout Declined"),
    
)

TITLE_CHOICES = (
    ("Mr", "Mr"),
    ("Mrs", "Mrs"),
    ("Ms", "Ms"),
    ("Dr", "Dr"),
    ("Prof", "Prof.")
)

class StatusChoices(models.TextChoices):
    NOT_APPROVED = ("NOT APPROVED", "Not approved")
    PENDING = ("PENDING", "Pending")
    APPROVED = ("APPROVED", "Approved")
    COMPLETED = ("Completed", "Completed")
    BLOCKED = ("Blocked", "Blocked")

class IdentityNumberChoices(models.TextChoices):
    ID_NUMBER = ("ID_NUMBER", "ID number")
    PASSPORT = ("PASSPORT", "Passport")

class Gender(models.TextChoices):
    MALE = ("MALE", "Male")
    FEMALE = ("FEMALE", "Female")
    OTHER = ("OTHER", "Other")

class RelationShip(models.TextChoices):
    OTHER = ("OTHER", "Other")
    WIFE = ("WIFE", "Wife")
    HUSBAND = ("HUSBAND", "Husband")
    DAUGHTER = ("DAUGHTER", "Daughter")
    SON = ("SON", "Son")
    MOTHER = ("MOTHER", "Mother")
    FATHER = ("FATHER", "Father")
    STEPMOTHER = ("STEPMOTHER", "Step-mother")
    STEPFATHER = ("STEPFATHER", "Step-father")
    STEPBROTHER = ("STEPBROTHER", "Step-Brother")
    STEPSISTER = ("STEPSISTER", "Step-Sister")
    GRANDMOTHER = ("GRANDMOTHER", "Grandmother")
    GRANDFATHER = ("GRANDFATHER", "Grandfather")
    GREATGRANDMOTHER = ("GREATGRANDMOTHER", "Great Grandmother")
    GREATGRANDFATHER = ("GREATGRANDFATHER", "Great Grandfather")
    GREATGREATGRANDMOTHER = ("GREATGREATGRANDMOTHER", "Great Great Grandmother")
    GREATGREATGRANDFATHER = ("GREATGREATGRANDFATHER", "Great Great Grandfather")
    BROTHER = ("BROTHER", "Brother")
    SISTER = ("SISTER", "Sister")
    COUSIN = ("COUSIN", "Cousin")
    AUNT = ("AUNT", "Aunt")
    UNCLE = ("UNCLE", "Uncle")
    NEPHEW = ("NEPHEW", "Nephew")
    NIECE = ("NIECE", "Niece")

class RelationshipSides(models.TextChoices):
    MOTHER = ("MOTHER'S SIDE", "Mother's side")
    FATHER = ("FATHER'S SIDE", "Father's side")
    STEPMOTHER = ("STEPMOTHER'S SIDE", "Stepmother's side")
    STEPFATHER = ("STEPFATHER'S SIDE", "Stepfather's side")
    BROTHER = ("BROTHER'S SIDE", "Brother's side")
    SISTER = ("SISTER'S SIDE", "Sister's side")
    
class QualificationType(models.TextChoices):
    BACHELOR = ("BACHELOR", "Bachelor's Degree")
    MASTER = ("MASTER", "Master's Degree")
    DOCTORAL = ("DOCTORAL", "Doctoral Degree")
    POSTGRAD = ("POSTGRAD_CERT", "Postgraduate Certificate")
    HIGH_CERT = ("HIGH_CERTI", "Higher Certicate")
    ADVA_DIP = ("ADVANCE_DIP", "Advance Diploma")
    DIPLOMA = ("DIPLOMA", "Diploma")
    HONO = ("HONOURS", "Honour's Degree")
    MATRIC = ("MATRIC", "Grade 12 Matric")
    OTHER = ("OTHER", "Other")