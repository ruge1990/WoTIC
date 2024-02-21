import logging
import json
import asyncio

import aiocoap.resource as resource
import aiocoap

from flask_out.wot_api import hub

class fan_set(resource.Resource):

  def get_link_description(self):
    return dict(**super().get_link_description(), request='aiocoap-client -m post --payload \'{"target_speed": {"type": "number"}}\' coap://localhost/fan')

  async def render_post(self, request):
    function_name = "fan_set"
    params = []
    kwargs = {}
    if request.payload:
      payload = json.loads(request.payload)
      kwargs["body"] = payload
      for k in payload: 
        params.append(k)
    implementation_path = "flask_out.wot_api.implementations"
    device = "dc_motor_fan"
    result = json.loads(hub.invoke_implementation(function_name, params, kwargs, implementation_path, device))
    code = aiocoap.VALID if result["code"] == 200 else aiocoap.BAD_REQUEST
    return aiocoap.Message(code=code, payload=json.dumps(result).encode("utf8"))

class decrease_fan_speed(resource.Resource):

  def get_link_description(self):
    return dict(**super().get_link_description(), request='aiocoap-client -m post --payload \'{"decrement": {"type": "number"}}\' coap://localhost/fan/decrease')

  async def render_post(self, request):
    function_name = "decrease_fan_speed"
    params = []
    kwargs = {}
    if request.payload:
      payload = json.loads(request.payload)
      kwargs["body"] = payload
      for k in payload: 
        params.append(k)
    implementation_path = "flask_out.wot_api.implementations"
    device = "dc_motor_fan"
    result = json.loads(hub.invoke_implementation(function_name, params, kwargs, implementation_path, device))
    code = aiocoap.VALID if result["code"] == 200 else aiocoap.BAD_REQUEST
    return aiocoap.Message(code=code, payload=json.dumps(result).encode("utf8"))

class increase_fan_speed(resource.Resource):

  def get_link_description(self):
    return dict(**super().get_link_description(), request='aiocoap-client -m post --payload \'{"increment": {"type": "number"}}\' coap://localhost/fan/increase')

  async def render_post(self, request):
    function_name = "increase_fan_speed"
    params = []
    kwargs = {}
    if request.payload:
      payload = json.loads(request.payload)
      kwargs["body"] = payload
      for k in payload: 
        params.append(k)
    implementation_path = "flask_out.wot_api.implementations"
    device = "dc_motor_fan"
    result = json.loads(hub.invoke_implementation(function_name, params, kwargs, implementation_path, device))
    code = aiocoap.VALID if result["code"] == 200 else aiocoap.BAD_REQUEST
    return aiocoap.Message(code=code, payload=json.dumps(result).encode("utf8"))

class fan_turn_off(resource.Resource):

  def get_link_description(self):
    return dict(**super().get_link_description(), request='aiocoap-client -m post coap://localhost/fan/off')

  async def render_post(self, request):
    function_name = "fan_turn_off"
    params = []
    kwargs = {}
    if request.payload:
      payload = json.loads(request.payload)
      kwargs["body"] = payload
      for k in payload: 
        params.append(k)
    implementation_path = "flask_out.wot_api.implementations"
    device = "dc_motor_fan"
    result = json.loads(hub.invoke_implementation(function_name, params, kwargs, implementation_path, device))
    code = aiocoap.VALID if result["code"] == 200 else aiocoap.BAD_REQUEST
    return aiocoap.Message(code=code, payload=json.dumps(result).encode("utf8"))

class get_humidity_grove(resource.Resource):

  def get_link_description(self):
    return dict(**super().get_link_description(), request='aiocoap-client -m get coap://localhost/humidity/1')

  async def render_get(self, request):
    function_name = "get_humidity_grove"
    params = []
    kwargs = {}
    if request.payload:
      payload = json.loads(request.payload)
      kwargs["body"] = payload
      for k in payload: 
        params.append(k)
    implementation_path = "flask_out.wot_api.implementations"
    device = "grove_temperature_humidity_sensor"
    result = json.loads(hub.invoke_implementation(function_name, params, kwargs, implementation_path, device))
    code = aiocoap.VALID if result["code"] == 200 else aiocoap.BAD_REQUEST
    return aiocoap.Message(code=code, payload=json.dumps(result).encode("utf8"))

class get_temperature_grove(resource.Resource):

  def get_link_description(self):
    return dict(**super().get_link_description(), request='aiocoap-client -m get coap://localhost/temperature/1')

  async def render_get(self, request):
    function_name = "get_temperature_grove"
    params = []
    kwargs = {}
    if request.payload:
      payload = json.loads(request.payload)
      kwargs["body"] = payload
      for k in payload: 
        params.append(k)
    implementation_path = "flask_out.wot_api.implementations"
    device = "grove_temperature_humidity_sensor"
    result = json.loads(hub.invoke_implementation(function_name, params, kwargs, implementation_path, device))
    code = aiocoap.VALID if result["code"] == 200 else aiocoap.BAD_REQUEST
    return aiocoap.Message(code=code, payload=json.dumps(result).encode("utf8"))

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
  root = resource.Site()
  root.add_resource(["list"], resource.WKCResource(root.get_resources_as_linkheader))
  root.add_resource(['fan'], fan_set())
  root.add_resource(['fan', 'decrease'], decrease_fan_speed())
  root.add_resource(['fan', 'increase'], increase_fan_speed())
  root.add_resource(['fan', 'off'], fan_turn_off())
  root.add_resource(['humidity', '1'], get_humidity_grove())
  root.add_resource(['temperature', '1'], get_temperature_grove())

  await aiocoap.Context.create_server_context(root)
  await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
  asyncio.run(main())
