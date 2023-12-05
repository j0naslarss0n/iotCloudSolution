import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

import {
  DynamoDBDocumentClient,
  ScanCommand,
  PutCommand,
  GetCommand,
  DeleteCommand,
} from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});

const dynamo = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {

  const tableName = "temperature_table";

  let body;
  let statusCode = 200;
  const headers = {
    "Content-Type": "application/json",
  };

  body = await dynamo.send(
          new ScanCommand({ TableName: tableName })
        );

  body = body.Items;

  const response = {
    statusCode: 200,
    body: JSON.stringify({"result": body}),
  };
  return response;
};
