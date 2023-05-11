import { Logger } from '../common'
import { data_wastesPool } from '../repositories/data_wastesPool'


export class WastesControllerPool {
    private static instance: WastesControllerPool;
    private log: Logger;

    private constructor()
    {
        this.log = new Logger();
        try
        {
        } catch (e)
        {
            this.log.error(e);
        }
    }

    public static getInstance() : WastesControllerPool
    {
        if (!this.instance)
        {
            this.instance = new WastesControllerPool();
        }
        return this.instance;
    }

    public getFilteredWastes(filter: number) : Promise<any> 
    {
        const wastesdata = new data_wastesPool();
        return wastesdata.getWasteMovementByQuantity(filter);
    }
}