import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  PutCommand

}
  from "@aws-sdk/lib-dynamodb";

/* global fetch*/

const client = new DynamoDBClient({});

const dynamo = DynamoDBDocumentClient.from(client);

const tableName = "temperature_table";


export const handler = async (event) => {

  const r = await fetch("https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/97200/period/latest-hour/data.json");
  const rJson = await r.json();

  if (r.status === 200) {
    console.log(JSON.stringify(rJson))
    await dynamo.send(
      new PutCommand({
        TableName: tableName,
        Item: {
          "device_id": rJson.station.name,
          "timestamp": rJson.value[0].date,

          "metadata": {
            "name": rJson.station.name,
            "device_type": "weatherStation",
          },
          "temperature": parseFloat(rJson.value[0].value)
        },
      })
    );

  }
};
