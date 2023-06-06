import logging
import json
import asyncio

import aiocoap.resource as resource
import aiocoap

from flask_out.wot_api import hub

class get_humidity_grove(resource.Resource):

  def get_link_description(self):
    return dict(**super().get_link_description(), request="aiocoap-client -m get coap://localhost:5683/humidity/1")

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
    return dict(**super().get_link_description(), request="aiocoap-client -m get coap://localhost:5683/temperature/1")

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
  root.add_resource(['humidity', '1'], get_humidity_grove())
  root.add_resource(['temperature', '1'], get_temperature_grove())

  await aiocoap.Context.create_server_context(root)
  await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
  asyncio.run(main())
