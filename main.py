import xml.etree.ElementTree as ET


def findElement(start, id):
    for element in start.iter():
        if element.get("id") != None:
            if element.get("id") == id:
                return element


def findParent(childObject, startObject):
    for child in startObject:
        if child == childObject:
            return startObject
        else:
            if findParent(childObject, child) != None:
                return findParent(childObject, child)


def findSequenceFlowTarget(start, targetRef):
    if targetRef is not None:
        for flow in start.findall("{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"):
            if flow.get("targetRef") == targetRef:
                return flow


def findSequenceFlowSource(start, sourceRef):
    if sourceRef is not None:
        for flow in start.findall("{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"):
            if flow.get("sourceRef") == sourceRef:
                return flow


def findBoundaryEvent(start, attachedTo):
    for event in start.findall("{http://www.omg.org/spec/BPMN/20100524/MODEL}boundaryEvent"):
        if event.get("attachedToRef") == attachedTo:
            return event


def finddiElement(start, element):
    if element is not None:
        for object in start.iter():
            if object.get("bpmnElement") == element:
                return object


def getdiElementPosition(element):
    if element is not None:
        return element.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")


def removeAllChilds(parent):
    if parent is not None:
        for child in parent.findall("{http://www.omg.org/spec/DD/20100524/DI}waypoint"):
            parent.remove(child)


def removeAllBounds(parent):
    if parent is not None:
        for child in parent.findall("{http://www.omg.org/spec/DD/20100524/DC}Bounds"):
            parent.remove(child)


def addbpmnShape(parent, id, x, y, width, height):
    shape = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNShape",
                          {"id": id + "_di", "bpmnElement": id})
    ET.SubElement(shape, "{http://www.omg.org/spec/DD/20100524/DC}Bounds",
                  {"x": str(x), "y": str(y), "width": width, "height": height})
    return shape


def addbmpnShapeLabel(parent, id, x, y, width, height):
    shape = addbpmnShape(parent, id, x, y, width, height)
    label = ET.SubElement(shape, "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNLabel")
    ET.SubElement(label, "{http://www.omg.org/spec/DD/20100524/DC}Bounds",
                  {"x": str(x), "y": str(y), "width": width, "height": height})
    return shape


def addbpmnShapeSubP(parent, id, x, y, width, height, isExpanded):
    shape = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNShape",
                          {"id": id + "_di", "bpmnElement": id, "isExpanded": str(isExpanded)})
    ET.SubElement(shape, "{http://www.omg.org/spec/DD/20100524/DC}Bounds",
                  {"x": str(x), "y": str(y), "width": width, "height": height})
    return shape


def addbmpnShapeSubPLabel(parent, id, x, y, width, height, isExpanded):
    shape = addbpmnShapeSubP(parent, id, x, y, width, height, isExpanded)
    label = ET.SubElement(shape, "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNLabel")
    ET.SubElement(label, "{http://www.omg.org/spec/DD/20100524/DC}Bounds",
                  {"x": str(x), "y": str(y), "width": width, "height": height})
    return shape


def addbpmnEdge(parent, id):
    edge = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNEdge",
                         {"id": id + "_di", "bpmnElement": id})
    return edge


def removeObjectFromXML(start, object):
    for element in start.iter():
        if element.get("id") == object.get("id"):
            findParent(element, start).remove(object)


def addbpmnWaypoint(parent, x, y):
    waypoint = ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(x), "y": str(y)})
    return waypoint


def addbpmnWaypointWithObjectsLeftRight(start, sequence_flow):
    parent = finddiElement(start, sequence_flow.get("id"))
    source = finddiElement(start, sequence_flow.get("sourceRef"))
    sourceBounds = source.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    sourceX = int(sourceBounds.get("x")) + int(sourceBounds.get("width"))
    sourceY = int(sourceBounds.get("y")) + int(sourceBounds.get("height")) / 2
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(sourceX), "y": str(sourceY)})
    target = finddiElement(start, sequence_flow.get("targetRef"))
    targetBounds = target.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    targetX = int(targetBounds.get("x"))
    targetY = int(targetBounds.get("y")) + int(targetBounds.get("height")) / 2
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(targetX), "y": str(targetY)})


def addbpmnWaypointWithObjectsTopRight(start, sequence_flow):
    parent = finddiElement(start, sequence_flow.get("id"))
    source = finddiElement(start, sequence_flow.get("sourceRef"))
    sourceBounds = source.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    sourceX = int(sourceBounds.get("x")) + int(sourceBounds.get("width")) / 2
    sourceY = int(sourceBounds.get("y"))
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(sourceX), "y": str(sourceY)})
    target = finddiElement(start, sequence_flow.get("targetRef"))
    targetBounds = target.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    targetX = int(targetBounds.get("x")) + int(targetBounds.get("width"))
    targetY = int(targetBounds.get("y")) + int(sourceBounds.get("height")) / 2
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(targetX), "y": str(targetY)})


def addbpmnWaypointWithObjectsTopBottom(start, sequence_flow):
    parent = finddiElement(start, sequence_flow.get("id"))
    source = finddiElement(start, sequence_flow.get("sourceRef"))
    sourceBounds = source.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    sourceX = int(sourceBounds.get("x")) + int(sourceBounds.get("width")) / 2
    sourceY = int(sourceBounds.get("y")) + int(sourceBounds.get("height"))
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(sourceX), "y": str(sourceY)})
    target = finddiElement(start, sequence_flow.get("targetRef"))
    targetBounds = target.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    targetX = int(targetBounds.get("x")) + int(targetBounds.get("width")) / 2
    targetY = int(targetBounds.get("y"))
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(targetX), "y": str(targetY)})


def addbpmnWaypointWithObjectsTopTop(start, sequence_flow):
    parent = finddiElement(start, sequence_flow.get("id"))
    source = finddiElement(start, sequence_flow.get("sourceRef"))
    sourceBounds = source.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    sourceX = int(sourceBounds.get("x")) + int(sourceBounds.get("width")) / 2
    sourceY = int(sourceBounds.get("y"))
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(sourceX), "y": str(sourceY)})
    target = finddiElement(start, sequence_flow.get("targetRef"))
    targetBounds = target.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
    targetX = int(targetBounds.get("x")) + int(targetBounds.get("width")) / 2
    targetY = int(targetBounds.get("y"))
    ET.SubElement(parent, "{http://www.omg.org/spec/DD/20100524/DI}waypoint", {"x": str(targetX), "y": str(targetY)})


def shiftLeft(start, centerObject, shift_length, process):
    flowsToCorrect = []
    center_x = int(
        finddiElement(start, centerObject.get("id")).find("{http://www.omg.org/spec/DD/20100524/DC}Bounds").get("x"))
    center_y = int(
        finddiElement(start, centerObject.get("id")).find("{http://www.omg.org/spec/DD/20100524/DC}Bounds").get("y"))
    # shift_length = int(finddiElement(start,newObject.get("id")).find("{http://www.omg.org/spec/DD/20100524/DC}Bounds").get("width")) + 100

    for element in start.iter():
        if element.tag == "{http://www.omg.org/spec/DD/20100524/DI}waypoint":
            x = int(float(element.get("x")))
            if x < center_x:
                x = x - shift_length - 50
                element.set("x", str(x))
        if element.tag == "{http://www.omg.org/spec/DD/20100524/DC}Bounds":
            x = int(float(element.get("x")))
            x_width = x + int(float(element.get("width")))
            if x < center_x:
                if center_x < x_width and findParent(element, start).tag == "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNShape":
                    if findElement(start, findParent(element, start).get("bpmnElement")).tag != "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObjectReference":
                        #print(findParent(element, start).get("bpmnElement"))
                        flow_to_shift = findSequenceFlowSource(process, findParent(element, start).get("bpmnElement"))
                        flowsToCorrect.append(flow_to_shift)
                x = x - shift_length - 50
                element.set("x", str(x))


    for element_flow in flowsToCorrect:
        if element_flow != None:
            removeAllChilds(finddiElement(start, element_flow.get("id")))
            addbpmnWaypointWithObjectsLeftRight(start, element_flow)


def shiftUp(start, centerObject, shift_length):
    center = int(
        finddiElement(start, centerObject.get("id")).find("{http://www.omg.org/spec/DD/20100524/DC}Bounds").get("y"))
    # shift_length = int(finddiElement(start,newObject.get("id")).find("{http://www.omg.org/spec/DD/20100524/DC}Bounds").get("height")) + 100

    for element in start.iter():
        if element.tag == "{http://www.omg.org/spec/DD/20100524/DI}waypoint":
            y = float(element.get("y"))
            if y < center:
                y = y - shift_length - 50
                element.set("y", str(y))
        if element.tag == "{http://www.omg.org/spec/DD/20100524/DC}Bounds":
            y = float(element.get("y"))
            if y < center:
                y = y - shift_length - 50
                element.set("y", str(y))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    ###############################
    ###############################
    ###############################
    tree = ET.parse('Case1.bpmn') # <----------------- !!!!!!!!!CHANGE .bpmn file which is to translate!!!!!!!!!!!!!!!!
    ############################### ----------> new file is stored or overwritten as Translated_Model.bpmn
    ###############################
    ###############################



    root = tree.getroot()
    for element in root:
        if element.tag == "{http://www.omg.org/spec/BPMN/20100524/MODEL}process":
            process = element
        if element.tag == "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNDiagram":
            BPdiagram = element
            for lane in BPdiagram:
                if lane.tag == "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNPlane":
                    BPlane = lane
    i = 0

    IoTChilds = []
    objectsToBeRemoved = []
    for child in root.iter():
        for att in child.attrib:
            if (att == "{http://some-company/schema/bpmn/iot}type"):
                IoTChilds.append(child)
        i = i + 1

    # -----> actor & actor-sub replacement
    for IoTChild in IoTChilds:

        # IoTChild contains all elements with the attribute iot type
        for child in root.iter():

            # check if element has IoT element in text which would mean that the element is child of a data output
            # association (for the actor artifact)
            # & check if IoTChild is of type actor
            if (IoTChild.attrib.get("id") == child.text
                    and (IoTChild.attrib.get(
                    "{http://some-company/schema/bpmn/iot}type") == "actor-sub" or IoTChild.attrib.get(
                    "{http://some-company/schema/bpmn/iot}type") == "actor")):

            #get parent which is a data output association
                dataOutputAssociation = findParent(child, root)
            #get task associated with the data output association
                parent = findParent(dataOutputAssociation, root)
            #modify parent tag and turn it into service task (see Transformation Rule Actor)
                parent.tag = "{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
                print("actor replaced")

            #add IoTChild and the data output association and their diagram elements (positioning and size)
            #to the objectsToBeRemoved array
                objectsToBeRemoved.append(IoTChild)
                objectsToBeRemoved.append(finddiElement(BPlane, IoTChild.get("id")))
                objectsToBeRemoved.append(dataOutputAssociation)
                objectsToBeRemoved.append(finddiElement(BPlane, dataOutputAssociation.get("id")))

    i = 0
    # ------> sensor replacement
    for IoTChild in IoTChilds:
        for child in root.iter():
            if IoTChild.attrib.get("id") == child.text and (
                    IoTChild.attrib.get("{http://some-company/schema/bpmn/iot}type") == "sensor" or IoTChild.attrib.get(
                    "{http://some-company/schema/bpmn/iot}type") == "sensor-sub"):
                i = i + 1

                # get old task, which gets sensor data
                old_sensor_task = findParent(findParent(child, root), root)

                # get old task positioning
                old_sensor_task_di = finddiElement(BPlane, old_sensor_task.get("id"))
                old_sensor_task_di_position = getdiElementPosition(old_sensor_task_di)

                # get old task parent element
                parent = findParent(old_sensor_task, process)

                # create new business rule task, which gets sensor data
                new_call_sensor_task = ET.SubElement(parent,
                                                     "{http://www.omg.org/spec/BPMN/20100524/MODEL}businessRuleTask",
                                                     {"id": "translatedsensortask" + str(i),
                                                      "name": "Get " + IoTChild.get("name") + " data"})

                # shift everything to left (center = old task)
                shiftLeft(root, old_sensor_task, 100,process)

                # create positioning of the business rule task
                new_shape = addbpmnShape(BPlane, new_call_sensor_task.get("id"),
                                         int(old_sensor_task_di_position.get("x")) - 150,
                                         int(old_sensor_task_di_position.get("y")),
                                         old_sensor_task_di_position.get("width"),
                                         old_sensor_task_di_position.get("height"))

                # get incoming sequence flow of old task and redirect to new task
                sequence_flow = findSequenceFlowTarget(process, old_sensor_task.get("id"))
                old_sequence_flow_id = findSequenceFlowTarget(process, old_sensor_task.get("id")).get("id")
                sequence_flow.set("targetRef", new_call_sensor_task.get("id"))
                removeAllChilds(finddiElement(BPlane, sequence_flow.get("id")))
                addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)

                # create arrows from business rule task to old task
                ET.SubElement(new_call_sensor_task,
                              "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = sequence_flow.get("id")
                sequence_flow = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                              {"id": "translated_sensor_task_sequence_flow" + str(i),
                                               "sourceRef": new_call_sensor_task.get("id"),
                                               "targetRef": old_sensor_task.get("id")})
                addbpmnEdge(BPlane, sequence_flow.get("id"))
                ET.SubElement(new_call_sensor_task,
                              "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = sequence_flow.get("id")
                addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)

                # create data object and object reference
                new_sensor_data_object = ET.SubElement(parent,
                                                       "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObject",
                                                       {"id": "SensorData" + str(i)})
                translated_sensor_ref_text = "translatedSensorRef" + str(i) + "name"
                translated_sensor_ref_text_name = translated_sensor_ref_text + "name"
                sensor_data_ref = ET.SubElement(parent,
                                                "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObjectReference",
                                                {"id": translated_sensor_ref_text, "name": "sensor data",
                                                 "dataObjectRef": new_sensor_data_object.attrib.get("id")})
                addbpmnShape(BPlane, sensor_data_ref.get("id"), int(old_sensor_task_di_position.get("x")),
                             int(old_sensor_task_di_position.get("y")) - 86, "36", "50")

                # create new sequence flow and edit old sequence flow
                for a in old_sensor_task:
                    if a.tag == "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming" and a.text == old_sequence_flow_id:
                        a.text = sequence_flow.get("id")

                # create data output association for new business rule task and edit old data input association of old task
                sensor_data_output_association_id = "translatedOutputAssociation" + str(i)
                sensor_data_output_association = ET.SubElement(new_call_sensor_task,
                                                               "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataOutputAssociation",
                                                               {"id": sensor_data_output_association_id})
                sensor_data_output_association_target = ET.SubElement(sensor_data_output_association,
                                                                      "{http://www.omg.org/spec/BPMN/20100524/MODEL}targetRef")
                sensor_data_output_association_target.text = sensor_data_ref.attrib.get("id")
                old_sensor_task.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}dataInputAssociation").find(
                    "{http://www.omg.org/spec/BPMN/20100524/MODEL}sourceRef").text = sensor_data_ref.get("id")
                removeAllChilds(finddiElement(BPlane, old_sensor_task.find(
                    "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataInputAssociation").get("id")))
                addbpmnEdge(BPlane, sensor_data_output_association.get("id"))
                print("sensor replaced")
                objectsToBeRemoved.append(IoTChild)
                objectsToBeRemoved.append(finddiElement(BPlane, IoTChild.get("id")))

    for child in root.iter():
        if child.tag == "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObjectReference" and (
                child.attrib.get("{http://some-company/schema/bpmn/iot}type") == "artefact-catch" or child.attrib.get(
                "{http://some-company/schema/bpmn/iot}type") == "artefact-catch-sub"):
            artifact = child
            for a in root.iter():
                i = i + 1
                if artifact.attrib.get("id") == a.text and (
                        findParent(findParent(a, root), root) not in objectsToBeRemoved):

                    # get artifact_task connected with catch artifact
                    artifact_task = findParent(findParent(a, root), root)

                    # get parent of artifact_task and artifact_task positioning
                    parent = findParent(artifact_task, process)
                    artifact_task_position = getdiElementPosition(finddiElement(BPlane, artifact_task.get("id")))

                    # get boundary event of artifact_task
                    boundary_event = findBoundaryEvent(process, artifact_task.attrib.get("id"))
                    removeAllBounds(finddiElement(BPlane, boundary_event.get("id")))

                    # get incoming and outgoing sequence flows of artifact_task
                    outgoing_arrow_artifact_task = findSequenceFlowSource(process, artifact_task.get("id"))
                    incoming_arrow_artifact_task = findSequenceFlowTarget(process, artifact_task.get("id"))
                    removeAllChilds(finddiElement(BPlane, outgoing_arrow_artifact_task.get("id")))
                    removeAllChilds(finddiElement(BPlane, incoming_arrow_artifact_task.get("id")))

                    # create new subprocess
                    translated_subprocess = ET.SubElement(parent,
                                                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}subProcess",
                                                          {"id": "translatedSubprocess" + str(i)})

                    # shift everything left (center = artifact_task)
                    shiftLeft(root, artifact_task, 500,process)

                    # create subprocess positioning
                    subprocess_di = addbpmnShapeSubP(BPlane, translated_subprocess.get("id"),
                                                     int(artifact_task_position.get("x")) - 550,
                                                     int(artifact_task_position.get("y")) - 120, "500", "300",
                                                     "true").find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
                    # set incoming and outgoing sequence flows of subprocess
                    ET.SubElement(translated_subprocess,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = incoming_arrow_artifact_task.get(
                        "id")
                    ET.SubElement(translated_subprocess,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = outgoing_arrow_artifact_task.get(
                        "id")
                    outgoing_arrow_artifact_task.set("sourceRef", translated_subprocess.get("id"))
                    incoming_arrow_artifact_task.set("targetRef", translated_subprocess.get("id"))
                    addbpmnWaypointWithObjectsLeftRight(BPlane, outgoing_arrow_artifact_task)
                    addbpmnWaypointWithObjectsLeftRight(BPlane, incoming_arrow_artifact_task)

                    # attach boundary event to subprocess
                    boundary_event.set("attachedToRef", translated_subprocess.get("id"))
                    boundary_bounds = ET.SubElement(finddiElement(BPlane, boundary_event.get("id")),
                                                    "{http://www.omg.org/spec/DD/20100524/DC}Bounds",
                                                    {"x": str(int(subprocess_di.get("x")) + 250),
                                                     "y": str(int(subprocess_di.get("y")) + 282), "width": "36",
                                                     "height": "36"})
                    finddiElement(BPlane, boundary_event.get("id")).find(
                        "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNLabel").find(
                        "{http://www.omg.org/spec/DD/20100524/DC}Bounds").set("x", boundary_bounds.get("x"))
                    finddiElement(BPlane, boundary_event.get("id")).find(
                        "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNLabel").find(
                        "{http://www.omg.org/spec/DD/20100524/DC}Bounds").set("y",
                                                                              str(int(boundary_bounds.get("y")) + 42))
                    # boundary_event_sequence_flow = ET.SubElement(parent,"{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",{"id":"boundary_sequence_flow","sourceRef":boundary_event.get("id"),"targetRef":outgoing_arrow_artifact_task.get("targetRef")})
                    boundary_event_sequence_flow = findSequenceFlowSource(process,boundary_event.get("id"))
                    removeAllChilds(finddiElement(BPlane,boundary_event_sequence_flow.get("id")))
                    addbpmnWaypointWithObjectsLeftRight(BPlane,boundary_event_sequence_flow)

                    # create start event in suborocess and create positioning
                    subprocess_start_event = ET.SubElement(translated_subprocess,
                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}startEvent",
                                                           {"id": "new_start_event_subprocess" + str(i)})
                    addbpmnShape(BPlane, subprocess_start_event.get("id"), int(subprocess_di.get("x")) + 40,
                                 int(subprocess_di.get("y")) + 75, "36", "36")

                    # create task in subprocess and create positioning
                    subprocess_actor_task = ET.SubElement(translated_subprocess, artifact_task.tag,
                                                          {"id": "new_actor_task_subprocess" + str(i), "name": artifact_task.get("name")})
                    addbpmnShape(BPlane, subprocess_actor_task.get("id"), int(subprocess_di.get("x")) + 150,
                                 int(subprocess_di.get("y")) + 50, artifact_task_position.get("width"),
                                 artifact_task_position.get("height"))

                    #create sequence flow for start event and task
                    subprocess_first_arrow = ET.SubElement(translated_subprocess,
                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                                           {"id": "new_sequence_flow_subprocess_1" + str(i),
                                                            "sourceRef": subprocess_start_event.get("id"),
                                                            "targetRef": subprocess_actor_task.get("id")})
                    addbpmnEdge(BPlane, subprocess_first_arrow.get("id"))
                    addbpmnWaypointWithObjectsLeftRight(BPlane, subprocess_first_arrow)
                    ET.SubElement(subprocess_start_event,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = subprocess_first_arrow.get(
                        "id")
                    ET.SubElement(subprocess_actor_task,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = subprocess_first_arrow.get(
                        "id")

                    # create sensor task and create positioning
                    subprocess_sensor_task = ET.SubElement(translated_subprocess,
                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}businessRuleTask",
                                                           {"id": "new_sensor_task_subprocess" + str(i), "name": "Get sensor data"})
                    addbpmnShape(BPlane, subprocess_sensor_task.get("id"), int(subprocess_di.get("x")) + 150,
                                 int(subprocess_di.get("y")) + 200, artifact_task_position.get("width"),
                                 artifact_task_position.get("height"))

                    # create sequence flow for task and sensortask
                    subprocess_second_arrow = ET.SubElement(translated_subprocess,
                                                            "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                                            {"id": "new_sequence_flow_subprocess_2" + str(i),
                                                             "sourceRef": subprocess_actor_task.get("id"),
                                                             "targetRef": subprocess_sensor_task.get("id")})
                    addbpmnEdge(BPlane, subprocess_second_arrow.get("id"))
                    addbpmnWaypointWithObjectsTopBottom(BPlane, subprocess_second_arrow)
                    ET.SubElement(subprocess_actor_task,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = subprocess_second_arrow.get(
                        "id")
                    ET.SubElement(subprocess_sensor_task,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = subprocess_second_arrow.get(
                        "id")

                    # create exclusive gateway
                    subprocess_exclusive_gateway = ET.SubElement(translated_subprocess,
                                                                 "{http://www.omg.org/spec/BPMN/20100524/MODEL}exclusiveGateway",
                                                                 {"id": "new_exclusive_gateway_subprocess" + str(i),
                                                                  "name": child.get("name")})
                    addbpmnShape(BPlane, subprocess_exclusive_gateway.get("id"), int(subprocess_di.get("x")) + 300,
                                 int(subprocess_di.get("y")) + 225, "36", "36")

                    # create sequence flow gateway to task
                    subprocess_third_arrow = ET.SubElement(translated_subprocess,
                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                                           {"id": "new_sequence_flow_subprocess_3" + str(i),
                                                            "sourceRef": subprocess_sensor_task.get("id"),
                                                            "targetRef": subprocess_exclusive_gateway.get("id")})
                    addbpmnEdge(BPlane, subprocess_third_arrow.get("id"))
                    addbpmnWaypointWithObjectsLeftRight(BPlane, subprocess_third_arrow)
                    ET.SubElement(subprocess_sensor_task,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = subprocess_third_arrow.get(
                        "id")
                    ET.SubElement(subprocess_exclusive_gateway,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = subprocess_third_arrow.get(
                        "id")
                    # create sequence flow sensor task to gateway
                    subprocess_fourth_arrow = ET.SubElement(translated_subprocess,
                                                            "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                                            {"id": "new_sequence_flow_subprocess_4" + str(i), "name": "No",
                                                             "sourceRef": subprocess_exclusive_gateway.get("id"),
                                                             "targetRef": subprocess_actor_task.get("id")})
                    addbpmnEdge(BPlane, subprocess_fourth_arrow.get("id"))
                    addbpmnWaypointWithObjectsTopRight(BPlane, subprocess_fourth_arrow)
                    ET.SubElement(subprocess_exclusive_gateway,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = subprocess_fourth_arrow.get(
                        "id")
                    ET.SubElement(subprocess_sensor_task,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = subprocess_fourth_arrow.get(
                        "id")
                    # create end event for subprocess
                    subprocess_end_event = ET.SubElement(translated_subprocess,
                                                         "{http://www.omg.org/spec/BPMN/20100524/MODEL}endEvent",
                                                         {"id": "new_end_event_subprocess" + str(i)})
                    addbpmnShape(BPlane, subprocess_end_event.get("id"), int(subprocess_di.get("x")) + 400,
                                 int(subprocess_di.get("y")) + 225, "36", "36")

                    # create sequence flow gateway to end event
                    subprocess_fifth_arrow = ET.SubElement(translated_subprocess,
                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                                           {"id": "new_sequence_flow_subprocess_5" + str(i), "name": "Yes",
                                                            "sourceRef": subprocess_exclusive_gateway.get("id"),
                                                            "targetRef": subprocess_end_event.get("id")})
                    addbpmnEdge(BPlane, subprocess_fifth_arrow.get("id"))
                    addbpmnWaypointWithObjectsLeftRight(BPlane, subprocess_fifth_arrow)
                    ET.SubElement(subprocess_exclusive_gateway,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = subprocess_fifth_arrow.get(
                        "id")
                    ET.SubElement(subprocess_end_event,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = subprocess_fifth_arrow.get(
                        "id")

                    print("catch artifact replaced")
                    objectsToBeRemoved.append(artifact_task)
                    objectsToBeRemoved.append(finddiElement(BPlane, artifact_task.get("id")))
                    dataInputAssociation = findParent(a, root)
                    objectsToBeRemoved.append(finddiElement(BPlane, dataInputAssociation.get("id")))
                else:
                    if artifact.attrib.get("id") == a.text:
                        dataInputAssociation = findParent(a, root)
                        objectsToBeRemoved.append(finddiElement(BPlane, dataInputAssociation.get("id")))
            dataObject = findElement(process, child.get("dataObjectRef"))
            objectsToBeRemoved.append(child)
            objectsToBeRemoved.append(dataObject)
            objectsToBeRemoved.append(finddiElement(BPlane, child.get("id")))

    for child in root.iter():
        if child.tag == "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObjectReference" and child.get(
                "{http://some-company/schema/bpmn/iot}type") == "obj":
            object_artifact = child
            for a in root.iter():
                i = i + 1
                if object_artifact.get("id") == a.text and (child not in objectsToBeRemoved):

                    # get artifact_task
                    object_artifact_task = findParent(findParent(a, root), root)

                    # get parent of artifact_task and positioning
                    parent = findParent(object_artifact_task, process)
                    object_artifact_task_di = getdiElementPosition(
                        finddiElement(BPlane, object_artifact_task.get("id")))

                    # get incoming and outgoing sequence flows
                    outgoing_arrow_artifact_task = findSequenceFlowSource(parent, object_artifact_task.get("id"))
                    incoming_arrow_artifact_task = findSequenceFlowTarget(parent, object_artifact_task.get("id"))
                    removeAllChilds(finddiElement(BPlane, outgoing_arrow_artifact_task.get("id")))
                    removeAllChilds(finddiElement(BPlane, incoming_arrow_artifact_task.get("id")))

                    # Create sensor task
                    translated_object_artifact_sensor_task = ET.SubElement(parent,
                                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}businessRuleTask",
                                                                           {
                                                                               "id": "translated_object_artifact_sensor_task" + str(i),
                                                                               "name": "Get " + object_artifact.get(
                                                                                   "name") + " data"})
                    shiftLeft(root, object_artifact_task, 100,process)
                    addbpmnShape(BPlane, translated_object_artifact_sensor_task.get("id"),
                                 int(object_artifact_task_di.get("x")) - 150, int(object_artifact_task_di.get("y")),
                                 object_artifact_task_di.get("width"), object_artifact_task_di.get("height"))

                    # Create actor task
                    # translated_object_artifact_actor_task = ET.SubElement(parent,"{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask",{"id":"translated_object_artifact_actor_task","name":object_artifact.get("name")})
                    # addbpmnShape(BPlane,translated_object_artifact_actor_task.get("id"),int(object_artifact_task_di.get("x")) + 150,int(object_artifact_task_di.get("y")),object_artifact_task_di.get("width"),object_artifact_task_di.get("height"))
                    object_artifact_task.tag = "{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"
                    # Create sequence flow sensor to actor
                    new_arrow_sensor_to_task = ET.SubElement(parent,
                                                             "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                                             {"id": "new_object_artifact_sequence_flow_1" + str(i),
                                                              "sourceRef": translated_object_artifact_sensor_task.get(
                                                                  "id"), "targetRef": object_artifact_task.get("id")})
                    ET.SubElement(translated_object_artifact_sensor_task,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = new_arrow_sensor_to_task.get(
                        "id")
                    for b in object_artifact_task:
                        if b.tag == "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming" and b.text == incoming_arrow_artifact_task.get(
                                "id"):
                            b.text = new_arrow_sensor_to_task.get("id")
                    addbpmnEdge(BPlane, new_arrow_sensor_to_task.get("id"))
                    addbpmnWaypointWithObjectsLeftRight(BPlane, new_arrow_sensor_to_task)

                    # Shift old sequence flows to sensor and actor
                    incoming_arrow_artifact_task.set("targetRef", translated_object_artifact_sensor_task.get("id"))
                    ET.SubElement(translated_object_artifact_sensor_task,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = incoming_arrow_artifact_task.get(
                        "id")
                    outgoing_arrow_artifact_task.set("sourceRef", object_artifact_task.get("id"))
                    addbpmnWaypointWithObjectsLeftRight(BPlane, incoming_arrow_artifact_task)
                    addbpmnWaypointWithObjectsLeftRight(BPlane, outgoing_arrow_artifact_task)

                    # Create sensor data object and ref
                    object_artifact_sensor_data_object = ET.SubElement(process,
                                                                       "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObject",
                                                                       {"id": "object_sensor_data" + str(i)})
                    object_artifact_sensor_data_object_ref = ET.SubElement(process,
                                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataObjectReference",
                                                                           {
                                                                               "id": "object_artifact_sensor_data_object_ref" + str(i),
                                                                               "name": "sensor data",
                                                                               "dataObjectRef": object_artifact_sensor_data_object.get(
                                                                                   "id")})
                    addbpmnShape(BPlane, object_artifact_sensor_data_object_ref.get("id"),
                                      int(object_artifact_task_di.get("x")) + 30,
                                      int(object_artifact_task_di.get("y")) - 86, "36", "50")
                    # Create data output association for sensor task
                    data_output_association = ET.SubElement(translated_object_artifact_sensor_task,
                                                            "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataOutputAssociation",
                                                            {"id": "object_artifact_dataoutputassociation" + str(i)})
                    ET.SubElement(data_output_association,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}targetRef").text = object_artifact_sensor_data_object_ref.get(
                        "id")
                    addbpmnEdge(BPlane, data_output_association.get("id"))

                    # Create data input association for actor task
                    placeholder = object_artifact_task.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}property")
                    data_input_association = ET.SubElement(object_artifact_task,
                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}dataInputAssociation",
                                                           {"id": "object_artifact_datainputassociation" + str(i)})
                    addbpmnEdge(BPlane, data_input_association.get("id"))
                    ET.SubElement(data_input_association,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}sourceRef").text = object_artifact_sensor_data_object_ref.get(
                        "id")
                    ET.SubElement(data_input_association,
                                  "{http://www.omg.org/spec/BPMN/20100524/MODEL}targetRef").text = placeholder.get("id")
                    print("object replaced")

                    objectsToBeRemoved.append(child)
                    objectsToBeRemoved.append(finddiElement(BPlane, child.get("id")))
                    dataInputAssociation = findParent(a, process)
                    objectsToBeRemoved.append(dataInputAssociation)
                    objectsToBeRemoved.append(finddiElement(BPlane, dataInputAssociation.get("id")))
                else:
                    if object_artifact.get("id") == a.text:
                        dataInputAssociation = findParent(a, process)
                        objectsToBeRemoved.append(dataInputAssociation)
                        objectsToBeRemoved.append(finddiElement(BPlane, dataInputAssociation.get("id")))

    for child in process.iter():
        i = i + 1
        if child.get("{http://some-company/schema/bpmn/iot}type") == "start":
            # get parent of start event and positioning
            parent = findParent(child, process)
            child_position = getdiElementPosition(finddiElement(BPlane, child.get("id")))

            # create conditional start event
            translated_start_event = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/MODEL}startEvent",
                                                   {"id": "translatedStartEvent" + str(i), "name": child.get("name")})
            addbpmnShape(BPlane, translated_start_event.get("id"), int(child_position.get("x")),
                         int(child_position.get("y")), child_position.get("width"), child_position.get("height"))
            ET.SubElement(translated_start_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}conditionalEventDefinition",
                          {"id": "new_conditEventDefinition" + str(i)})

            # get outgoing sequence flow of old start event and set new start event as source
            sequence_flow = findSequenceFlowSource(process, child.get("id"))
            sequence_flow.set("sourceRef", translated_start_event.get("id"))
            removeAllChilds(finddiElement(BPlane, sequence_flow.get("id")))
            addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)
            ET.SubElement(translated_start_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = sequence_flow.get("id")

            objectsToBeRemoved.append(child)
            objectsToBeRemoved.append(finddiElement(BPlane, child.get("id")))
            print("start replaced")

        if child.get("{http://some-company/schema/bpmn/iot}type") == "end":
            # get parent of end event and positioning
            parent = findParent(child, process)
            child_position = getdiElementPosition(finddiElement(BPlane, child.get("id")))

            # create new end event and new service task
            translated_end_event = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/MODEL}endEvent",
                                                 {"id": "translated_end_event" + str(i)})
            translated_end_event_actor = ET.SubElement(parent,
                                                       "{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask",
                                                       {"id": "translated_end_event_actor_task" + str(i),
                                                        "name": child.get("name")})

            # get incoming sequence flow of the old end event
            sequence_flow = findSequenceFlowTarget(process, child.get("id"))

            # shift everything left (center = old end event) and set new target of sequence flow
            shiftLeft(root, child, 100,process)
            addbpmnShape(BPlane, translated_end_event.get("id"), int(child_position.get("x")),
                         int(child_position.get("y")), child_position.get("width"), child_position.get("height"))
            addbpmnShape(BPlane, translated_end_event_actor.get("id"), int(child_position.get("x")) - 100,
                         int(child_position.get("y")) - 18, "80", "80")
            removeAllChilds(finddiElement(BPlane, sequence_flow.get("id")))
            sequence_flow.set("targetRef", translated_end_event_actor.get("id"))
            addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)
            ET.SubElement(translated_end_event_actor,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = sequence_flow.get("id")

            # create new sequence flow service task to end event
            translated_end_event_sequence_flow = ET.SubElement(parent,
                                                               "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                                               {"id": "translated_end_event_sequence_flow" + str(i),
                                                                "sourceRef": translated_end_event_actor.get("id"),
                                                                "targetRef": translated_end_event.get("id")})
            addbpmnEdge(BPlane, translated_end_event_sequence_flow.get("id"))
            addbpmnWaypointWithObjectsLeftRight(BPlane, translated_end_event_sequence_flow)
            ET.SubElement(translated_end_event_actor,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = translated_end_event_sequence_flow.get(
                "id")
            ET.SubElement(translated_end_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = translated_end_event_sequence_flow.get(
                "id")

            print("end replaced")
            objectsToBeRemoved.append(child)
            objectsToBeRemoved.append(finddiElement(BPlane, child.get("id")))

        if child.get("{http://some-company/schema/bpmn/iot}type") == "throw":
            # get throw event parent and positioning
            parent = findParent(child, process)
            child_position = getdiElementPosition(finddiElement(BPlane, child.get("id")))

            # create new service task
            translated_throw_event = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask",
                                                   {"id": "translated_throw_event" + str(i), "name": child.get("name")})

            # get incoming sequence flow of throw event and shift to service task and shift everything left (center =
            # throw event)
            sequence_flow = findSequenceFlowSource(process, child.get("id"))
            shiftLeft(root, child, 50,process)
            addbpmnShape(BPlane, translated_throw_event.get("id"), int(child_position.get("x")) -40,
                         int(child_position.get("y")), "80", "80")
            sequence_flow.set("sourceRef", translated_throw_event.get("id"))
            removeAllChilds(finddiElement(BPlane,sequence_flow.get("id")))
            addbpmnWaypointWithObjectsLeftRight(BPlane,sequence_flow)
            ET.SubElement(translated_throw_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = sequence_flow.get("id")

            # get outgoing sequence flow of throw event and shift to service task
            sequence_flow = findSequenceFlowTarget(process, child.get("id"))
            sequence_flow.set("targetRef", translated_throw_event.get("id"))
            removeAllChilds(finddiElement(BPlane, sequence_flow.get("id")))
            addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)
            ET.SubElement(translated_throw_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = sequence_flow.get("id")

            print("throw replaced")
            objectsToBeRemoved.append(child)
            objectsToBeRemoved.append(finddiElement(BPlane, child.get("id")))

        if child.get("{http://some-company/schema/bpmn/iot}type") == "catch":
            # get catch event parent and positioning
            parent = findParent(child, process)
            child_position = getdiElementPosition(finddiElement(BPlane, child.get("id")))

            # create new business rule task, gateway and sequence flow business rule task to gateway
            translated_catch_event = ET.SubElement(parent,
                                                   "{http://www.omg.org/spec/BPMN/20100524/MODEL}businessRuleTask",
                                                   {"id": "translated_catch_event" + str(i), "name": "Get Sensor Data"})
            translated_catch_event_gateway = ET.SubElement(parent,
                                                           "{http://www.omg.org/spec/BPMN/20100524/MODEL}exclusiveGateway",
                                                           {"id": "translated_catch_event_gateway" + str(i),
                                                            "name": child.get("name")})
            sequence_flow = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                          {"id": "translated_catch_event_sequence_flow" + str(i),
                                           "sourceRef": translated_catch_event.get("id"),
                                           "targetRef": translated_catch_event_gateway.get("id")})

            addbpmnShape(BPlane, translated_catch_event_gateway.get("id"), int(child_position.get("x")),
                         int(child_position.get("y")), "36", "36")
            shiftLeft(root, translated_catch_event_gateway, 100,process)
            addbpmnShape(BPlane, translated_catch_event.get("id"), int(child_position.get("x")) - 100,
                         int(child_position.get("y")) - 18, "80", "80")
            addbpmnEdge(BPlane, sequence_flow.get("id"))
            addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)
            ET.SubElement(translated_catch_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = sequence_flow.get("id")
            ET.SubElement(translated_catch_event_gateway,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = sequence_flow.get("id")

            # create sequence flow gateway to business rule task
            sequence_flow = ET.SubElement(parent, "{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow",
                                          {"id": "translated_catch_event_sequence_flow" + str(i),
                                           "sourceRef": translated_catch_event_gateway.get("id"),
                                           "targetRef": translated_catch_event.get("id"), "name": "No"})
            addbpmnEdge(BPlane, sequence_flow.get("id"))
            addbpmnWaypointWithObjectsTopTop(BPlane, sequence_flow)
            ET.SubElement(translated_catch_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = sequence_flow.get("id")
            ET.SubElement(translated_catch_event_gateway,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = sequence_flow.get("id")

            # get incoming and outgoing sequence flow of catch event and shift to business rule task and gateway
            sequence_flow = findSequenceFlowTarget(process, child.get("id"))
            removeAllChilds(finddiElement(BPlane, sequence_flow.get("id")))
            sequence_flow.set("targetRef", translated_catch_event.get("id"))
            addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)
            ET.SubElement(translated_catch_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}incoming").text = sequence_flow.get("id")

            sequence_flow = findSequenceFlowSource(process, child.get("id"))
            removeAllChilds(finddiElement(BPlane, sequence_flow.get("id")))
            sequence_flow.set("sourceRef", translated_catch_event_gateway.get("id"))
            sequence_flow.set("name", "Yes")
            addbpmnWaypointWithObjectsLeftRight(BPlane, sequence_flow)
            ET.SubElement(translated_catch_event,
                          "{http://www.omg.org/spec/BPMN/20100524/MODEL}outgoing").text = sequence_flow.get("id")

            print("catch replaced")
            objectsToBeRemoved.append(child)
            objectsToBeRemoved.append(finddiElement(BPlane, child.get("id")))

    for element in objectsToBeRemoved:
        removeObjectFromXML(root, element)

    try:
        tree.write('Translated_Model.bpmn')
        print("bpmn has been written successfully!")
    except (AttributeError, TypeError):
        print("Could not create new file!")
        print("Something is wrong with BPMNE4IoT Model! Is everythinged labeled?")

