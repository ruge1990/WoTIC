import hub
import inspect
from io import StringIO
import tokenize
import re
import yaml
import json

IMPORT_STATEMENTS = """import logging
import json
import asyncio

import aiocoap.resource as resource
import aiocoap

from flask_out.wot_api import hub
"""


filename = 'server.py'

with open(filename, 'w') as file:
    file.write(IMPORT_STATEMENTS)
 
    with open('api.yaml', 'r') as api_file:
        api_spec = yaml.load(api_file, Loader=yaml.Loader)
        for path in api_spec['paths']:
            for operation in api_spec['paths'][path]:

                function_name = api_spec['paths'][path][operation]['operationId']
                request_device_pattern = re.compile(r"(.*) request on device (.*)")
                matches = request_device_pattern.search(api_spec['paths'][path][operation]['summary'])
                device = matches.group(2)                

            file.write('\nclass ' + function_name + '(resource.Resource):\n')
            file.write('\n  def get_link_description(self):\n')
            if operation == 'post' and 'requestBody' in api_spec['paths'][path][operation]:
                payload = json.dumps(api_spec['paths'][path][operation]['requestBody']['content']['application/x-www-form-urlencoded']['schema']['properties'])
                print(payload)
                file.write(f'    return dict(**super().get_link_description(), request=\'aiocoap-client -m {operation} --payload \\\'{payload}\\\' coap://localhost{path}\')\n')
            else:
                file.write(f'    return dict(**super().get_link_description(), request=\'aiocoap-client -m {operation} coap://localhost{path}\')\n')
            file.write(f'\n  async def render_{operation}(self, request):\n')
            file.write(f'    function_name = "{function_name}"\n')
            file.write('    params = []\n')
            file.write('    kwargs = {}\n')
            file.write('    if request.payload:\n')
            file.write('      payload = json.loads(request.payload)\n')
            file.write('      kwargs["body"] = payload\n')                    
            file.write('      for k in payload: \n')
            file.write('        params.append(k)\n')

            file.write('    implementation_path = "flask_out.wot_api.implementations"\n')
            file.write(f'    device = "{device}"\n')
            file.write('    result = json.loads(hub.invoke_implementation(function_name, params, kwargs, implementation_path, device))\n')
            file.write('    code = aiocoap.VALID if result["code"] == 200 else aiocoap.BAD_REQUEST\n')
            file.write('    return aiocoap.Message(code=code, payload=json.dumps(result).encode("utf8"))\n')
    
        file.write('\nlogging.basicConfig(level=logging.INFO)\n')
        file.write('logging.getLogger("coap-server").setLevel(logging.DEBUG)\n')
        file.write('\nasync def main():\n')
        file.write('  root = resource.Site()\n')
        file.write('  root.add_resource(["list"], resource.WKCResource(root.get_resources_as_linkheader))\n')
        for path in api_spec['paths']:
            for operation in api_spec['paths'][path]:
                function_name = api_spec['paths'][path][operation]['operationId']
                file.write(f'  root.add_resource({path.split("/")[1:]}, {function_name}())\n')

        file.write('\n  await aiocoap.Context.create_server_context(root)\n')
        file.write('  await asyncio.get_running_loop().create_future()\n')
        file.write('\nif __name__ == "__main__":\n')
        file.write('  asyncio.run(main())\n') 