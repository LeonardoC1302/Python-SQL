import { Logger } from '../common'
const sql = require('mssql');

const sqlConfig = {
    user: "root",
    password: "123456",
    database: "caso3",
    server: "localhost",
    pool: {
    max: 1,
    min: 1,
    idleTimeoutMillis: 30000
    },
    options: {
    encrypt: true, 
    trustServerCertificate: true 
    }
}


export class data_wastesPool {
    private log: Logger;

    public constructor()
    {
        this.log = new Logger();
        // via singleton, accediendo a un solo pool tengo una conexiona la base de datos
    }

    public getWasteMovementByQuantity(filter:number) : Promise<any> {
        return sql.connect(sqlConfig).then((pool:any) => {
            return pool.request()
                .input('filter', sql.Int, filter)
                .execute('GetWasteMovementsByQuantity')
                .then((result:any) => {
                    console.log(result)
                    return result.recordset;
                });
        });
    }
    

}