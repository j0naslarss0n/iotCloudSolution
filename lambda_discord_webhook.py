from discord_webhook import DiscordWebhook, DiscordEmbed
import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('temperature_table')

def lambda_handler(event, context):
    # Query the last entry from DynamoDB table
    print("starting")
    response = table.query(
        KeyConditionExpression=Key('device_id').eq('RPi3_B'),
        ScanIndexForward=False,  # Set to False to get the latest entry
        Limit=1
    )
    print("response", response)
    # Check if there are items in the response
    if 'Items' in response and len(response['Items']) > 0:
        # Extract temperature value from the last entry
        temperature = response['Items'][0]['temperature']
        print("temp sent", temperature)

        # Send the temperature value to Discord
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXXXXXXXXXXXXionCqC2ucLaiOSCvTuAh9HmKCzv")

        # You can customize the embed as needed
        embed = DiscordEmbed(
            title="Morning Temperature:",
            description=f"The latest temperature is {temperature} °C",
            color="03b2f8"
        )
        embed.set_image(url="https://live.staticflickr.com/65535/51531332338_2db58904ca_b.jpg")
        webhook.add_embed(embed)

        # Execute the webhook
        webhook.execute()

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Temperature update sent to Discord"})
    }
