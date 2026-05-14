const { MongoClient } = require('mongodb');

// 副本集连接
const uri = "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0";
const client = new MongoClient(uri);

async function run() {
    await client.connect();
    const db = client.db('testdb');

    // 写操作自动路由到PRIMARY
    insertResult = await db.collection('test').insertOne({ msg: 'Hello' });


    // // 可设置读偏好（实验指导书中错误的API）
    // const secondaryDb = client.db('testdb').withReadPreference('secondaryPreferred');
    // deepseek修复的代码获取一个设置了读偏好的数据库实例
    const secondaryDb = client.db('testdb', { readPreference: 'secondaryPreferred' });
    const docs = await secondaryDb.collection('test').find().toArray();



    // 写点东西控制台输出
    console.log(`插入成功，文档ID: ${insertResult.insertedId}`);
    console.log(`查询到 ${docs.length} 条文档:`);
    console.log(docs);
}
run()