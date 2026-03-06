from django.db import transaction

from .models import Organisation, OrganisationMembership, OrganisationRole

def create_organisation(user, organisation_name):
    """
    Creates an organisation and assigns the creating user
    as the organisation ADMIN.

    This operation is atomic to prevent partial tenant creation.
    """

    with transaction.atomic():

        organisation - Organisation.objects.create(
            name=organisation_name,
            created_by=user,
        )

        OrganisationMembership.objects.create(
            user=user,
            organisation=organisation,
            role=OrganisationRole.ADMIN,
        )

    return organisation

def get_user_memberships(user):
    """
    Returns all organisation memberships for a given user.
    """

    return OrganisationMembership.objects.filter(user=user).select_related("organisation")
