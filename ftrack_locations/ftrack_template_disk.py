import os

import ftrack_api
import ftrack
import ftrack_template


def get_modified_component_path(path, name, padding, file_type):

    if padding:
        expression = "%0{0}d".format(padding)
    else:
        expression = "%d"

    replace_text = "{0}/{1}.{2}{3}".format(name, name, expression, file_type)

    original_filename = os.path.basename(path)

    return path.replace(original_filename, replace_text)


def get_new_location(session):

    location = session.query(
        "Location where name is \"project.disk.root\""
    ).one()
    location.accessor = ftrack_api.accessor.disk.DiskAccessor(prefix="")
    location.structure = NewStructure()
    location.priority = 50
    return location


class NewStructure(ftrack_api.structure.base.Structure):

    def get_resource_identifier(self, entity, context=None):

        templates = ftrack_template.discover_templates()

        path = ftrack_template.format({}, templates, entity=entity)[0]

        if entity.entity_type == "SequenceComponent":

            path = get_modified_component_path(path, entity['name'], entity["padding"], entity["file_type"])

        return os.path.abspath(path)


class OldStructure(ftrack.Structure):

    def getResourceIdentifier(self, entity):

        templates = ftrack_template.discover_templates()
        session = ftrack_api.Session()

        path = ftrack_template.format(
            {}, templates, entity=session.get("Component", entity.getId())
        )[0]

        if entity.isSequence():

            filetype = entity.getFileType()
            padding = entity.getPadding()
            name = entity.getName()

            path = get_modified_component_path(path, name, padding, filetype)

        return path


def get_old_location():

    location = ftrack.ensureLocation("project.disk.root")
    location.setAccessor(ftrack.DiskAccessor(prefix=""))
    location.setStructure(OldStructure())
    return location
