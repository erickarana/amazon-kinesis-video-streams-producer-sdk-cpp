import argparse
import boto3
import uuid
from boto3.session import Session
import json

# Tus credenciales de AWS
region_name = 'ca-central-1'  # Reemplaza con la región que desees usar
aws_access_key_id="ASIA3DHD7MHISHDWGNHU"
aws_secret_access_key="M4M8ecT4EYehABHr5N58wq2iojV1XXRi9DKmioFt"
aws_session_token="IQoJb3JpZ2luX2VjEEUaDGNhLWNlbnRyYWwtMSJIMEYCIQDqvkF1CPNmvTzr+sAt+EW6zwy4H5N+uXHxn9PGXobIzAIhAOSj9ft+tzfe0yiOilaTrd9zT8ExHFNpJva+QeDTYr0jKocDCB8QABoMNzYyODM0ODA1MjAxIgzNOibNzPdrGjzoBPQq5AJ89NHqsauP7ops5OoQ36sFy+nPFKS4sfbWU7qxTqzkbyKEyXfSRY0Z90qWC3pe6khlyGnp1esRF4XmwVLY+MuDvPlldQk2pH1712yHGkIj7BZDjSBScDAejD/p4o6uvscL38o6fj3UgCRGEFhLxMTYP5u15CmVZfg+4+kEIv4P1ErfBeI9DDKvsvjpTR9/6MEF8sIcSXizzakGJWSyq55pNphT47j+P4zo0zjP1pyBPu3vhtXeR02myyqvqWoAkwS+et7aqZqCT/Cf861UUBQZst+fW/GKaMqVw9UCk3xn/SttyRKVJlAluLFSQhkT3sm6D0NzDq0q0jHMTe7yb36fJH0On5I49HVqHYyEDro9vqAtCi3uPKmowEF7iACO8YPrBHGsa8mud2jFZfJIc+pHuDB7WG24CBNaLlYx2jd/+2GLDjhRncFjoAS0B4JIrVuF7s7qHKCR0lpADs0YHuAy0rRR5zDCsJquBjqlAehc91/wZi/CKodrkFILsAow9+LbbvGTo5HbJ5fhTajGGddUdk9SwLoHKGg/ULVEkya19DXGkbwJoh6MoTZ0mkIrRLvj2DvnNSSKpG5IEsw4WJM6qxHunX5c/vTzhJsk7k/WiikH10yAH10RtuWUZQldUbkI+RGF1lZXVarkb+1eI9MxQBsiSkBOsIiFgkSY6tjt7YF9//cn4cWCBxmdz03PejyV2w=="
# Crear una sesión de Boto3 con tus credenciales y región
session = Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token,
    region_name=region_name
)


def get_random_uuid():
    return str(uuid.uuid4()).lower()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--param1', help='Interval Id')
    parser.add_argument('--param2', help='Current Time')
    return parser.parse_args()

# Crear un cliente de EventBridge


def main():
    eventbridge = session.client('events')
    house_hold_id = "01HP51A98KTFG0W9YM000CP1N0"
    device_id = "test-156706319882"
    eventTypeValue = "pirSensor"
    args = parse_arguments()
    # Definir el evento
    event = {
        "correlationIds": [
            get_random_uuid()
        ],
        "description": "This is the AssetCreated notification and the below asset has been newly added into Asset Management",
        "returnCode": 0,
        "body": {
            "householdId": house_hold_id,
            "assetId": device_id,
            "alias": "Door Bell",
            "assetStatus": "True",
            "assetType": "telus.d.doorbell",
            "lastUpdatedTs": "",
            "lastUpdatedBy": "",
            "resources": {
                f"/{eventTypeValue}": {
                    "rt": [
                        "aws.r.kvs.video_event"
                    ],
                    "pts": {
                        "current": int(args.param2)
                    },
                    "timestamp": int(args.param2),
                    "if": [
                        "oic.if.s"
                    ],
                    "value": True,
                    "ve": {
                        "vet": f"{eventTypeValue}",
                        "vei": {
                            "current": f"{device_id}-{args.param2}:0"
                        },
                        "vii": {
                            "current": f"{args.param1}"
                        }
                    }
                }
            }
        }
    }

    event_json = json.dumps(event)

    # Publicar el evento en EventBridge
    response = eventbridge.put_events(
        Entries=[{
            'Source': 'SH2.IotCloud.AssetManagement',
            'DetailType': 'SH2.IotCloud.AssetManagement.AssetStateUpdate',
            'EventBusName': 'Sh2PlatformEventBus',
            'Detail': event_json
        }]
    )

    # Imprimir la respuesta
    print(event_json)
    print(response)

    # Verificar si el evento se publicó correctamente
    if response['FailedEntryCount'] == 0:
        print('Evento publicado con éxito')
    else:
        print('Error al publicar el evento:', response)


if __name__ == '__main__':
    main()
