import { TimestreamWriteClient, WriteRecordsCommand } from '@aws-sdk/client-timestream-write';
/*global fetch*/

const client = new TimestreamWriteClient({});

const databaseName = 'smhi_to_timestream';
const tableName = 'smhi_timestream_table';

export const handler = async (event) => {
  const r = await fetch('https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1/station/97200/period/latest-hour/data.json');
  const rJson = await r.json();

  console.log("Got SMHI data", r.status);

  if (r.status === 200) {
    console.log(JSON.stringify(rJson));


    const time = new Date(rJson.value[0].date).getTime() + (60*60*1000);


    console.log("Send data to database" + time);

    await client.send(
      new WriteRecordsCommand({
        DatabaseName: databaseName,
        TableName: tableName,
        Records: [
          {
            Dimensions: [
              { Name: 'device_id', Value: rJson.station.key },
              { Name: 'name', Value: rJson.station.name },
              { Name: 'device_type', Value: 'weatherStation' },
            ],
            MeasureName: 'temperature',
            MeasureValue: `${parseFloat(rJson.value[0].value)}`,
            MeasureValueType: 'DOUBLE',
            Time: time.toString(),
          },
        ],
      })
    );
  }
};
