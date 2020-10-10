from django.utils import timezone

from library.models import Item, ItemGroup


def create_item_record(
    itemgroup_id,
    library_id,
    serial_num,
    condition,
    availability,
    notes=None,
    date_acquired=None,
    last_inspected=None,
):
    """
    Creates and saves a new item record, creates an audit log entry for the new incoming inventory
    """

    item = Item(
        item_group=ItemGroup.objects.get(pk=itemgroup_id),
        library_id=library_id,
        serial_num=serial_num,
        condition=condition,
        availability=availability,
        notes=notes,
        date_acquired=date_acquired if date_acquired else timezone.now(),
        last_inspected=last_inspected if last_inspected else timezone.now(),
    )

    item.full_clean()
    item.save()

    # TODO: audit log entry

    return item


def create_itemgroup_record(make, model, description, moniker=None):
    itemgroup = ItemGroup(
        make=make, model=model, description=description, moniker=moniker
    )
    itemgroup.full_clean()
    itemgroup.save()
    return itemgroup
