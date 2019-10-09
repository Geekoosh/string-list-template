import json
import yaml
import logging
import traceback
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    response = {
      "requestId": event["requestId"],
      "status": "success"
    }
    
    try:
      YAML = 'TemplateYaml'
      JSON = 'TemplateJson'
      if YAML in event["params"]:
        format = YAML
      elif JSON in event["params"]:
        format = JSON
      else:
        raise 'list template must include TemplateYaml or TemplateJson parameters'

      if "Values" in event["params"]:
        values = event["params"]["Values"].split(',')
      elif "Parameter" in event["params"]:
        parameter = event["params"]["Parameter"]
        if parameter not in event["templateParameterValues"]:
          raise 'parameter {} does not exist in stack'.format(parameter)
        values = event["templateParameterValues"][parameter].split(',')
      else:
        raise 'list template must include Values or Parameter parameters'
      
      template = event["params"][format]

      items = []
      for value in values:
        item_str = template.replace('#VALUE#', value.strip())
        if format == YAML:
          item = yaml.load(item_str)
        else:
          item = json.loads(item_str)
        items.append(item)    
      response["fragment"] = items
    except Exception:
        traceback.print_exc()
        response["status"] = "failure"
        macro_response["errorMessage"] = str(e)
    return response