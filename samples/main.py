import argparse
import boto3
import uuid
from boto3.session import Session
import json

# Tus credenciales de AWS
region_name = 'ca-central-1'  # Reemplaza con la región que desees usar

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
